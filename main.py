from utils.Steam.steamUtils import Steam, SteamCMD
from utils.systemUtils.fileMovement import FileManagement

def menu():
    choice = 0
    print("1) Download steam workshop mods")
    print("2) Install steamcmd")
    print("3) Exit")
    print()

    try:
        choice = int(input("Choice: "))
    except ValueError:
        print("Error, invalid choice. Please try again")
        print()
        menu()

    match choice:
        case 1:
            Steam().main()
        case 2:
            SteamCMD().installSteamCmd()
        case 3:
            print("Exiting program...")
            exit()
            
menu()
        
    



menu()