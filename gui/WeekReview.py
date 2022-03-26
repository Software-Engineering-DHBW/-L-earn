from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QLabel
import datetime

import DataClasses


class ProgressBar(QProgressBar):

    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setValue(0)


class WeekReview(QDialog):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #2196f3;')

        titleLabel = QLabel("Wochenrückblick")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleLabel.setMaximumHeight(80)
        titleLabel.setStyleSheet("QLabel {"
                                 "background-color: #0069c0;"
                                 "text-align: Center;"
                                 "font-size: 30px;"
                                 "font-family: 'Times New Roman', Times, serif;"
                                 "color: white;}")
        layout.addWidget(titleLabel)
        self.createReviewBars(layout)

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

    def createReviewBars(self, layout):

        # get review data form DataClasses
        data = DataClasses.ReviewData().createReview()

        if data.empty:
            msgLabel = QLabel("Ganz schön leer hier :( !?\n"
                              "Es gibt bisher leider nicht genug Daten um einen Rückblick zu erstellen!")
            msgLabel.setStyleSheet("QLabel{"
                                   "text-align: Center;"
                                   "color: white;}")
            msgLabel.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(msgLabel)
            return

        data.drop(['date'], axis=1, inplace=True)
        data = data.groupby(data['name']).aggregate({'runtime': 'sum'})
        data.sort_values(by=['runtime'], ascending=False, inplace=True)

        i = 0
        for name, row in data.iterrows():

            if i == 0:
                maxVal = row.runtime
            if i >= 10:
                break
            i += 1

            # create the string for the runtime of each process
            barTime = ""
            runtime = (datetime.timedelta(seconds=round(row.runtime)))
            if runtime.days != 0:
                barTime += str(runtime.days) + "d " + str(runtime.seconds // 3600) + "h " + str(
                    (runtime.seconds // 60) % 60) + "min"
            elif runtime.seconds // 3600 != 0:
                barTime += str(runtime.seconds // 3600) + "h " + str((runtime.seconds // 60) % 60) + "min"
            elif (runtime.seconds // 60) % 60 != 0:
                barTime += str((runtime.seconds // 60) % 60) + "min"
            else:
                return

            # put together final process description
            barText = "     " + name + ":   " + barTime

            # create progress bar
            bar = QProgressBar()
            bar.setMinimum(0)
            bar.setMaximum(maxVal)
            bar.setValue(row.runtime)
            bar.setFormat(barText)
            bar.setAlignment(QtCore.Qt.AlignLeft)
            bar.setStyleSheet("QProgressBar {"
                              " border-radius: 5px;"
                              " text-align: left;"
                              " font-size: 18px;"
                              " font-family: 'Times New Roman', Times, serif;"
                              " color: black;"
                              " T min-height: 35px;} "
                              "QProgressBar::chunk {"
                              "background-color: #6ec6ff;"
                              " border-radius: 5px;}")

            layout.addWidget(bar)
