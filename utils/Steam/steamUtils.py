from requests import get
from requests.exceptions import InvalidSchema, ConnectionError
from bs4 import BeautifulSoup
from utils.systemUtils.osUtils import MachineInfo
from utils.systemUtils.fileMovement import FileManagement
from dotenv import load_dotenv
import os
from utils.gameInfo import GameInfo
import shutil
import urllib
from utils.systemUtils.osUtils import OsUtils, Logger
import subprocess
import git
load_dotenv()

class Steam:
    def __init__(self) -> None:
        _1 = OsUtils()
        _2 = GameInfo()
        self.steamCMDPath = _1.joinPath([_1.cwd, "steamCMD"])
        self.workshopContentPath = _1.joinPath([self.steamCMDPath, "steamapps", "workshop", "content", _2.gameId])
        self.isWindows = _1.isWindows()
        self.cwd = _1.cwd
        self.steamCMDExec = self.getSteamCMDExec()

    def getSteamCMDExec(self):
        _os = OsUtils()
        commands = []
        if self.isWindows:
            commands = [_os.joinPath([self.steamCMDPath, "steamcmd.exe"]), "steamcmd"]
        else:
            commands = ["steamcmd"]
        for command in commands:
            try:
                result = subprocess.run([command, '+quit'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    return command
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue
        return None

class Workshop(Steam):
    def __init__(self) -> None:
        _1 = OsUtils()
        super().__init__()
        self.workshopId = GameInfo().getGameId()
        self.workshopURL = _1.getEnvVariable("WORKSHOPURL")
        if self.isWindows:
            self.downloadString =  + "+login anonymous "
        else:
            self.downloadString = f"steamcmd +force_install_dir {os.path.join(self.cwd, "steamCMD")} " + "+login anonymous "
            
    def getWorkshopIds(self) -> list:
        try:
            _response = get(self.workshopURL)
        except (ConnectionError, InvalidSchema) as e:
            print("Error, invalid URL provided for WORKSHOPURL in env file. Please provide a valid steam workshop collection")
            exit()
        workshopElements = BeautifulSoup(_response.content, 'html.parser').findAll('div', class_="workshopItem")

        mod_ids = []
        i = 0
        for x in workshopElements:
            mod_ids.append(x.find('a').get('href').split('id=')[1])
            if i == 5:
                break
            i += 1
        return mod_ids
        
    def downloadSteamWorkshopMods(self):
        
        for x in self.getWorkshopIds():    
            self.downloadString += f" +workshop_download_item {self.workshopId} {x}"

        self.downloadString += " +quit"
        subprocess.call(self.downloadString, shell=True)

    def main(self):
        SteamCMD().checkSteamCmd()
        self.downloadSteamWorkshopMods()
        FileManagement().moveFiles()


class SteamCMD(Steam):
    

    def __init__(self) -> None:
        super().__init__()
        self.machineInfo = MachineInfo()
        self.distroBase = self.machineInfo.getDistroBase()
        self.osUtils = OsUtils()
        pass


    def steamCmdErrorMessage(self) -> None:
        print("Error installing steamcmd. Please look at the Valve page for information on how to install steamcmd for your machine.")
        print("https://developer.valvesoftware.com/wiki/SteamCMD")
        print("Exiting...")
        exit()


    def __downloadSteamCmdWin(self):
        _os = OsUtils()
        print(f"Detected Windows Machine")
        os.makedirs(_os.joinPath(self.cwd, "steamCMD"), exist_ok=True)
        urllib.request.urlretrieve("https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", _os.joinPath(self.steamCMDPath, "steamcmd.zip"))
        shutil.unpack_archive(_os.joinPath(self.steamCMDPath, "steamcmd.zip"), self.steamCMDPath)
        os.remove(_os.joinPath(self.steamCMDPath, "steamcmd.zip"))
            
        
    def __installSteamCmdArch(self):
        print(f"Detected {self.distroBase} based Distro.")
        self.osUtils.run('sudo pacman -S --needed base-devel git')
        
        try:
            print("Cloning steamcmd...")
            git.Repo.clone_from('https://aur.archlinux.org/steamcmd.git', "steamCmdInstaller")
        except git.GitCommandError as e:

            if not "already exists and is not an empty directory" in e.stderr:
                print("Fatal Error ocurred with cloning the steamcmd package. Find error details below:")
                Logger().logCrit()


            if self.osUtils.confirm("the folder 'steamCmdInstaller' exists already.", "Overwrite?", True):
                shutil.rmtree(os.path.join(self.cwd, "steamCmdInstaller"))
                git.Repo.clone_from('https://aur.archlinux.org/steamcmd.git', "steamCmdInstaller")

        os.chdir('steamCmdInstaller')

        subprocess.call(['makepkg -si --noconfirm'], shell=True)
        os.chdir('../')
        shutil.rmtree(os.path.join(self.cwd, "steamCmdInstaller"))


    def __installSteamCmdDeb(self):
        print(f"Detected {self.distroBase} based distro")
        self.osUtils.run("sudo apt update; sudo apt install software-properties-common; sudo apt-add-repository non-free -y; sudo dpkg --add-architecture i386; sudo apt update", stdout=True)
        self.osUtils.run('echo steam steam/question select "I AGREE" | sudo debconf-set-selections')
        self.osUtils.run('echo steam steam/license note '' | sudo debconf-set-selections')
        self.osUtils.run('sudo apt install steamcmd -y', stdout=True)


    def __installSteamCmdUbuntu(self):
        print(f"Detected {self.distroBase} based distro")
        self.osUtils.run('sudo add-apt-repository multiverse -y; sudo dpkg --add-architecture i386; sudo apt update ')
        self.osUtils.run('echo steam steam/question select "I AGREE" | sudo debconf-set-selections')
        self.osUtils.run('echo steam steam/license note '' | sudo debconf-set-selections')
        self.osUtils.run('sudo apt install steamcmd -y')


    def installSteamCmd(self):
        if self.steamCMDExec != None:
            return
        if self.isWindows:
            self.__downloadSteamCmdWin()
            return
        match self.distroBase:
            case "arch":
                self.__installSteamCmdArch()
            case "debian":
                self.__installSteamCmdDeb()
            case "ubuntu":
                self.__installSteamCmdUbuntu()
            case "rhel":
                print("Error, this script does not support RHEL distros yet.")
                self.steamCmdErrorMessage()
            case "gentoo":
                print("Error, this script does not support RHEL distros yet.")
                self.steamCmdErrorMessage()
        # print("SteamCMD installed!")
        return

    def checkSteamCmd(self):
        if self.steamCMDExec != None:
            return
        
        if not self.osUtils.confirm("steamcmd binary not found.", "Install now?", True):
            self.steamCmdErrorMessage()
        self.installSteamCmd()
        