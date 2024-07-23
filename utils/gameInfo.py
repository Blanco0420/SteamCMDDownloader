from dotenv import load_dotenv
import json
import os
from utils.systemUtils.osUtils import MachineInfo, OsUtils


class GameInfo:
    def openFile(self):
        with open(os.path.join(os.getcwd(), "Modules", f"{self.gameName}.json"))  as f:
                f = json.load(f)
                return f
        
    def __init__(self) -> None:
        _1 = OsUtils()
        load_dotenv()
        self.gameName = _1.getEnvVariable("GAMENAME")
        self.gameInfo = self.openFile()
        self.gameId = self.getGameId()
        self.isWindows = _1.isWindows()



    def getGameId(self):
        return self.gameInfo["workshopId"]


    def getDefaultClientLocation(self):
        path = []
        defaultPath = ""
        if self.isWindows:
            defaultPath = self.openFile()["fileInformation"]["defaultWindowsClientPath"]
        else:
            defaultPath = self.openFile()["fileInformation"]["defaultLinuxClientPath"]
        _1 = OsUtils()
        for x in defaultPath:
            if x == "<currentUser>":
                x = _1.getUser()
            path.append(x)
        return _1.joinPath(path)