import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QSizePolicy

from gui.OnOffButton import Switch


class ActivityMonitorGUI(QWidget):

    def __init__(self):
        super().__init__()

        # Set Variables
        self.monitoringActive = False

        if not os.path.isdir('logs'):
            os.makedirs('logs')
        with open('logs/transfer.txt', 'w') as f:
            f.write('False')
            f.close()

        # Create a QGridLayout instance
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)

        # Add widgets to the layout
        titleLabel = QLabel("Activity Monitor")
        titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        titleLabel.setMaximumHeight(80)
        titleLabel.setMinimumHeight(80)
        titleLabel.setObjectName("title")
        mainLayout.addWidget(titleLabel)

        frame = QFrame()
        frameLayout = QVBoxLayout(frame)
        frameLayout.setAlignment(Qt.AlignTop)
        frame.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        frame.setObjectName("frame")

        monitoringWidget = QWidget()
        monitoringWidget.setObjectName("widget")
        monitoringLayout = QHBoxLayout()
        monSwitch = self.getSwitch()
        monSwitch.clicked.connect(self.switchMonitoring)
        monitoringLayout.addWidget(monSwitch)
        monitoringLabel = QLabel()
        monitoringLabel.setText("Monitoring einschalten")
        monitoringLabel.setObjectName("switchLabel")

        monitoringLayout.addWidget(monitoringLabel)
        monitoringWidget.setLayout(monitoringLayout)

        frameLayout.addWidget(monitoringWidget)
        mainLayout.addWidget(frame)

        verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        mainLayout.addItem(verticalSpacer)

        self.setLayout(mainLayout)

        # Set Switch Values
        if self.monitoringActive:
            self.monitoringActive = False
            monSwitch.click()

    def getSwitch(self):
        switch = Switch()
        switch.setStyleSheet("Switch { margin-left: 40px;}")
        switch.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        return switch

    # toggle monitoring status
    def switchMonitoring(self):
        if not self.monitoringActive:
            self.monitoringActive = True
            with open('logs/transfer.txt', 'w') as f:
                f.write('True')
                f.close()
        elif self.monitoringActive:
            self.monitoringActive = False
            with open('logs/transfer.txt', 'w') as f:
                f.write('False')
                f.close()
