import os
import shutil
import subprocess
from urllib import request
from glob import glob
from dotenv import load_dotenv

load_dotenv()


import requests
from bs4 import BeautifulSoup

Server = False
# Check OS
OS = ""

def downloadSteamCmd():
    os.makedirs(os.getcwd(), "mods", exist_ok=True)
    request.urlretrieve("https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", "steamcmd.zip")
    steamcmdPath = os.path.join(os.getcwd(), "steamcmd")
    shutil.unpack_archive(os.path.join(steamcmdPath, "steamcmd.zip"), steamcmdPath)
    os.remove(os.path.join(steamcmdPath, "steamcmd.zip"))

def downloadSteamWorkshopMods():
    response = requests.get(WORKSHOP_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    mod_ids = []
    workshopElements = soup.findAll('div', class_="workshopItem")

    downloadString = ""
    for x in workshopElements:
        mod_ids.append(x.find('a').get('href').split('id=')[1])
    if os.name == "Windows":
        downloadString = ".\\steam.exe "
    else:
        downloadString = f"steamcmd +force_install_dir {os.path.join(os.getcwd(), "steamcmd")} "

    downloadString += "+login anonymous "

    ##### Testing Purposes #####
    downloadString += "+workshop_download_item 108600 1510950729 +workshop_download_item 108600 3171167894"

    # for x in mod_ids:
    #     downloadString += f" +workshop_download_item 108600 {x}"
    downloadString += " +quit"
    subprocess.call(downloadString, shell=True)


def getDirectory():
    extractDir = ""
    print("\n\n\n")
    print(f"1) Move to Default Windows: {defaultWindowsZomboidModsPath}")
    print(f"2) Move to server mods folder: {defaultLinuxServerZomboidModsPath}")
    print(f"3) Move to local 'mods' folder: {os.getcwd()}")
    print(f"4) Move to custom path")

    choice = 3
    # choice = int(input("\nChoice: "))
    match choice:
        case 1: 
            extractDir = defaultWindowsZomboidModsPath
        case 2: 
            extractDir = defaultLinuxServerZomboidModsPath
        case 3: 
            extractDir = os.path.join(os.getcwd(), "mods")
        case 4:
            extractDir = input("Enter Custom Path: ")
        case _:
            print("Error, incorrect choice. Please try again")
            getDirectory()
    return extractDir

def find_id_in_mod_info(mod_info_path):
    with open(mod_info_path, 'r') as file:
        for line in file:
            if line.strip().startswith('id='):
                return line.strip().split('=', 1)[1]
    return None


# downloadSteamWorkshopMods()
extractDir = getDirectory()
if os.path.exists(extractDir):
    shutil.rmtree(extractDir)

for workshopFolder in os.listdir(defaultSteamCmdDownloadPath):
    print(workshopFolder)
    modFolder = os.path.join(defaultSteamCmdDownloadPath, workshopFolder)       
    if os.listdir(modFolder)[0] == "mods":
        print(extractDir)
        shutil.copytree(os.path.join(modFolder, "mods"), extractDir, dirs_exist_ok=True)
        continue

    modInfoFile = os.path.join(modFolder, 'mod.info')
    if not os.path.exists(modInfoFile):
        raise LookupError(f"Cannot find mod.info in {modFolder}")

    with open(modInfoFile, 'r') as file:
        modName = None
        for line in file:
            line = file.readline()
            if not line.startswith("id="):
                continue
            modName = line[3:].strip("\n")
            continue

        if modName is None:
            file.close()
            raise LookupError(f"No ID found in {modInfoFile}") 

        file.close()

    print(modFolder, os.path.join(extractDir, modName))
    shutil.copytree(modFolder, os.path.join(extractDir, modName))