import wx
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QPushButton, QWidget, QHBoxLayout, QLabel, QSizePolicy

from gui.OnOffButton import Switch


class NotificationsGUI(QDialog):

    def __init__(self):
        super().__init__()
        self.notificationsAllowed = False
        self.lectureNotifications = False

        # Create a QGridLayout instance
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        # main_layout.addStretch(10)

        # Add widgets to the layout
        notificationWidget = QWidget()
        notificationLayout = QHBoxLayout()
        switch1 = self.getSwitch()
        switch1.clicked.connect(self.switchNotifications)
        notificationLayout.addWidget(switch1)
        notificationLabel = QLabel()
        notificationLabel.setText("Mitteilungen erlauben")
        notificationLayout.addWidget(notificationLabel)
        notificationWidget.setLayout(notificationLayout)
        main_layout.addWidget(notificationWidget)

        lectureWidget = QWidget()
        lectureLayout = QHBoxLayout()
        switch2 = self.getSwitch()
        switch2.clicked.connect(self.switchLectureNotifications)
        lectureLayout.addWidget(switch2)
        lectureLabel = QLabel()
        lectureLabel.setText("Mitteilungen während der Vorlesungszeit ausschalten")
        lectureLayout.addWidget(lectureLabel)
        lectureWidget.setLayout(lectureLayout)
        main_layout.addWidget(lectureWidget)

        self.setLayout(main_layout)

    def getSwitch(self):
        switch = Switch()
        switch.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        return switch

    def switchNotifications(self):
        self.notificationsAllowed = not self.notificationsAllowed
        print(self.notificationsAllowed)

    def switchLectureNotifications(self):
        self.lectureNotifications = not self.lectureNotifications
        print(self.lectureNotifications)

