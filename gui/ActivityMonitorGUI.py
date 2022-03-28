from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QSizePolicy

from gui.OnOffButton import Switch




class ActivityMonitorGUI(QWidget):

    def __init__(self):
        super().__init__()



        #self.createProcessThread4()

        #Set Variables
        self.monitoringActive =False
        with open('logs/transfer.txt', 'w') as f:
            f.write('False')
            f.close()
        print('false')
        # Create a QGridLayout instance
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Add widgets to the layout
        titleLabel = QLabel("Activity Monitor")
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

        frame = QFrame()
        frameLayout = QVBoxLayout(frame)
        # frameLayout.setContentsMargins(0, 0, 0, 0)
        frameLayout.setAlignment(Qt.AlignTop)
        frame.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        frame.setStyleSheet("""
                                    QFrame 
                                    { 
                                        margin-left: 40px;
                                        margin-right: 40px;
                                        background-color: white;
                                        border-radius: 5px;
                                    }
                                    """)

        monitoringWidget = QWidget()
        monitoringLayout = QHBoxLayout()
        monSwitch = self.getSwitch()
        monSwitch.clicked.connect(self.switchMonitoring)
        monitoringLayout.addWidget(monSwitch)
        monitoringLabel = QLabel()
        monitoringLabel.setText("Monitoring einschalten")
        monitoringLabel.setStyleSheet("""              
                                    QLabel
                                    {
                                        font-size: 18px;
                                        font-family: 'Times New Roman', Times, serif;
                                    }
                                    """)
        monitoringLayout.addWidget(monitoringLabel)
        monitoringWidget.setLayout(monitoringLayout)

        frameLayout.addWidget(monitoringWidget)
        main_layout.addWidget(frame)

        verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        main_layout.addItem(verticalSpacer)


        self.setLayout(main_layout)

        # Set Switch Values
        if self.monitoringActive:
            self.monitoringActive = False
            monSwitch.click()
            # self.__setNotifications(True)


    def getSwitch(self):
        switch = Switch()
        switch.setStyleSheet("Switch { margin-left: 40px;}")
        switch.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        return switch

    def checkMonitoring(self):
        if self.monitoringActive:
            return True
        else:
            return False

    def stopMonitoring(self):
        print('stop')

    def switchMonitoring(self):
        if not self.monitoringActive:
            self.monitoringActive = True
            with open('logs/transfer.txt', 'w') as f:
                f.write('True')
                f.close()
            print('True')
        elif self.monitoringActive:
            self.monitoringActive = False
            with open('logs/transfer.txt', 'w') as f:
                f.write('False')
                f.close()
            print('false')

