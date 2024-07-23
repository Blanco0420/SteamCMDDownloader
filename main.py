from utils.Steam.steamUtils import Workshop, SteamCMD
from utils.systemUtils.fileMovement import FileManagement
from utils.systemUtils.osUtils import Logger, OsUtils

def menu():
    choice = OsUtils().choice(["Download steam workshop mods", "Install steamcmd", "Exit"], 1)
    match choice:
        case 1:
            Workshop().main()
        case 2:
            SteamCMD().installSteamCmd()
        case 3:
            print("Exiting program...")
            exit()
    menu()

menu()