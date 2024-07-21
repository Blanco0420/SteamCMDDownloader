import os
import platform

def isWindows():
    if platform.system() == "Windows":
        return True
    return False


def getUser():
    if os.getenv("SUDO_USER") == None:
        user = os.getlogin()
    else:
        user = os.getenv("SUDO_USER")

    return user


def getOsReleaseinfo():
    try:
        with open('/etc/os-release') as f:
            lines = f.readlines()
            info = {line.split('=')[0]: line.split('=')[1].strip().strip('"') for line in lines}
            return info
    except FileNotFoundError:
        return {}
    

def getDistroBase():
    info = getOsReleaseinfo()
    if 'ID' in info:
        id = info['ID'].lower()
        if id == "debian":
            return 'debian'
        elif id == "ubuntu":
            return 'ubuntu'
        elif id in ['manjaro', 'endeavouros', 'arch']:
            return 'arch'
        elif id in ['centos', 'rhel', 'fedora']:
            print("Sorry, RedHat systems are not supported by this script yet.")
            from ..Steam.installSteamCmd import ErrorMessage
            ErrorMessage()
            exit()
        elif id == "gentoo":
            return 'gentoo'
    
    print("Error, unable to determine distro base. Please choose from the list:")
    print("1) Arch based")
    print("2) Debian based")
    print("3) Gentoo based")
    print()
    try:
        choice = int(input("Choice:"))
        if choice <1 or choice >3:
            print("Error, invalid choice. Please try again")
    except ValueError:
        print("Error, invalid choice. Please try again")

    match choice:
        case 1: return "arch"
        case 2: return "debian"
        case 3: return "gentoo"

    #TODO: Same thing as above for other bases