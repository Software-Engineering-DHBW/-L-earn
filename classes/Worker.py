"""
Defines the worker classes that contain the thread methods
"""
import os
import threading
from PyQt5.QtCore import QObject
import time
from sys import platform

if platform == "win32":
    import plyer.platforms.win.notification
    from plyer import notification

import Learn
from classes import DataClasses as dc, ProcessModule as pm
from sys import platform
from classes.ActMonitor import check_idleTime_Mac, check_idleTime_windows, check_idleTime_linux
import classes.ActMonitor as am

# variable determines how long idle time is tolerated
global idle_time_sec
idle_time_sec = 600


# check File for either True or False to determine the status of ActivityMonitor
def checkFile():
    with open(os.path.join("logs", "transfer.txt")) as f:
        lines = f.readlines()
        f.close()
    if lines[0] == 'True':
        return True
    else:
        return False


class ActWorker(QObject):
    def __init__(self):
        super().__init__()

    def idleTime(self):

        try:
            while True:
                if checkFile():
                    if platform == 'linux' or platform == 'linux2':
                        check_idleTime_linux(idle_time_sec)
                    elif platform == 'darwin':
                        check_idleTime_Mac(idle_time_sec)
                    elif platform == 'win32':
                        check_idleTime_windows(idle_time_sec)
                time.sleep(5)
        except Exception as e:
            print(e)


# class to run update functions in a thread
class Worker(QObject):

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.timers = []
        self.setTimers = []

    # update process data and check for banned processes
    def updateProcessData(self):

        try:
            pD = pm.ProcessData()
            while True:
                pD.updateData()
                # check for running banned processes
                if len(pD.getBannedProcesses()) != 0:
                    running = pD.checkProcesses()
                    if len(running) != 0:
                        i = 0
                        for r in running:
                            if not r in self.setTimers:
                                # set threading timer to kill banned process after 5 minutes
                                self.timers.append(threading.Timer(300, self.timerEnds, [r, i]))
                                self.setTimers.append(r)
                                self.timers[i].start()
                                title = "[L]earn - Limit Alert"
                                message = "Das Programm " + r + "läuft und hat sein eingestelltes Limit erreicht! Es wird " \
                                                                "deshalb in 5 Minuten beendet! "
                                # send system notification for Windows, Linux, Mac
                                if platform == "win32":
                                    notification.notify(title,message)

                                if platform == "linux":
                                    am.sendmessageLinux(title, message)

                                if platform == "darwin":
                                    am.sendmessageMac(title, message)

                                i += 1

                time.sleep(5)

        except Exception as e:
            print(e)

    def updateCurrentDayData(self):
        cDD = dc.CurrentDayData()
        while True:

            try:
                cDD.updateData()
            except Exception as e:
                print(e)

            time.sleep(300)

    # kill process and delete threading timer
    def timerEnds(self, proc, i):

        try:
            pm.ProcessData().killProcess(proc)
            del self.timers[i]
            self.setTimers.remove(proc)
        except Exception as e:
            print(e)
