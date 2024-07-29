import os
from utils.gameInfo import GameInfo
from utils.systemUtils.osUtils import OsUtils, Logger
import shutil

class FileManagement:

    def __init__(self):
        self.gameInfo = GameInfo()
        self.fileInfo = self.gameInfo.gameInfo["fileInformation"]
        self._os = OsUtils()

    def getDirectory(self):

        clientDefaultLocation = self.gameInfo.getDefaultClientLocation()
        extractDir = ""
        choices = [f"Move to Default location: {clientDefaultLocation}", f"Move to local 'mods' folder: {os.path.join(os.getcwd(), "mods")}", "Move to custom path"]
        choice = self._os.choice(choices, 1)
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
            choice = self._os.choice(files)
            return files[choice]

    def checkIfHasFiles(self, path):
        for x in os.listdir(path):
            if os.path.isfile(os.path.join(path, x)):
                return True
        return False


    def moveFiles(self):
        extractDir = self.getDirectory()
        if os.path.exists(extractDir):
            _2 = Logger()
            if self._os.confirm("Extract directory exists", "Overwrite?", True):
                shutil.rmtree(extractDir)
            else:
                _2.logLog("Exiting program...")
                exit()
                
        from utils.Steam.steamUtils import Steam
        steamcmdPath = Steam().workshopContentPath
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
            
        return
