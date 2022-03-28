import threading
from datetime import datetime
from urllib.error import URLError

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QSizePolicy

from defaults.Defaults import Defaults
from LecturePlan import LecturePlan
from Notifications import Notifications
from defaults.Values import DEF_NOTIFICATIONSALLOWED, DEF_LECTUREPLANURL, DEF_LECTURENOTIFICATIONS
from gui.OnOffButton import Switch


class NotificationsGUI(QDialog):

    def __init__(self):
        super().__init__()

        # Set Variables
        self.timers = []

        value = Defaults().get(DEF_NOTIFICATIONSALLOWED)
        if value != "":
            self.notificationsAllowed = value
        else:
            self.notificationsAllowed = True

        value = Defaults().get(DEF_LECTURENOTIFICATIONS)
        if value != "":
            self.lectureNotifications = value
        else:
            self.lectureNotifications = False

        # Create a QGridLayout instance
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Add widgets to the layout
        notificationWidget = QWidget()
        notificationLayout = QHBoxLayout()
        ntfSwitch = self.getSwitch()
        ntfSwitch.clicked.connect(self.switchNotifications)
        notificationLayout.addWidget(ntfSwitch)
        notificationLabel = QLabel()
        notificationLabel.setText("Mitteilungen erlauben")
        notificationLayout.addWidget(notificationLabel)
        notificationWidget.setLayout(notificationLayout)
        main_layout.addWidget(notificationWidget)

        lectureWidget = QWidget()
        lectureLayout = QHBoxLayout()
        lectureSwitch = self.getSwitch()
        lectureSwitch.clicked.connect(self.switchLectureNotifications)
        lectureLayout.addWidget(lectureSwitch)
        lectureLabel = QLabel()
        lectureLabel.setText("Mitteilungen während der Vorlesungszeit ausschalten")
        lectureLayout.addWidget(lectureLabel)
        lectureWidget.setLayout(lectureLayout)
        main_layout.addWidget(lectureWidget)

        self.setLayout(main_layout)

        # Set Switch Values
        if self.notificationsAllowed:
            self.notificationsAllowed = False
            ntfSwitch.click()
            # self.__setNotifications(True)

        if self.lectureNotifications:
            lectureSwitch.click()

        # init timers for lectures
        url = Defaults().get(DEF_LECTUREPLANURL)
        self.initTimers(url)

    def getSwitch(self):
        switch = Switch()
        switch.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        return switch

    def switchNotifications(self):
        self.__setNotifications(not self.notificationsAllowed)

    def __setNotifications(self, notificationsAllowed):
        self.notificationsAllowed = notificationsAllowed
        Defaults().set(DEF_NOTIFICATIONSALLOWED, notificationsAllowed)
        if notificationsAllowed:
            Notifications().enableNtf()
        else:
            Notifications().disableNtf()

    def switchLectureNotifications(self):
        self.lectureNotifications = not self.lectureNotifications
        Defaults().set(DEF_LECTURENOTIFICATIONS, self.lectureNotifications)

    def initTimers(self, url):
        if url != "":
            try:
                lecturePlan = LecturePlan(url).getStartBeginLP()
                print(lecturePlan)
                self.timers = []
                i = 0
                for index, row in lecturePlan.iterrows():
                    now = datetime.now()

                    # Add Timer for begin
                    begin = row["date"] + " " + row["begin"]
                    beginDatetime = datetime.strptime(begin, "%d.%m.%Y %H:%M")
                    difference = beginDatetime-now
                    self.timers.append(threading.Timer(difference.seconds, self.startLecture))
                    self.timers[i].start()
                    i += 1
                    print(begin)

                    # Add Timer for end
                    end = row["date"] + " " + row["end"]
                    endDatetime = datetime.strptime(end, "%d.%m.%Y %H:%M")
                    difference = endDatetime-now
                    self.timers.append(threading.Timer(difference.seconds, self.endLecture))
                    self.timers[i].start()
                    i += 1
                    print(end)

            except (URLError, ValueError) as e:
                print(e)
                print(url)

    def startLecture(self):
        if self.lectureNotifications:
            Notifications().disableNtf()

    def endLecture(self):
        if self.notificationsAllowed:
            Notifications().enableNtf()


