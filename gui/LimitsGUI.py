import getpass

import pandas as pd
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QComboBox, QSlider, \
    QPushButton, QFrame, QScrollArea

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
        limitsFrame.setObjectName("limitsFrame")
        limitsFrame.setStyleSheet("""
                                    QFrame#limitsFrame {
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

        bottomFrame = QFrame()
        bottomFrameLayout = QHBoxLayout(bottomFrame)
        bottomFrame.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        bottomFrame.setObjectName("bottomFrame")
        bottomFrame.setStyleSheet("""
                                    QFrame#bottomFrame {
                                        background-color: white;
                                        margin-left: 40px;
                                        margin-right: 40px;
                                        border-radius: 5px;
                                    }
                                    """)
        self.createLimitList(bottomFrameLayout)

        scrollArea = QScrollArea()
        scrollArea.setWidget(bottomFrame)
        scrollArea.setWidgetResizable(True)
        scrollArea.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        scrollArea.setStyleSheet("""
                                        QScrollArea 
                                        {
                                            margin-left: 40px;
                                            margin-right: 40px;
                                            min-height: 485px;
                                            background-color: white;
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

        main_layout.addWidget(limitsFrame)
        main_layout.addWidget(scrollArea)

        verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        main_layout.addItem(verticalSpacer)

    def deleteLimit(self):
        print("delete")
        return

    def createLimitList(self, layout):

        data = pm.ProcessData().bannedProcesses

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

            limitRowText = row.name + ":    Limit: " + str(row.limittime % 60) + " min"
            limitRowLabel = QLabel(limitRowText)
            limitRowLabel.setAlignment(QtCore.Qt.AlignLeft)
            limitRowLabel.setStyleSheet("""
                                        QLabel
                                        {
                                           text-align: right;
                                           color: black;
                                           font-size: 18px;
                                           min-width: 100px;
                                           font-family: 'Times New Roman', Times, serif;
                                        }""")

            limitRowLayout.addWidget(limitRowLabel)

            limitRowButton = QPushButton("Entfernen")
            limitRowButton.setAlignment(QtCore.Qt.AlignRight)
            limitRowButton.clicked.connect(self.deleteLimit)

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
