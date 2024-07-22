import os
import platform
from utils.systemUtils.osUtils import OsUtils

class MachineInfo:
    def __init__(self) -> None:
        pass
        self.osUtils = OsUtils()
        
    def isWindows(self):
        if platform.system() == "Windows":
            return True
        return False


    def getUser(self):
        return os.getenv("SUDO_USER") or os.getlogin()


    def getOsReleaseinfo(self):
        try:
            with open('/etc/os-release') as f:
                lines = f.readlines()
                info = {line.split('=')[0]: line.split('=')[1].strip().strip('"') for line in lines}
                return info
        except FileNotFoundError:
            return {}
        

# FIXME: Only check distro info once. Script is supported if steamcmd is installed

    def getDistroBase(self):
        info = self.getOsReleaseinfo()
        from ..Steam.installSteamCmd import SteamCMD
        
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
                self.osUtils.ErrorMessage()
                exit()
            elif id == "gentoo":
                print("Sorry, gentoo machine are not supported by this script yet.")
                self.osUtils.ErrorMessage()
        
        print("Error, unable to determine distro base. Please choose from the list:")
        print("1) Arch based")
        print("2) Debian based")
        print("3) RHEL (Red-Hat Enterprise Linux) based")
        print("4) Gentoo based")
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