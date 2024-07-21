import os
import urllib
import shutil
import subprocess
from ..machineBased.machineInfo import getDistroBase, isWindows
import git
import sys

def ErrorMessage():
    print("Error installing steamcmd. Please look at the Valve page for information on how to install steamcmd for your machine.")
    print("https://developer.valvesoftware.com/wiki/SteamCMD")
    input("Press enter to exit...")
    exit()
    

def run(command, stdout=False):
    try:
        res = subprocess.run(command, shell=True ,check=True, stdout=(None if stdout else subprocess.PIPE), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("Error Occurred during this command:")
        print(command)
        print("Details:")
        print(e.stderr)
        ErrorMessage()
    return res


def checkInstalled():
    command = ["steamcmd +quit"]
    if isWindows():
        command = [os.path.join(os.getcwd(), "steamcmd", "steamcmd.exe"), command]
    for x in command:
        try:
            return run(x).returncode == 0
            
        except FileNotFoundError:
            pass
        

def downloadSteamCmdWin():
    os.makedirs(os.path.join(os.getcwd(), "steamcmd"), exist_ok=True)
    urllib.request.urlretrieve("https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", os.path.join(os.getcwd(), "steamcmd", "steamcmd.zip"))
    steamcmdPath = os.path.join(os.getcwd(), "steamcmd")
    shutil.unpack_archive(os.path.join(steamcmdPath, "steamcmd.zip"), steamcmdPath)
    os.remove(os.path.join(steamcmdPath, "steamcmd.zip"))
        
    
def installSteamCmdArch():
    print(f"Detected {getDistroBase()} based Distro.")
    run('sudo pacman -S --needed base-devel git')
    
    try:
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

    run(['makepkg', '-si', '--noconfirm'], True)
    os.chdir('../')
    shutil.rmtree(os.path.join(os.getcwd(), "steamCmdInstaller"))

def installSteamCmdDeb():
    run("sudo apt update; sudo apt install software-properties-common; sudo apt-add-repository non-free -y; sudo dpkg --add-architecture i386; sudo apt update", stdout=True)
    run('echo steam steam/question select "I AGREE" | sudo debconf-set-selections')
    run('echo steam steam/license note '' | sudo debconf-set-selections')
    run('sudo apt install steamcmd -y')

def main():
    if isWindows():
        downloadSteamCmdWin()
        return
    match getDistroBase():
        case "arch":
            installSteamCmdArch()
        case "debian":
            installSteamCmdDeb()
        case "ubuntu":
            return
        case "gentoo":
            return
    print("SteamCMD installed!")