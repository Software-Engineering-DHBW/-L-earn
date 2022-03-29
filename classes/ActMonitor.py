import time
from sys import platform
import os
import subprocess

if platform == "win32":
    import win32api
    from win10toast import ToastNotifier

if platform == "linux" or platform == 'linux2':
    import notify2

if platform == "darwin":
    import pync


def check_idleTime_linux(temp_idle_value_sec):
    idle_time = int(subprocess.getoutput('xprintidle')) / 1000  # Requires xprintidle (sudo apt install xprintidle)
    if idle_time > temp_idle_value_sec:
        sendmessageLinux('Erinnerung', 'Sie haben schon 10 Minuten nichts mehr gemacht')
        time.sleep(2)


def check_idleTime_windows(temp_idle_value_sec):
    idle_time = (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
    if idle_time > temp_idle_value_sec:
        sendmessageWindows('Erinnerung', 'Sie haben schon 10 Minuten nichts mehr gemacht')
        time.sleep(2)


def check_idleTime_Mac(temp_idle_value_sec):
    time.sleep(2)
    cmd = "ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle}'"
    result = os.popen(cmd)  # use popen instead of os.system to open a perl script
    str = result.read()
    temp_idle = int(str.split(".")[0])
    if temp_idle > temp_idle_value_sec:
        sendmessageMac('Erinnerung', 'Sie haben schon 10 Minuten nichts mehr gemacht')


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
        # icon_path="icon.ico",
        threaded=True,
    )


def sendmessageMac(title, message):
    pync.notify(message, title=title)
