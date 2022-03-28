import getpass

import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QComboBox, QSlider, \
    QPushButton, QFrame

from classes import DataClasses, ProcessModule as pm
from classes.DBHelper import DBHelper


class LimitsGUI(QDialog):
    def __init__(self):
        super().__init__()

        self.timers = []

        # Create a QGridLayout instance
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        titleLabel = QLabel("Anwendungslimits")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleLabel.setMaximumHeight(80)
        titleLabel.setMinimumHeight(80)
        titleLabel.setObjectName("title")
        main_layout.addWidget(titleLabel)

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
        main_layout.addWidget(limitsFrame)

        verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        main_layout.addItem(verticalSpacer)

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
