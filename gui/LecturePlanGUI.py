"""
GUI for the Lecture Plan tab
"""
from urllib.error import URLError

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QBrush, QColor, QPalette
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame
from qroundprogressbar import QRoundProgressBar

from classes.LecturePlan import LecturePlan
from defaults.Defaults import Defaults
from defaults.Values import DEF_LECTUREPLANURL
from gui.NotificationsGUI import NotificationsGUI


class LecturePlanGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.loadedWebsite = False

        mainLayout = QVBoxLayout()

        # -----------------
        # First Side
        self.firstWidget = QWidget()
        firstLayout = QVBoxLayout(self)
        firstLayout.setAlignment(Qt.AlignTop)

        titleLabel = QLabel("Vorlesungsplan")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setMaximumHeight(80)
        titleLabel.setMinimumHeight(80)
        titleLabel.setObjectName("titleLecture")
        firstLayout.addWidget(titleLabel)

        frame = QFrame()
        frameLayout = QVBoxLayout(frame)
        frameLayout.setAlignment(Qt.AlignTop)
        frame.setAttribute(Qt.WA_StyledBackground, True)
        frame.setObjectName("lectureFrame")

        nameLabel = QLabel()
        nameLabel.setText('Vorlesungsplanurl:')
        nameLabel.setObjectName("label")
        self.line = QLineEdit()

        pybutton = QPushButton('Verbinden')
        pybutton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        pybutton.clicked.connect(self.setLecturePlan)

        # Add Widgets
        frameLayout.addWidget(nameLabel)
        frameLayout.addWidget(self.line)
        frameLayout.addWidget(pybutton)

        frame.setLayout(frameLayout)
        firstLayout.addWidget(frame)

        self.firstWidget.setLayout(firstLayout)
        mainLayout.addWidget(self.firstWidget)

        # -----------------
        # Second Side
        self.webView = QWebEngineView()
        self.webView.loadStarted.connect(self.loadStartedHandler)
        self.webView.loadProgress.connect(self.loadProgressHandler)
        self.webView.loadFinished.connect(self.loadFinishedHandler)

        self.pybutton2 = QPushButton('Neu Verbinden')
        self.pybutton2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.pybutton2.clicked.connect(self.setFirstSide)

        # ProgressBar
        self.progressWidget = QWidget()
        progressLayout = QHBoxLayout()
        progressLayout.setAlignment(Qt.AlignCenter)

        self.progress = QRoundProgressBar()
        self.progress.setBarStyle(QRoundProgressBar.BarStyle.DONUT)

        # style accordingly via palette
        palette = QPalette()
        brush = QBrush(QColor(244, 0, 27))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)

        self.progress.setPalette(palette)
        self.progress.setFixedSize(50, 50)

        progressLayout.addWidget(self.progress)
        self.progressWidget.setLayout(progressLayout)

        # Add Widgets
        mainLayout.addWidget(self.webView)
        mainLayout.addWidget(self.pybutton2)
        mainLayout.addWidget(self.progressWidget)

        # -----------------
        # Set Side
        self.setLayout(mainLayout)

        url = Defaults().get(DEF_LECTUREPLANURL)
        if url != "":
            self.webView.setUrl(QUrl(url))
        else:
            self.setFirstSide()

    def setFirstSide(self):
        self.loadedWebsite = False

        self.hideAll()

        self.firstWidget.setHidden(False)

    def setSecondSide(self):
        self.hideAll()

        self.webView.setHidden(False)
        self.pybutton2.setHidden(False)

    def setLecturePlan(self):
        url = self.line.text()

        # check if it is a valid url
        if "vorlesungsplan.dhbw-mannheim.de" in url:
            # remove date parameter
            dateIndex = url.find("date=")
            if dateIndex != -1:
                url = url[0:dateIndex-1]

            try:
                # save url in defaults if the lecturePlan could be read
                lecturePlan = LecturePlan(url).getLP()

                if len(lecturePlan) > 0:
                    Defaults().set(DEF_LECTUREPLANURL, url)
                    # set webView
                    self.webView.setUrl(QUrl(url))
                    # init timers for the lectures
                    NotificationsGUI().initTimers(url)

            except (URLError, ValueError) as e:
                print(e)
                print(url)

    def hideAll(self):
        for i in range(self.layout().count()):
            self.layout().itemAt(i).widget().hide()

    def loadStartedHandler(self):
        # show progress widget while website is loading
        if not self.loadedWebsite:
            self.hideAll()
            self.progressWidget.setHidden(False)

    def loadProgressHandler(self, prog):
        # set progress while website is loading
        if not self.loadedWebsite:
            self.progress.setValue(prog)

    def loadFinishedHandler(self):
        # show webView
        if not self.loadedWebsite:
            self.loadedWebsite = True
            self.setSecondSide()
