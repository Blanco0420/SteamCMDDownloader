import requests
from bs4 import BeautifulSoup
from utils.systemUtils.machineInfo import MachineInfo
from utils.systemUtils.fileMovement import FileManagement
from dotenv import load_dotenv
import os
from utils.gameInfo import GameInfo
import shutil
import urllib
from utils.systemUtils.osUtils import OsUtils
import subprocess
import git
load_dotenv()

class Steam:
    def __init__(self):
        pass
        self.workshopId = GameInfo().getGameId()
        self.isWindowsMachine = MachineInfo().isWindows()
        self.cwd = os.getcwd()
        self.steamcmdInstallPath = os.path.join(self.cwd, "steamCMD")
        if self.isWindowsMachine:
            self.downloadString = os.path.join(self.cwd, "steamCMD", "steamcmd.exe ") + "+login anonymous "
        else:
            self.downloadString = f"steamcmd +force_install_dir {os.path.join(self.cwd, "steamCMD")} " + "+login anonymous "
            
    def getWorkshopIds(self):
        response = requests.get(os.getenv("WORKSHOPURL"))
        soup = BeautifulSoup(response.content, 'html.parser')
        workshopElements = soup.findAll('div', class_="workshopItem")
        mod_ids = []
        # TESTING PURPOSES
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


class SteamCMD:
    def checkInstalled(self):
        commands = []
        if self.machineInfo.isWindows():
            commands = [os.path.join(os.getcwd(), "steamCMD", "steamcmd.exe"), "steamcmd"]
        else:
            commands = ["steamcmd"]
        for command in commands:
            try:
                result = subprocess.run([command, '+quit'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode == 0:
                    return True
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue
        return False
    

    def __init__(self):
        self.machineInfo = MachineInfo()
        self.distroBase = self.machineInfo.getDistroBase()
        self.osUtils = OsUtils()
        self.cwd = self.osUtils.getCwd()
        pass


    def downloadSteamCmdWin(self):
        print(f"Detected Windows Machine")
        os.makedirs(os.path.join(self.cwd, "steamCMD"), exist_ok=True)
        urllib.request.urlretrieve("https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", os.path.join(self.cwd, "steamCMD", "steamcmd.zip"))
        steamcmdPath = os.path.join(self.cwd, "steamcmd")
        shutil.unpack_archive(os.path.join(steamcmdPath, "steamcmd.zip"), steamcmdPath)
        os.remove(os.path.join(steamcmdPath, "steamcmd.zip"))
            
        
    def installSteamCmdArch(self):
        print(f"Detected {self.distroBase} based Distro.")
        self.osUtils.run('sudo pacman -S --needed base-devel git')
        
        try:
            print("Cloning steamcmd...")
            git.Repo.clone_from('https://aur.archlinux.org/steamcmd.git', "steamCmdInstaller")
        except git.GitCommandError as e:
            if not "already exists and is not an empty directory" in e.stderr:
                print("Fatal Error ocurred with cloning the steamcmd package. Find error details below:")
                print(e.stderr.strip())
                print(f"Exit Code: {e.status}")
                exit()
            choice = ""
            # TODO: Make global choice handler
            # FIXME: This doesn't check n
            while choice not in ["y","n", ""]:
                choice = input("the folder 'steamCmdInstaller' exists already. \033[1mOverwrite?\n \033[0m[Y]es/[N]o (Y):").lower()
                if choice == "y" or choice == "":
                    shutil.rmtree(os.path.join(self.cwd, "steamCmdInstaller"))
                    git.Repo.clone_from('https://aur.archlinux.org/steamcmd.git', "steamCmdInstaller")
                    break

        os.chdir('steamCmdInstaller')

        subprocess.call(['makepkg -i --noconfirm'], shell=True)
        os.chdir('../')
        shutil.rmtree(os.path.join(self.cwd, "steamCmdInstaller"))


    def installSteamCmdDeb(self):
        print(f"Detected {self.distroBase} based distro")
        self.osUtils.run("sudo apt update; sudo apt install software-properties-common; sudo apt-add-repository non-free -y; sudo dpkg --add-architecture i386; sudo apt update", stdout=True)
        self.osUtils.run('echo steam steam/question select "I AGREE" | sudo debconf-set-selections')
        self.osUtils.run('echo steam steam/license note '' | sudo debconf-set-selections')
        self.osUtils.run('sudo apt install steamcmd -y', stdout=True)


    def installSteamCmdUbuntu(self):
        print(f"Detected {self.distroBase} based distro")
        self.osUtils.run('sudo add-apt-repository multiverse -y; sudo dpkg --add-architecture i386; sudo apt update ')
        self.osUtils.run('echo steam steam/question select "I AGREE" | sudo debconf-set-selections')
        self.osUtils.run('echo steam steam/license note '' | sudo debconf-set-selections')
        self.osUtils.run('sudo apt install steamcmd -y')


    def installSteamCmd(self):
        if self.machineInfo.isWindows():
            self.downloadSteamCmdWin()
            return
        match self.distroBase:
            case "arch":
                self.installSteamCmdArch()
            case "debian":
                self.installSteamCmdDeb()
            case "ubuntu":
                self.installSteamCmdUbuntu()
                self.osUtils.ErrorMessage()
        print("SteamCMD installed!")
        return

    def checkSteamCmd(self):
        if self.checkInstalled():
            print("steamcmd is already installed")
            print("\n")
            return
        print("steamcmd binary not found. Do you want to install it now?")
        choice = input("[Y]es/[N]o (Y)").lower()
        if choice == "n":
            self.osUtils.ErrorMessage()
        elif choice == "y" or choice == "":
            self.installSteamCmd()
        else:
            print("Invalid option. Please try again")
            self.checkSteamCmd()
        