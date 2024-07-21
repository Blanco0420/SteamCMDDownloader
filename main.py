from utils.Steam import installSteamCmd

def menu():
    while True:
        print("1) Download steam workshop mods")
        print("2) Install steamcmd")
        print("3) Exit")
        print()

        try:
            choice = int(input("Choice: "))
            # choice = 1
        except ValueError:
            print("Error, invalid choice. Please try again")
            print()
            menu()

        match choice:
            case 1:
                downloadWorkshopContent.main()
            case 2:
                installSteamCmd.SteamCMD().installSteamCmd()
            case 3:
                print("Exiting program...")
        



menu()