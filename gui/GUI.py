"""
Includes the functionality to run the graphical user interface
"""
import sys

from PyQt5.QtGui import QIcon, QPixmap, QFontDatabase
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QTabWidget, \
    QMainWindow
from PyQt5.QtCore import QThread, QSize, Qt

from Worker import Worker


# class that represents the main GUI window
from gui.ActivityMonitorGUI import ActivityMonitorGUI
from gui.LecturePlanGUI import LecturePlanGUI
from gui.NotificationsGUI import NotificationsGUI
from gui.WeekReview import WeekReview
from gui.LimitsGUI import LimitsGUI


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.worker = None
        self.thread = None
        self.worker2 = None
        self.thread2 = None
        self.worker3 = None
        self.thread3 = None

        # set the title of main window
        self.setWindowTitle('[L]earn')
        self.setWindowIcon(QIcon('images/Logo.png'))

        # set the size of window
        self.Width = 1000
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.btn_1 = self.getButton(image='diagram.png', text='Wochenrückblick')
        self.btn_2 = self.getButton(image='dhbw.png', text='Vorlesungsplan')
        self.btn_3 = self.getButton(image='stopwatch.png', text='Limits')
        self.btn_4 = self.getButton(image='notification.png', text='Mitteilungen')
        self.btn_5 = self.getButton(image='activityMonitor.png', text='Activity Monitor')

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)
        self.btn_5.clicked.connect(self.button5)

        self.right_widget = None

        # add tabs
        self.weekReview = WeekReview()
        self.lecturePlan = LecturePlanGUI()
        self.limits = LimitsGUI()
        self.notifications = NotificationsGUI()
        self.activityMonitor = ActivityMonitorGUI()

        self.tab1 = self.weekReview
        self.tab2 = self.lecturePlan
        self.tab3 = self.limits
        self.tab4 = self.notifications
        self.tab5 = self.activityMonitor

        self.initUI()

        # create Threads
        #self.createProcessThread()
        self.createProcessThread2()
        self.createProcessThread3()

    # function to create a thread, which updates the process table
    def createProcessThread(self):
        self.thread = QThread()
        self.worker = Worker(self.weekReview)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.loadProcesses)
        self.thread.start()

    def createProcessThread2(self):
        self.thread2 = QThread()
        self.worker2 = Worker(self.weekReview)
        self.worker2.moveToThread(self.thread2)
        self.thread2.started.connect(self.worker2.updateProcessData)
        self.thread2.start()

    def createProcessThread3(self):
        self.thread3 = QThread()
        self.worker3 = Worker(self.weekReview)
        self.worker3.moveToThread(self.thread3)
        self.thread3.started.connect(self.worker3.updateCurrentDayData)
        self.thread3.start()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addWidget(self.btn_5)
        left_layout.addStretch(40)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')
        self.right_widget.addTab(self.tab5, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setDocumentMode(True)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none; border-radius: 5px;}
            QTabBar::pane { border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # -----------------
    # buttons
    def getButton(self, image, text):
        button = QPushButton(text, self)
        button.setIcon(QIcon(QPixmap("images/" + image)))
        button.setStyleSheet("QPushButton { text-align: left;"
                             "padding-left: 10px;"
                             "border-radius: 5px;"
                             "background-color: white;"
                             "min-height: 30px;"
                             "min-width: 150px;}")
        font = button.font()
        font.setPointSize(13)
        button.setFont(font)
        button.setIconSize(QSize(20, 20))
        return button

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)

    def button5(self):
        self.right_widget.setCurrentIndex(4)


def startWindow():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
