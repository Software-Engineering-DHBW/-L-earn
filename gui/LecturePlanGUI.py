import time
from urllib.error import URLError

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QBrush, QColor, QPalette

from qroundprogressbar import QRoundProgressBar

from Defaults import Defaults
from LecturePlan import LecturePlan

DEF_LECTUREPLANURL = "LecturePlanURL"


class LecturePlanGUI(QWidget):

    def __init__(self):
        super().__init__()

        # -----------------
        # First Side
        self.nameLabel = QLabel()
        self.nameLabel.setText('Vorlesungsplanurl:')
        self.line = QLineEdit()

        # self.line.move(150, 10)
        # self.line.resize(300, 20)
        # self.nameLabel.move(20, 20)

        self.pybutton = QPushButton('Verbinden')
        self.pybutton.clicked.connect(self.setLecturePlan)
        # self.pybutton.resize(200, 32)
        # self.pybutton.move(80, 60)

        # -----------------
        # Second Side
        self.webView = QWebEngineView()
        self.webView.loadStarted.connect(self.loadStartedHandler)
        self.webView.loadProgress.connect(self.loadProgressHandler)
        self.webView.loadFinished.connect(self.loadFinishedHandler)

        self.progress = QRoundProgressBar()

        # -----------------
        # Set Side
        url = Defaults().get(DEF_LECTUREPLANURL)
        if url != "":
            self.webView.setUrl(QUrl(url))
        else:
            self.setFirstSide()

    def setFirstSide(self):
        if self.layout() is not None:
            QWidget().setLayout(self.layout())
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.nameLabel)
        main_layout.addWidget(self.line)
        main_layout.addWidget(self.pybutton)
        main_layout.addStretch(5)
        self.setLayout(main_layout)

    def setSecondSide(self):
        if self.layout() is not None:
            QWidget().setLayout(self.layout())
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.webView)
        self.setLayout(main_layout)

    def setLecturePlan(self):
        url = self.line.text()
        try:
            lecturePlan = LecturePlan(url).getLP()

            if len(lecturePlan) > 0:
                Defaults().set(DEF_LECTUREPLANURL, url)
                self.webView.setUrl(QUrl(url))

        except URLError as e:
            print(e)
            print(url)

    def loadStartedHandler(self):
        try:
            if self.layout() is not None:
                QWidget().setLayout(self.layout())

            self.progress.setBarStyle(QRoundProgressBar.BarStyle.DONUT)

            # style accordingly via palette
            palette = QPalette()
            brush = QBrush(QColor(244, 0, 27))
            brush.setStyle(Qt.SolidPattern)
            palette.setBrush(QPalette.Active, QPalette.Highlight, brush)

            self.progress.setPalette(palette)
            self.progress.setFixedSize(50, 50)

            main_layout = QVBoxLayout(self)
            main_layout.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(self.progress)
            self.setLayout(main_layout)
        except Exception as e:
            print(e)

    def loadProgressHandler(self, prog):
        self.progress.setValue(prog)

    def loadFinishedHandler(self):
        self.setSecondSide()
