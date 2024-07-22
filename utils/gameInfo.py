from dotenv import load_dotenv
import json
import os
from utils.systemUtils.machineInfo import MachineInfo


class GameInfo:
    def openFile(self):
        with open(os.path.join(os.getcwd(), "Modules", f"{self.gameName}.json"))  as f:
                f = json.load(f)
                return f
        
    def __init__(self) -> None:
        load_dotenv()
        self.gameName = self.getVariable("GAMENAME")
        self.gameInfo = self.openFile()


    def getVariable(self, var):
        return os.getenv(var)


    def getGameId(self):
        return self.gameInfo["workshopId"]


    def getDefaultClientLocation(self):
        path = []
        for x in self.openFile()["fileInformation"]["defaultClientPath"]:
            if x == "<currentUser>":
                x = MachineInfo().getUser()
            path.append(x)
        return os.path.join(*path)