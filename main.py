from utils.Steam import installSteamCmd

def menu():
    print("1) Download steam workshop mods")
    print("2) Install steamcmd")
    print()

    try:
        # choice = int(input("Choice: "))
        choice = 1
    except ValueError:
        print("Error, invalid choice. Please try again")
        print()
        menu()

    if choice == 1:
        installSteamCmd.main()


menu()