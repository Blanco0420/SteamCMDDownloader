import requests
from bs4 import BeautifulSoup
from ..machineBased.machineInfo import DistroInfo
from .installSteamCmd import SteamCMD
from dotenv import load_dotenv
import os
from ..gameInfo import GameInfo
import subprocess
load_dotenv()

class Steam:
    def __init__(self):
        pass
        self.workshopId = GameInfo().getGameId()
        self.distro = DistroInfo()
        self.cwd = os.getcwd()
        if self.distro.isWindows():
            self.downloadString = os.path.join(self.cwd, "steamcmd", "steamcmd.exe ") + "+login anonymous "
        else:
            self.downloadString = f"steamcmd +force_install_dir {os.path.join(self.cwd, "steamcmd")} " + "+login anonymous "
            
    def getWorkshopIds():
        response = requests.get(os.getenv("WORKSHOPURL"))
        soup = BeautifulSoup(response.content, 'html.parser')
        workshopElements = soup.findAll('div', class_="workshopItem")
        mod_ids = []

        for x in workshopElements:
            mod_ids.append(x.find('a').get('href').split('id=')[1])
        return mod_ids
        
    def downloadSteamWorkshopMods(self):
        
        for x in self.getWorkshopIds():    
            self.downloadString += f" +workshop_download_item {self.workshopId} {x}"

        self.downloadString += " +quit"
        subprocess.call(self.downloadString, shell=True)

    def main(self):
        SteamCMD().checkSteamCmd()
        self.downloadSteamWorkshopMods()