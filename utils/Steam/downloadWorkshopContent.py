import requests
from bs4 import BeautifulSoup
from ..machineBased.machineInfo import isWindows
from dotenv import load_dotenv
import os
from ..getGameInfo import getGameId
import subprocess
load_dotenv()



def getWorkshopIds():
    response = requests.get(os.getenv("WORKSHOPURL"))
    soup = BeautifulSoup(response.content, 'html.parser')
    workshopElements = soup.findAll('div', class_="workshopItem")
    mod_ids = []

    for x in workshopElements:
        mod_ids.append(x.find('a').get('href').split('id=')[1])
    return mod_ids
    
def downloadSteamWorkshopMods():
    downloadString = ""
    for x in getWorkshopIds():    
        downloadString += f" +workshop_download_item {getGameId()} {x}"
    if isWindows():
        if os.path.exists(os.path.join(os.getcwd(), "steamcmd")):
            downloadString = "steamcmd " + "+login anonymous " + downloadString
        else:
            downloadString = os.path.join(os.getcwd(), "steamcmd", "steamcmd.exe ") + "+login anonymous " + downloadString
    else:
        downloadString = f"steamcmd +force_install_dir {os.path.join(os.getcwd(), "steamcmd")} " + "+login anonymous " + downloadString
    downloadString += " +quit"
    subprocess.call(downloadString, shell=True)