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

        self.timers = []

        # Create a QGridLayout instance
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop)

        titleLabel = QLabel("Anwendungslimits")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleLabel.setMaximumHeight(80)
        titleLabel.setMinimumHeight(80)
        titleLabel.setObjectName("title")
        self.main_layout.addWidget(titleLabel)

        limitsFrame = QFrame()
        limitsFrame.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        limitsFrame.setObjectName("limitsFrame")
        frameLayout = QVBoxLayout(limitsFrame)

        # Add widgets to the layout
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

        buttonWidget = QWidget()
        buttonWidget.setObjectName("widget")
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignCenter)
        button = QPushButton()
        button.setText("Limit hinzufügen")
        button.setFont(QFont('Times New Roman', 13))
        button.clicked.connect(self.buttonClicked)

        buttonLayout.addWidget(button)
        buttonWidget.setLayout(buttonLayout)

        frameLayout.addWidget(buttonWidget)

        self.main_layout.addWidget(limitsFrame)

        self.createBottomWidget()

    def createBottomWidget(self):

        bottomFrame = QFrame()
        bottomFrameLayout = QVBoxLayout(bottomFrame)
        bottomFrame.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        bottomFrame.setObjectName("bottomFrame")
        bottomFrame.setStyleSheet("""
                                QFrame#bottomFrame {
                                    background-color: white;
                                    border-radius: 5px;
                                }
                                """)
        self.createLimitList(bottomFrameLayout)
        verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        bottomFrameLayout.addItem(verticalSpacer)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(bottomFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.scrollArea.setStyleSheet("""
                                                QScrollArea 
                                                {
                                                    margin-left: 40px;
                                                    margin-right: 40px;
                                                    background-color: white;
                                                    border-radius: 5px;
                                                    border: None;
                                                }
                                                QScrollBar:vertical
                                                {
                                                    background-color: white;
                                                    width: 9px;
                                                    border-radius: 5px;
                                                }

                                                QScrollBar::handle:vertical
                                                {
                                                    background-color: #d6d6d6;
                                                    border-radius: 5px;
                                                }

                                                QScrollBar::sub-line:vertical
                                                {
                                                    margin: 3px 0px 3px 0px;
                                                    border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
                                                    height: 10px;
                                                    width: 10px;
                                                    subcontrol-position: top;
                                                    subcontrol-origin: margin;
                                                }

                                                QScrollBar::add-line:vertical
                                                {
                                                    margin: 3px 0px 3px 0px;
                                                    border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
                                                    height: 10px;
                                                    width: 10px;
                                                    subcontrol-position: bottom;
                                                    subcontrol-origin: margin;
                                                }

                                                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
                                                {
                                                    background: none;
                                                }

                                                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
                                                {
                                                    background: none;
                                                }""")

        self.main_layout.addWidget(self.scrollArea)

        verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.main_layout.addItem(verticalSpacer)

    def deleteLimit(self):

        data = pm.ProcessData().getBannedProcesses()
        data = data[data.name != self.sender().objectName()]
        pm.ProcessData().setBannedProcesses(data)

        DBHelper().deleteBP(self.sender().objectName(), getpass.getuser())

        self.layout().removeWidget(self.scrollArea)
        self.createBottomWidget()
        return

    def createLimitList(self, layout):

        data = pm.ProcessData().getBannedProcesses()

        if data.empty:
            msgLabel = QLabel("Bisher gibt es noch keine Limits")
            msgLabel.setStyleSheet("QLabel{"
                                   "text-align: Center;"
                                   "color: black;}")
            msgLabel.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(msgLabel)
            return

        for i, row in data.iterrows():
            limitRow = QFrame()
            limitRowLayout = QHBoxLayout(limitRow)
            limitRowLayout.setSpacing(0)
            limitRowLayout.setContentsMargins(0, 0, 0, 0)
            limitRow.setAttribute(QtCore.Qt.WA_StyledBackground, True)
            limitRow.setStyleSheet("QFrame{ max-height: 25px;}")

            limitRowText = row["name"] + ":    Limit: " + str(row.limit // 60) + " min"
            limitRowLabel = QLabel(limitRowText)
            limitRowLabel.setAlignment(QtCore.Qt.AlignLeft)
            limitRowLabel.setStyleSheet("""
                                        QLabel
                                        {
                                           text-align: left;
                                           color: black;
                                           font-size: 18px;
                                           font-family: 'Times New Roman', Times, serif;
                                        }""")

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

    def buttonClicked(self):
        processName = str(self.combo.currentText())
        limittime = int(self.slider.value()) * 60
        username = getpass.getuser()

        banned = {'name': [processName], 'limit': [limittime]}
        banned = pd.DataFrame(banned)
        pm.ProcessData().extendBannedProcesses(banned)

        DBHelper().writeBP(processName, limittime, username)

        self.combo.removeItem(self.combo.currentIndex())
        self.layout().removeWidget(self.scrollArea)
        self.createBottomWidget()

    def addProcesses(self):
        data = DataClasses.ReviewData().createReview()

        username = getpass.getuser()
        dbItems = DBHelper().readBP(username)

        for index, row in dbItems.iterrows():
            banned = {'name': [row['name']], 'limit': [row['limittime']]}
            banned = pd.DataFrame(banned)
            pm.ProcessData().extendBannedProcesses(banned)

        savedItems = list(dbItems["name"])

        for name, row in data.iterrows():
            currentItems = [self.combo.itemText(i) for i in range(self.combo.count())]
            if row['name'] not in currentItems and row['name'] not in savedItems:
                self.combo.addItem(row['name'])
