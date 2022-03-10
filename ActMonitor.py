import pyautogui
import time
import platform

def check_idle_linux():
    import subprocess
    idle_time = int(subprocess.getoutput('xprintidle')) / 1000 # Requires xprintidle (sudo apt install xprintidle)
    if idle_time > 3:
        print("You have been logged out due to inactivity.")

def check_idle_windows():
    import win32api
    idle_time = (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
    if idle_time > 3:

        print("You have been logged out due to inactivity.")



if platform.system() == 'Linux':
    print('linux')
    while 1:
        check_idle_linux()
elif platform.system() == 'Darwin':
    print('Macn not yet')
    while 1:
        check_idle_windows()
elif platform.system() == 'Windows':
    print('windows')













