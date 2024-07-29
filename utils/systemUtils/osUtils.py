import os
import platform
import logging
from dotenv import load_dotenv

load_dotenv()

class MachineInfo:
    def __init__(self) -> None:
        pass

    def getOsReleaseinfo(self):
        try:
            with open('/etc/os-release') as f:
                lines = f.readlines()
                info = {line.split('=')[0]: line.split('=')[1].strip().strip('"') for line in lines}
                return info
        except FileNotFoundError:
            return {}
        
    def manualDistroBase(self):
        print("Error, unable to determine distro base. Please choose from the list:")
        choice = OsUtils().choice(["Arch based", "Debian based", "Ubuntu based", "RHEL (Red-Hat Enterprise Linux) based", "Gentoo based"])

        match choice:
            case 1: return "arch"
            case 2: return "debian"
            case 3: return "ubuntu"
            case 4: return "rhel"
            case 5: return "gentoo"

    def getDistroBase(self):
        info = self.getOsReleaseinfo()
        
        if 'ID' in info:
            id = info['ID'].lower()
            if id == "debian":
                return 'debian'
            elif id == "ubuntu":
                return 'ubuntu'
            elif id in ['manjaro', 'endeavouros', 'arch']:
                return 'arch'
            elif id in ['centos', 'rhel', 'fedora']:
                return 'rhel'
            elif id == "gentoo":
                return 'gentoo'
        self.manualDistroBase()
        
class Logger:
    def __init__(self) -> None:
        _1 = OsUtils()
        if _1.getEnvBool("DEBUGGING", False):
            level = logging.DEBUG
        else:
            level = logging.WARNING
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%d/%m/%y - %H:%M:%S",
        )
        self.logger = logging.getLogger(__name__)

    def logDebug(self, message: str):
        self.logger.debug(msg=message)

    def logLog(self, message: str):
        self.logger.log(msg=message)
        
    def logWarn(self, message: str):
        self.logger.warn(msg=message)

    def logErr(self):
        self.logger.error(("An error has ocurred. See details below:\n"), exc_info=True)

    def logCrit(self):
        self.logger.critical(("A critical error has ocurred and the program cannot continue. See details below:\n"), exc_info=True)
        exit()

class OsUtils:
    def __init__(self) -> None:
        self.cwd = self.__getCwd()
        pass

    def choice(self, choices: list, default: int) -> int:
        i = 1
        print()
        print()
        for x in choices:
            print(f"{i}) {x}")
            i += 1
        print()
        try:
            choice = input(f'Choice {f"(Default: {default})" if default != None else ""}:')
            choice = int(choice)
            if choice < 1 or choice > len(choices):
                print("Error, invalid Choice. Please try again")
                self.choice(choices, default)    
        except ValueError:
            if choice == "":
                return default
            print("Error, invalid Choice. Please try again")
            self.choice(choices, default)
        return choice

    def confirm(self, message: str, confirmMessage: str, default: bool = True) -> bool:
        print(message)

        choice = "PLACEHOLDER"
        choices = ["y", "n", ""]
        while choice not in choices:
            choice = input(f"\033[1m{confirmMessage} " + ("\033[0m[Y/n]" if default else "\033[0m[y/N]") + ":")
            if choice in choices:
                return True if choice in ["y", ""] else False
            print("Invalid Choice. Please try again")

    # Private Functions:

    def __getCwd(self) -> str:
        return os.getcwd()

    # Public Functions:

    def getEnvVariable(self, variable: str) -> str:
        return os.getenv(variable) or None
    
    def getEnvBool(self, variable: str, default: bool) -> bool:
        _ = os.getenv(variable, str(default)).lower() in ['true', '1', 't']
        return _

    def isWindows(self):
        return platform.system() == "Windows"

    def getUser(self):
        return os.getenv("SUDO_USER") or os.getlogin()

    def joinPath(self, dirs: list) -> str:
        return os.path.join(*dirs)


    def run(self, command:str | list, stdout=False):
        from subprocess import run, PIPE, CalledProcessError
        try:
            res = run(command, shell=True, check=True, stdout=(None if stdout else PIPE), stderr=PIPE, text=True)
        except CalledProcessError as e:
            x = Logger().logErr()

        return res
    # FIXME: Don't return the entire subprocess