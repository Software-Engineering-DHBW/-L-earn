"""
Includes the functionality to run the graphical user interface
"""
import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread
from PyQt5.uic import loadUi
import time

import ProcessModule as pm
import DataClasses as dc


# class to run update functions in a thread
class Worker(QObject):

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
                window.tableWidget.setRowCount(len(df.index))
                i = 0
                # update the table (every 5 seconds)
                for index, row in df.iterrows():
                    window.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(row["name"]))
                    window.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(row["create_time"]))
                    window.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem("WIP"))
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


# class that represents the main GUI window
class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.worker = None
        self.thread = None
        self.worker2 = None
        self.thread2 = None
        self.worker3 = None
        self.thread3 = None

        # load UI from file
        loadUi("UserInterface.ui", self)

        # init table
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.createProcessThread()
        self.createProcessThread2()
        self.createProcessThread3()

        # init start button
        self.pushButton.setToolTip("This button starts the [L]earn session.")

        # init stop button
        self.pushButton_2.setToolTip("This button stops the [L]earn session.")

    # function to create a thread, which updates the process table
    def createProcessThread(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.loadProcesses)
        self.thread.start()

    def createProcessThread2(self):
        self.thread2 = QThread()
        self.worker2 = Worker()
        self.worker2.moveToThread(self.thread2)
        self.thread2.started.connect(self.worker2.updateProcessData)
        self.thread2.start()

    def createProcessThread3(self):
        self.thread3 = QThread()
        self.worker3 = Worker()
        self.worker3.moveToThread(self.thread3)
        self.thread3.started.connect(self.worker3.updateCurrentDayData)
        self.thread3.start()


def startWindow():
    app = QApplication(sys.argv)
    global window
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
