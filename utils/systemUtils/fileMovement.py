import os
from utils.gameInfo import GameInfo
import shutil

class FileManagement:

    def __init__(self):
        self.gameInfo = GameInfo()
        self.fileInfo = self.gameInfo.gameInfo["fileInformation"]

    def getDirectory(self):

        clientDefaultLocation = self.gameInfo.getDefaultClientLocation()
        extractDir = ""
        print("\n\n\n")
        print(f"1) Move to Default location: {clientDefaultLocation}")
        print(f"2) Move to local 'mods' folder: {os.path.join(os.getcwd(), "mods")}")
        print(f"3) Move to custom path")
        # FIXME: Choice enter errors
        choice = int(input("\nChoice: "))
        match choice:
            case 1: 
                extractDir = clientDefaultLocation
            case 2: 
                extractDir = os.path.join(os.getcwd(), "mods")
            case 3:
                extractDir = input("Enter Custom Path: ")
            case _:
                print("Error, incorrect choice. Please try again")
                self.getDirectory()
        return extractDir

    def findModFolderName(self, path):
        try:
            infoFileModName = self.fileInfo["modNameValueFromInfoFile"]
            with open(os.path.join(path, *self.fileInfo["pathToModInfoFile"]), 'r') as file:
                for line in file:
                    if line.strip().startswith(infoFileModName):
                        return line.strip().split(infoFileModName, 1)[1]
            return None
        
        except FileNotFoundError:
            print(f"Mod path: {path}")
            print("A mod info file was not found. Please choose a name for the mod file from the list:")
            i = 1
            files = os.listdir(path)
            for x in files:
                print(f"{i}) {x}")
                i += 1
            print()
            choice = int(input("Choice: "))
            while True:
                if choice < 1 or choice > len(files):
                    print("Invalid Choice. Please try again")
                    choice = int(input("Choice: "))
                    continue
                return files[choice]

    def checkIfHasFiles(self, path):
        for x in os.listdir(path):
            if os.path.isfile(os.path.join(path, x)):
                return True
        return False


    def moveFiles(self):
        extractDir = self.getDirectory()
        if os.path.exists(extractDir):
            print("Extract directory exists. \033[1mOverwrite?\n")
            choice = str
            while choice not in ["y","n", ""]:
                choice = input("\033[0m[Y]es/[N]o (Y): ")
                if choice == "y" or choice == "":
                    shutil.rmtree(extractDir)
                    break
                elif choice == "n":
                    print("Exiting....")
                    exit()
        # TODO: Make this value available from a class for all other ocurrences
        steamcmdPath = os.path.join(os.getcwd(), "steamCMD", "steamapps", "workshop", "content", self.gameInfo.getGameId())
        for workshopFolder in os.listdir(steamcmdPath):
            
            # Add nested folders if they exist. e.g. <workshopFolder>/mods/sub/subsub
            try:
                modFolderPath = os.path.join(steamcmdPath, workshopFolder, *self.fileInfo["pathToModContents"])
            except KeyError:
                modFolderPath = os.path.join(steamcmdPath, workshopFolder)
            # Check for parent folder
            modFolderFiles = os.listdir(modFolderPath)
            if len(modFolderFiles) > 1:
                if not self.checkIfHasFiles(modFolderPath):
                    shutil.copytree(modFolderPath, extractDir, dirs_exist_ok=True)
                    continue
                # Has more than 1 item including files
                modName = self.findModFolderName(modFolderPath)
                newModDir = os.path.join(extractDir, modName)
                shutil.copytree(modFolderPath, newModDir)
                continue
            shutil.copytree(modFolderPath, extractDir, dirs_exist_ok=True)
            continue

