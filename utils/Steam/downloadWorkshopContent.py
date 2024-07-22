import requests
from bs4 import BeautifulSoup
from utils.systemUtils.machineInfo import MachineInfo
from utils.systemUtils.fileMovement import FileManagement
from utils.Steam.installSteamCmd import SteamCMD
from dotenv import load_dotenv
import os
from utils.gameInfo import GameInfo
import subprocess
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
