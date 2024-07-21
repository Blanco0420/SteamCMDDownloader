import json
import os
from .jsonAndEnv import openFile
from utils.machineBased.machineInfo import getUser

def getGameId():
    return openFile()["workshopid"]

def getInstallLocation():
    path = []
    for x in openFile()["modFolder"]:
        if x == "<user>":
            x = getUser()
        path.append(x)
        print(os.path.join(*path))
    return path