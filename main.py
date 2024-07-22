import utils.Steam
import utils.Steam.downloadWorkshopContent
import utils.Steam.installSteamCmd

def menu():
    choice = 0
    print("1) Download steam workshop mods")
    print("2) Install steamcmd")
    print("3) Exit")
    print()

    try:
        # choice = int(input("Choice: "))
        choice = 1
    except ValueError:
        print("Error, invalid choice. Please try again")
        print()
        menu()

    match choice:
        case 1:
            utils.Steam.downloadWorkshopContent.Steam().main()
        case 2:
            utils.Steam.installSteamCmd.SteamCMD().installSteamCmd()
        case 3:
            print("Exiting program...")
    menu()
        
    



menu()