import getpass
import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QComboBox, QSlider, \
    QPushButton, QFrame, QScrollArea

from classes import DataClasses, ProcessModule as pm
from classes.DBHelper import DBHelper


class LimitsGUI(QDialog):
    def __init__(self):
        super().__init__()

        self.scrollArea = None
        self.timers = []

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)

        # upper gui part
        titleLabel = QLabel("Anwendungslimits")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleLabel.setMaximumHeight(80)
        titleLabel.setMinimumHeight(80)
        titleLabel.setObjectName("title")
        self.mainLayout.addWidget(titleLabel)

        # middle gui part
        limitsFrame = QFrame()
        limitsFrame.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        limitsFrame.setObjectName("frame")
        frameLayout = QVBoxLayout(limitsFrame)

        limitsWidget = QWidget()
        limitsWidget.setObjectName("widget")
        limitsLayout = QHBoxLayout()
        limitsLayout.setAlignment(Qt.AlignLeft)

        limitsLabel = QLabel()
        limitsLabel.setText("Limit setzen für")
        limitsLabel.setObjectName("label")
        limitsLayout.addWidget(limitsLabel)

        self.combo = QComboBox(self)
        self.combo.setFont(QFont('Times New Roman', 13))

        self.addProcesses()

        limitsLayout.addWidget(self.combo)

        limitsWidget.setLayout(limitsLayout)
        frameLayout.addWidget(limitsWidget)

        timeWidget = QWidget()
        timeWidget.setObjectName("widget")
        timeLayout = QHBoxLayout()
        timeLayout.setAlignment(Qt.AlignLeft)

        timeLabel = QLabel()
        timeLabel.setText("Limit:")
        timeLabel.setObjectName("label")

        timeLayout.addWidget(timeLabel)

        sliderWidget = QWidget()
        sliderWidget.setObjectName("widget")
        sliderLayout = QVBoxLayout()
        sliderLayout.setAlignment(Qt.AlignCenter)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(180)
        self.slider.setSingleStep(5)
        self.slider.setValue(60)
        self.slider.valueChanged.connect(self.sliderChangedValue)

        sliderLayout.addWidget(self.slider)

        valueWidget = QWidget()
        valueWidget.setObjectName("widget")
        valueLayout = QHBoxLayout()
        valueLayout.setAlignment(Qt.AlignCenter)

        self.valueLabel = QLabel()
        text = self.slider.value().__str__() + " Minuten"
        self.valueLabel.setText(text)
        self.valueLabel.setObjectName("label")

        valueLayout.addWidget(self.valueLabel)
        valueWidget.setLayout(valueLayout)

        sliderLayout.addWidget(valueWidget)
        sliderWidget.setLayout(sliderLayout)

        timeLayout.addWidget(sliderWidget)
        timeWidget.setLayout(timeLayout)

        frameLayout.addWidget(timeWidget)

        # lower gui part
        buttonWidget = QWidget()
        buttonWidget.setObjectName("widget")
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignCenter)
        button = QPushButton()
        button.setText("Limit hinzufügen")
        button.clicked.connect(self.addLimit)

        buttonLayout.addWidget(button)
        buttonWidget.setLayout(buttonLayout)

        frameLayout.addWidget(buttonWidget)

        self.mainLayout.addWidget(limitsFrame)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.mainLayout.addWidget(self.scrollArea)

        self.createBottomWidget()

    def createBottomWidget(self):

        bottomFrame = QFrame()
        self.bottomFrameLayout = QVBoxLayout(bottomFrame)
        bottomFrame.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        bottomFrame.setObjectName("bottomFrame")
        self.createLimitList(self.bottomFrameLayout)
        verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.bottomFrameLayout.addItem(verticalSpacer)

        self.scrollArea.setWidget(bottomFrame)

        verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addItem(verticalSpacer)

    def createLimitList(self, layout):

        data = pm.ProcessData().getBannedProcesses()

        if data.empty:
            msgLabel = QLabel("Bisher gibt es noch keine Limits")
            msgLabel.setObjectName("centerLabel")
            msgLabel.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(msgLabel)
            return

        for i, row in data.iterrows():
            limitRow = QFrame()
            limitRow.setObjectName("rowFrame")
            limitRowLayout = QHBoxLayout(limitRow)
            limitRowLayout.setSpacing(0)
            limitRowLayout.setContentsMargins(0, 0, 0, 0)
            limitRow.setAttribute(QtCore.Qt.WA_StyledBackground, True)

            limitRowText = row["name"] + ":    Limit: " + str(row.limittime // 60) + " min"
            limitRowLabel = QLabel(limitRowText)
            limitRowLabel.setAlignment(QtCore.Qt.AlignLeft)
            limitRowLabel.setObjectName("limitLabel")

            limitRowLayout.addWidget(limitRowLabel)

            limitRowButton = QPushButton("Entfernen")
            limitRowButton.setObjectName(row["name"])
            limitRowButton.clicked.connect(self.deleteLimit)
            limitRowButton.setStyleSheet("QPushButton {max-width: 100px;} ")

            horizontalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum,
                                                     QtWidgets.QSizePolicy.Expanding)
            limitRowLayout.addItem(horizontalSpacer)
            limitRowLayout.addWidget(limitRowButton)

            layout.addWidget(limitRow)

    def sliderChangedValue(self):

        text = self.slider.value().__str__() + " Minuten"
        self.valueLabel.setText(text)

    def addLimit(self):

        processName = str(self.combo.currentText())
        if processName == "":
            return
        else:
            limittime = int(self.slider.value()) * 60
            username = getpass.getuser()

            banned = {'name': [processName], 'limittime': [limittime]}
            banned = pd.DataFrame(banned)
            pm.ProcessData().extendBannedProcesses(banned)

            DBHelper().writeBP(processName, limittime, username)

            self.combo.removeItem(self.combo.currentIndex())
            self.layout().removeWidget(self.scrollArea)
            self.createBottomWidget()


    def deleteLimit(self):
        data = pm.ProcessData().getBannedProcesses()
        data = data[data.name != self.sender().objectName()]
        pm.ProcessData().setBannedProcesses(data)

        processName = self.sender().objectName()
        DBHelper().deleteBP(processName, getpass.getuser())

        self.scrollArea.setWidget(None)
        self.layout().removeWidget(self.scrollArea)

        self.createBottomWidget()

        self.combo.addItem(processName)
        return

    def addProcesses(self):

        data = DataClasses.ReviewData().createReview()

        username = getpass.getuser()
        dbItems = DBHelper().readBP(username)

        for index, row in dbItems.iterrows():
            banned = {'name': [row['name']], 'limittime': [row['limittime']]}
            banned = pd.DataFrame(banned)
            pm.ProcessData().extendBannedProcesses(banned)

        savedItems = list(dbItems["name"])

        for name, row in data.iterrows():
            currentItems = [self.combo.itemText(i) for i in range(self.combo.count())]
            if row['name'] not in currentItems and row['name'] not in savedItems:
                self.combo.addItem(row['name'])
