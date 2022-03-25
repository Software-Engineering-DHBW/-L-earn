from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog


class WeekReview(QDialog):

    def __init__(self):
        super().__init__()

        # load UI from file
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.setupUi()

        # init table
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(982, 707)
        self.setAutoFillBackground(False)
        self.setStyleSheet("")

        self.tableWidget.setGeometry(QtCore.QRect(50, 50, 550, 380))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(70, 20, 181, 31))
        font = self.label.font()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Creation time"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Productivity"))
        self.label.setText(_translate("Dialog", "Running processes"))
