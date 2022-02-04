import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("UserInterface.ui", self)
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.loadData()

    def loadData(self):
        processes = [{"name": "Firefox", "runTime": 124, "productive": True},
                     {"name": "PyCharm", "runTime": 123, "productive": True},
                     {"name": "Explorer", "runTime": 120, "productive": True},
                     {"name": "Word", "runTime": 119, "productive": True},
                     {"name": "Discord", "runTime": 118, "productive": True},
                     {"name": "Spotify", "runTime": 60, "productive": True},
                     {"name": "Steam", "runTime": 3, "productive": False}]

        self.tableWidget.setRowCount(len(processes))

        row = 0
        for p in processes:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(p["name"]))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(p["runTime"])))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(p["productive"])))
            row += 1

app = QApplication(sys.argv)
window = MainWindow()
#window.showMaximized()
window.show()
sys.exit(app.exec_())
