from dotenv import load_dotenv
import json
import os
from .machineBased.machineInfo import DistroInfo


class GameInfo:
    def __init__(self) -> None:
        load_dotenv()

    def getVariable(var):
        return os.getenv(var)

    def openFile(self):
        with open(os.path.join("Modules", f"{self.getVariable("GAMENAME")}.json"))  as f:
                f = json.load(f)
                return f

    def getGameId(self):
        return self.openFile()["workshopid"]

    def getInstallLocation(self):
        path = []
        for x in self.openFile()["modFolder"]:
            if x == "<user>":
                x = DistroInfo().getUser()
            path.append(x)
            print(os.path.join(*path))
        return path