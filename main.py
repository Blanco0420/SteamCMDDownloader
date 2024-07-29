from utils.Steam.steamUtils import Workshop, SteamCMD
from utils.systemUtils.fileMovement import FileManagement

def menu():
    # choice = OsUtils().choice(["Download steam workshop mods", "Install steamcmd", "Exit"], 1)
    choice = 4
    match choice:
        case 1:
            Workshop().main()
        case 2:
            SteamCMD().installSteamCmd()
        case 3:
            print("Exiting program...")
            exit()
        case 4:
            #TESTING PURPOSES ONLY!!!!
            FileManagement().moveFiles()
    menu()

menu()