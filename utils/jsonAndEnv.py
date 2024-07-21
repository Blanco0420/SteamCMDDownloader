from dotenv import load_dotenv
import json
import os

load_dotenv()

def getVariable(var):
    return os.getenv(var)

def openFile():
    with open(os.path.join("Modules", f"{getVariable("GAMENAME")}.json"))  as f:
            f = json.load(f)
            return f