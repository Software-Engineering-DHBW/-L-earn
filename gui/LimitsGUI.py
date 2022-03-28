import threading

import pandas as pd
import ProcessModule as pm
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QWidget, QComboBox, QSizePolicy, QSlider, \
    QPushButton


class LimitsGUI(QDialog):
    def __init__(self):
        super().__init__()

        self.bannedName = "Steam"
        self.bannedTime = 0

        self.timers = []

        # Create a QGridLayout instance
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        # main_layout.addStretch(10)

        titleLabel = QLabel("Anwendungslimits")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleLabel.setMaximumHeight(80)
        titleLabel.setMinimumHeight(80)
        titleLabel.setStyleSheet("QLabel {"
                                 "background-color: white;"
                                 "text-align: Center;"
                                 "margin-left: 40px;"
                                 "margin-right: 40px;"
                                 "font-size: 30px;"
                                 "font-family: 'Times New Roman', Times, serif;"
                                 "color: black;"
                                 "border-radius: 5px}")
        main_layout.addWidget(titleLabel)
        # Add widgets to the layout
        limitsWidget = QWidget()
        limitsLayout = QHBoxLayout()
        limitsLayout.setAlignment(Qt.AlignLeft)

        limitsLabel = QLabel()
        limitsLabel.setText("Limit setzen für")
        limitsLabel.setFont(QFont('Times New Roman', 13))
        limitsLayout.addWidget(limitsLabel)

        self.combo = QComboBox(self)
        self.combo.addItem("Steam")
        self.combo.addItem("Valorant")
        #self.combo.addItem("")
        self.combo.activated[str].connect(self.dropdownChanged)
        self.combo.setFont(QFont('Times New Roman', 13))
        limitsLayout.addWidget(self.combo)

        limitsWidget.setLayout(limitsLayout)
        main_layout.addWidget(limitsWidget)

        timeWidget = QWidget()
        timeLayout = QHBoxLayout()
        timeLayout.setAlignment(Qt.AlignLeft)

        timeLabel = QLabel()
        timeLabel.setText("Limit:")
        timeLabel.setFont(QFont('Times New Roman', 13))

        timeLayout.addWidget(timeLabel)

        sliderWidget = QWidget()
        sliderLayout = QVBoxLayout()
        sliderLayout.setAlignment(Qt.AlignCenter)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(180)
        self.slider.setSingleStep(5)
        self.slider.setFont(QFont('Times New Roman', 13))
        self.slider.setValue(60)
        self.slider.sliderReleased.connect(self.sliderChangedRelease)
        self.slider.valueChanged.connect(self.sliderChangedValue)

        sliderLayout.addWidget(self.slider)

        valueWidget = QWidget()
        valueLayout = QHBoxLayout()
        valueLayout.setAlignment(Qt.AlignCenter)

        self.valueLabel = QLabel()
        text = self.slider.value().__str__() + " Minuten"
        self.valueLabel.setText(text)
        self.valueLabel.setFont(QFont('Times New Roman', 13))

        valueLayout.addWidget(self.valueLabel)
        valueWidget.setLayout(valueLayout)

        sliderLayout.addWidget(valueWidget)

        sliderWidget.setLayout(sliderLayout)

        timeLayout.addWidget(sliderWidget)

        timeWidget.setLayout(timeLayout)


        main_layout.addWidget(timeWidget)

        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignCenter)
        button = QPushButton()
        button.setText("Limit hinzufügen")
        button.setFont(QFont('Times New Roman', 13))
        button.clicked.connect(self.buttonClicked)

        buttonLayout.addWidget(button)
        buttonWidget.setLayout(buttonLayout)

        main_layout.addWidget(buttonWidget)
        self.setLayout(main_layout)

    def dropdownChanged(self, text):
        self.bannedName = text

    def sliderChangedRelease(self):
        self.bannedTime = self.slider.value()

    def sliderChangedValue(self):
        text = self.slider.value().__str__() + " Minuten"
        self.valueLabel.setText(text)

    def buttonClicked(self):
        banned = {'name': [self.bannedName], 'limit': [self.bannedTime*60]}
        banned = pd.DataFrame(banned)
        pm.ProcessData().extendBannedProcesses(banned)


