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


# class that represents the main GUI window
class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.worker = None
        self.thread = None

        # load UI from file
        loadUi("UserInterface.ui", self)

        # init table
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.loadProcesses()

        # init start button
        self.pushButton.setToolTip("This button starts the [L]earn session.")

        # init stop button
        self.pushButton_2.setToolTip("This button stops the [L]earn session.")

    # function to create a thread, which updates the process table
    def loadProcesses(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.loadProcesses)
        self.thread.start()

def startWindow():
    app = QApplication(sys.argv)
    global window
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
