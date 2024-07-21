import os
import getGameInfo
import shutil

def getDirectory():
    modsLocation = getGameInfo.getInstallLocation()
    extractDir = ""
    print("\n\n\n")
    print(f"1) Move to Default Windows: {modsLocation}")
    print(f"2) Move to local 'mods' folder: {os.getcwd()}")
    print(f"3) Move to custom path")

    choice = int(input("\nChoice: "))
    match choice:
        case 1: 
            extractDir = modsLocation
        case 2: 
            extractDir = os.path.join(os.getcwd(), "mods")
        case 3:
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


def moveFiles():
    steamcmdPath = os.path.join(os.getcwd(), "steamcmd", "steamapps", "workshop", "content", getGameInfo.getGameId())
    extractDir = getDirectory()
    for workshopFolder in os.listdir():
        modFolder = os.path.join(steamcmdPath, workshopFolder)       
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