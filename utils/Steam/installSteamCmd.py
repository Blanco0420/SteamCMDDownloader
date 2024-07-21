import os
import urllib
import shutil
import subprocess
from ..machineBased.machineInfo import getDistroBase, isWindows
import git
import time

def run(command, stdout=False):
    try:
        res = subprocess.run(command, shell=True, check=True, stdout=(None if stdout else subprocess.PIPE), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("Error Occurred during this command:")
        print(command)
        print("Details:")
        print(e.stderr)
        SteamCMD().ErrorMessage()
    return res

class SteamCMD:
    def checkInstalled():
        try:
            result = subprocess.run(["steamcmd", '+quit'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                return True
        except FileNotFoundError:
            return False
        return False
    

    def __init__(self):
        self.isInstalled = self.checkInstalled()
        pass

    def ErrorMessage():
        print("Error installing steamcmd. Please look at the Valve page for information on how to install steamcmd for your machine.")
        print("https://developer.valvesoftware.com/wiki/SteamCMD")
        input("Press enter to exit...")
        exit()


    def downloadSteamCmdWin():
        print(f"Detected Windows Machine")
        os.makedirs(os.path.join(os.getcwd(), "steamcmd"), exist_ok=True)
        urllib.request.urlretrieve("https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", os.path.join(os.getcwd(), "steamcmd", "steamcmd.zip"))
        steamcmdPath = os.path.join(os.getcwd(), "steamcmd")
        shutil.unpack_archive(os.path.join(steamcmdPath, "steamcmd.zip"), steamcmdPath)
        os.remove(os.path.join(steamcmdPath, "steamcmd.zip"))
            
        
    def installSteamCmdArch():
        print(f"Detected {getDistroBase()} based Distro.")
        run('sudo pacman -S --needed base-devel git')
        
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
            while choice not in ["y","n"]:
                choice = input("the folder 'steamCmdInstaller' exists already. \033[1mOverwrite?\n \033[0m[Y]es/[N]o (Y):").lower()
                if choice == "y" or choice == "":
                    shutil.rmtree(os.path.join(os.getcwd(), "steamCmdInstaller"))
                    git.Repo.clone_from('https://aur.archlinux.org/steamcmd.git', "steamCmdInstaller")
                    break

        os.chdir('steamCmdInstaller')

        subprocess.run(['makepkg', '-s', '-i', '--noconfirm'], check=True, stdout=None, stderr=subprocess.PIPE)
        os.chdir('../')
        shutil.rmtree(os.path.join(os.getcwd(), "steamCmdInstaller"))


    def installSteamCmdDeb():
        print(f"Detected {getDistroBase()} based distro")
        run("sudo apt update; sudo apt install software-properties-common; sudo apt-add-repository non-free -y; sudo dpkg --add-architecture i386; sudo apt update", stdout=True)
        run('echo steam steam/question select "I AGREE" | sudo debconf-set-selections')
        run('echo steam steam/license note '' | sudo debconf-set-selections')
        run('sudo apt install steamcmd -y')


    def installSteamCmdUbuntu():
        print(f"Detected {getDistroBase()} based distro")
        run('sudo add-apt-repository multiverse -y; sudo dpkg --add-architecture i386; sudo apt update ')
        run('echo steam steam/question select "I AGREE" | sudo debconf-set-selections')
        run('echo steam steam/license note '' | sudo debconf-set-selections')
        run('sudo apt install steamcmd -y')


    def installSteamCmd(self):
        if isWindows():
            self.downloadSteamCmdWin()
            return
        match getDistroBase():
            case "arch":
                self.installSteamCmdArch()
            case "debian":
                self.installSteamCmdDeb()
            case "ubuntu":
                self.installSteamCmdUbuntu()
            case "gentoo":
                print("Error, gentoo machine are not supported by this script yet.")
                self.ErrorMessage()
        print("SteamCMD installed!")
        return

    def checkSteamCmd(self):
        if self.isInstalled:
            print("steamcmd is already installed")
            time.sleep(1)
            print("\n")
            return
        
        print("steamcmd binary not found. Do you want to install it now?")
        choice = input("[Y]es/[N]o (Y)").lower()
        if choice == "n":
            self.ErrorMessage()
        elif choice == "y" or choice == "":
            self.installSteamCmd()
        else:
            print("Invalid option. Please try again")
            self.installSteamCmd()