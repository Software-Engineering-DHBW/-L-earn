from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
import time
from sys import platform

from ActMonitor import check_idle_Mac, check_idle_windows, check_idle_linux
import ProcessModule as pm
import DataClasses as dc

global idle_time_sec
idle_time_sec = 600
def checkFile():
    with open('logs/transfer.txt') as f:
        lines = f.readlines()
        f.close()
        print(lines[0])
    if lines[0] == 'True':
        return True
    else:
        return False

class ActWorker(QObject):
    def __init__(self):
        super().__init__()


    def idleTime(self):
        while True:
            if platform == 'linux' and checkFile() or platform == 'linux2' and checkFile():
                print('linux')
                check_idle_linux(idle_time_sec)
            elif platform == 'darwin' and checkFile():
                print('Macn not yet')
                check_idle_Mac(idle_time_sec)
            elif platform == 'win32'and checkFile():
                print('windows')
                check_idle_windows(idle_time_sec)
            time.sleep(5)


# class to run update functions in a thread
class Worker(QObject):

    def __init__(self, window):
        super().__init__()
        self.window = window

    # function to load the current processes and update the table
    def loadProcesses(self):
        previousDf = None

        # endless loop to update the processes
        while True:

            # load currently running processes via module
            df = pm.getAllProcesses()

            # if the process dataframe did not change, the table does not need to be updated
            if df.equals(previousDf):
                time.sleep(5)
                continue
            else:
                previousDf = df
                self.window.tableWidget.setRowCount(len(df.index))
                i = 0
                # update the table (every 5 seconds)
                for index, row in df.iterrows():
                    self.window.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(row["name"]))
                    self.window.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row["create_time"]))
                    self.window.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem("WIP"))
                    i += 1
                time.sleep(5)

    def updateProcessData(self):
        pD = pm.ProcessData()
        while True:
            pD.updateData()
            time.sleep(5)

    def updateCurrentDayData(self):
        cDD = dc.CurrentDayData()
        while True:

            try:
                cDD.updateData()
            except Exception as e:
                print(e)

            time.sleep(300)
