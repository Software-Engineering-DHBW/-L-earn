import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QComboBox, QSlider, \
    QPushButton

import DataClasses
import ProcessModule as pm
from DBHelper import DBHelper


class LimitsGUI(QDialog):
    def __init__(self):
        super().__init__()

        self.timers = []

        # Create a QGridLayout instance
        main_layout = QVBoxLayout(self)
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

        limitsFrame = QFrame()
        limitsFrame.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        limitsFrame.setStyleSheet("""
                                    QFrame {
                                        background-color: white;
                                        margin-left: 40px;
                                        margin-right: 40px;
                                        border-radius: 5px;
                                    }
                                    """)
        frameLayout = QVBoxLayout(limitsFrame)

        # Add widgets to the layout
        limitsWidget = QWidget()
        limitsLayout = QHBoxLayout()
        limitsLayout.setAlignment(Qt.AlignLeft)

        limitsLabel = QLabel()
        limitsLabel.setText("Limit setzen für")
        limitsLabel.setFont(QFont('Times New Roman', 13))
        limitsLayout.addWidget(limitsLabel)

        self.combo = QComboBox(self)
        self.combo.setFont(QFont('Times New Roman', 13))

        self.addProcesses()

        limitsLayout.addWidget(self.combo)

        limitsWidget.setLayout(limitsLayout)
        frameLayout.addWidget(limitsWidget)

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

        frameLayout.addWidget(timeWidget)

        buttonWidget = QWidget()
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

    def addProcesses(self):
        data = DataClasses.ReviewData().createReview()
        # savedItems

        for name, row in data.iterrows():
            currentItems = [self.combo.itemText(i) for i in range(self.combo.count())]
            if row['name'] not in currentItems:
                self.combo.addItem(row['name'])
