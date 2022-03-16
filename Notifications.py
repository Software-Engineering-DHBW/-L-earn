from sys import platform
import subprocess
import logging

class Notifications(object):

    def __init__(self):
        self.__setLogger()

    def __setLogger(self):
        # create a logger
        self.logger = logging.getLogger('ntflogger')
        # set logger level
        self.logger.setLevel(logging.ERROR)
        # or set one of the following level
        # logger.setLevel(logging.CRITICAL)
        # logger.setLevel(logging.WARNING)
        # logger.setLevel(logging.INFO)
        # logger.setLevel(logging.DEBUG)

        handler = logging.FileHandler('logs/ntflog.log')
        # create a logging format
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def enableNtf(self):
        if platform == "linux" or platform == "linux2":
            # linux
            self.__enableNtfLinux()
        elif platform == "darwin":
            # OS X
            self.__enableNtfMac()
        elif platform == "win32":
            # Windows...
            self.__enableNtfWindows()
        else:
            self.logger.error("No valid system for enabling Notifications")

    def disableNtf(self):
        if platform == "linux" or platform == "linux2":
            # linux
            self.__disableNtfLinux()
        elif platform == "darwin":
            # OS X
            self.__disableNtfMac()
        elif platform == "win32":
            # Windows...
            self.__disableNtfWindows()
        else:
            self.logger.error("No valid system for disabling Notifications")

    def __enableNtfLinux(self):
        # check state
        showNtf = subprocess.check_output(["gsettings get org.gnome.desktop.notifications show-banners"])
        if not showNtf:
            # enable Notifications
            subprocess.Popen(["gsettings set org.gnome.desktop.notifications show-banners true"])
            # notify user
            subprocess.Popen(["notify-send 'Notifications are disabled' -i user-busy"])

            self.logger.info("enabled Notifications")
        else:
            self.logger.info("Notifications are already enabled")

    def __disableNtfLinux(self):
        # check state
        showNtf = subprocess.check_output(["gsettings get org.gnome.desktop.notifications show-banners"])
        if showNtf:
            # disable Notifications
            subprocess.Popen(["gsettings set org.gnome.desktop.notifications show-banners false"])
            # notify user
            subprocess.Popen(["notify-send 'Notifications are enabled' -i user-available"])

            self.logger.info("disabled Notifications")
        else:
            self.logger.info("Notifications are already disabled")

    def __enableNtfMac(self):
        # Read state from defaults
        dndState = int(
            subprocess.check_output(["defaults read com.apple.controlcenter 'NSStatusItem Visible DoNotDisturb'"],
                                    shell=True).decode())
        if dndState == 1:
            # Set short key ^⌥⇧⌘D for doNotDisturb
            subprocess.Popen([
                                 "defaults write ~/Library/Preferences/com.apple.symbolichotkeys.plist "
                                 "AppleSymbolicHotKeys -dict-add 175 "
                                 "'<dict><key>enabled</key><true/><key>value</key><dict><key>parameters</key>"
                                 "<array><integer>100</integer><integer>2</integer><integer>1966080</integer></array>"
                                 "<key>type</key><string>standard</string></dict></dict>'"],
                             shell=True)
            subprocess.Popen(
                ["/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/activateSettings -u"],
                shell=True)
            # Press short key to deactivate doNotDisturb
            subprocess.Popen([
                                 "osascript -e 'tell application \"System Events\" to keystroke \"D\" using {command "
                                 "down, shift down, option down, control down}'"],
                             shell=True)
            # Save state in defaults
            subprocess.Popen(["defaults write com.apple.controlcenter 'NSStatusItem Visible DoNotDisturb' 0"],
                             shell=True)

            self.logger.info("enabled Notifications")
        else:
            self.logger.info("Notifications are already enabled")

    def __disableNtfMac(self):
        # Read state from defaults
        dndState = int(
            subprocess.check_output(["defaults read com.apple.controlcenter 'NSStatusItem Visible DoNotDisturb'"],
                                    shell=True).decode())
        if dndState == 0:
            # Set short key ^⌥⇧⌘D for doNotDisturb
            subprocess.Popen([
                                 "defaults write ~/Library/Preferences/com.apple.symbolichotkeys.plist "
                                 "AppleSymbolicHotKeys -dict-add 175 "
                                 "'<dict><key>enabled</key><true/><key>value</key><dict><key>parameters</key>"
                                 "<array><integer>100</integer><integer>2</integer><integer>1966080</integer></array>"
                                 "<key>type</key><string>standard</string></dict></dict>'"],
                             shell=True)
            subprocess.Popen(
                ["/System/Library/PrivateFrameworks/SystemAdministration.framework/Resources/activateSettings -u"],
                shell=True)
            # Press short key to activate doNotDisturb
            subprocess.Popen([
                                 "osascript -e 'tell application \"System Events\" to keystroke \"D\" using {command "
                                 "down, shift down, option down, control down}'"],
                             shell=True)
            # Save state in defaults
            subprocess.Popen(["defaults write com.apple.controlcenter 'NSStatusItem Visible DoNotDisturb' 1"],
                             shell=True)

            self.logger.info("disabled Notifications")
        else:
            self.logger.info("Notifications are already disabled")

    def __enableNtfWindows(self):
        print("ToDo")
        subprocess.Popen(["python WnfDump.py -w WNF_SHEL_QUIET_MOMENT_SHELL_MODE_CHANGED 1"],
                         shell=True)

    def __disableNtfWindows(self):
        print("ToDo")
        subprocess.Popen(["python WnfDump.py -w WNF_SHEL_QUIET_MOMENT_SHELL_MODE_CHANGED 0"],
                         shell=True)
