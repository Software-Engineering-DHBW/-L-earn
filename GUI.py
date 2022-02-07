import sys
import platform
import pandas as pd
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.uic import loadUi
import time

import ProcessModule as win
from functions import mac_functions as mac


class Worker(QObject):

    def loadProcesses(self):
        previousDf = None
        while True:
            # checking what operating system the software is running on
            os = platform.system()
            if os == "Windows" or os == "Linux":
                df = win.getAllProcesses()
            elif os == "Darwin":
                df = mac.getProcesses()

            if df.equals(previousDf):
                time.sleep(5)
                continue
            else:
                previousDf = df
                window.tableWidget.setRowCount(len(df.index))
                i = 0
                for index, row in df.iterrows():
                    window.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(row["name"]))
                    window.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row["create_time"]))
                    window.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem("WIP"))
                    i += 1
                time.sleep(5)



class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.worker = None
        self.thread = None
        loadUi("UserInterface.ui", self)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.loadProcesses()

    def loadProcesses(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.loadProcesses)
        self.thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
