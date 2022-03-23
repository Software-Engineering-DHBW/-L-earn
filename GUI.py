"""
Includes the functionality to run the graphical user interface
"""
import sys

from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QTabWidget, \
    QMainWindow
from PyQt5.QtCore import QObject, QThread, QSize
from PyQt5.uic import loadUi

from Worker import Worker


# class that represents the main GUI window
class MainWindow(QMainWindow):

    def __init__(self):
        # super(MainWindow, self).__init__()
        super().__init__()
        self.worker = None
        self.thread = None

        """# load UI from file
        loadUi("UserInterface.ui", self)

        # init table
        self.tableWidget.setColumnWidth(0, 200)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)

        # init start button
        self.pushButton.setToolTip("This button starts the [L]earn session.")

        # init stop button
        self.pushButton_2.setToolTip("This button stops the [L]earn session.")"""

        self.createProcessThread()

        # set the title of main window
        self.setWindowTitle('[L]earn')

        # set the size of window
        self.Width = 1000
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.btn_1 = self.getButton(image='hourglass.png', text='Wochenrückblick')
        self.btn_2 = self.getButton(image='dhbw.png', text='Vorlesungsplan')
        self.btn_3 = self.getButton(image='stopwatch.png', text='Limits')
        self.btn_4 = self.getButton(image='notification.png', text='Mitteilungen')

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()

        self.initUI()

    # function to create a thread, which updates the process table
    def createProcessThread(self):
        self.thread = QThread()
        self.worker = Worker(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.loadProcesses)
        self.thread.start()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
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

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

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
        button.setStyleSheet("QPushButton { text-align: left; }")
        font = button.font()
        font.setPointSize(16)
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

    # -----------------
    # pages

    def ui1(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 1'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 2'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 3'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 4'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main


def startWindow():
    app = QApplication(sys.argv)
    # global window
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
