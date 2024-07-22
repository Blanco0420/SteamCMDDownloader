import subprocess
import os

class OsUtils:
    def __init__(self) -> None:
        pass


    def ErrorMessage(self):
        print("Error installing steamcmd. Please look at the Valve page for information on how to install steamcmd for your machine.")
        print("https://developer.valvesoftware.com/wiki/SteamCMD")
        input("Press enter to exit...")
        exit()

    def getCwd(self):
        return os.getcwd()

    def run(self, command, stdout=False):
        try:
            res = subprocess.run(command, shell=True, check=True, stdout=(None if stdout else subprocess.PIPE), stderr=subprocess.PIPE, text=True)
        except subprocess.CalledProcessError as e:
            print("Error Occurred during this command:")
            print(command)
            print("Details:")
            print(e.stderr)
            self.ErrorMessage()
        return res