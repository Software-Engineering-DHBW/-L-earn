import time
from sys import platform
import notify2
import os
import subprocess
import pync

if platform == "win32":
    from win32gui import GetWindowText, GetForegroundWindow
    from win10toast import ToastNotifier

def check_idle_linux(temp_idle_value_sec):
    idle_time = int(subprocess.getoutput('xprintidle')) / 1000 # Requires xprintidle (sudo apt install xprintidle)
    if idle_time > temp_idle_value_sec:
        print("You have been logged out due to inactivity.")
        sendmessageLinux('test','This is a Testmessage')
        time.sleep(2)

def check_idle_windows(temp_idle_value_sec):
    idle_time = (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
    if idle_time > temp_idle_value_sec:
        sendmessageWindows('test','This is a Testmessage')
        time.sleep(2)
        print("You have been logged out due to inactivity.")

def check_idle_Mac(temp_idle_value_sec):
        time.sleep(2)
        cmd = "ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle}'"
        result = os.popen(cmd)  # use popen instead of os.system to open a perl script
        str = result.read()
        temp_idle = int(str.split(".")[0])
        # print(str)
        if temp_idle > temp_idle_value_sec:
            sendmessageMac('Test','This is a Text Message')
            print("You have been logged out due to inactivity.")


def sendmessageLinux(title, message):
    notify2.init("Test")
    notice = notify2.Notification(title, message)
    notice.show()
    return

def sendmessageWindows(title, message):
    toast = ToastNotifier()
    toast.show_toast(
        title,
        message,
        duration=20,
        #icon_path="icon.ico",
        threaded=True,
    )

def sendmessageMac(title, message):
    pync.notify(message, title=title)


def idleTime(idle_time_sec):
    if platform == 'linux':
        print('linux')
        while 1:
            check_idle_linux(idle_time_sec)
    elif platform == 'darwin':
        print('Macn not yet')
        while 1:
            check_idle_Mac(idle_time_sec)
    elif platform == 'win32':
        print('windows')
        while 1:
            check_idle_windows(idle_time_sec)













