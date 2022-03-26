import time
from urllib.error import URLError

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QBrush, QColor, QPalette

from qroundprogressbar import QRoundProgressBar

from Defaults import Defaults
from LecturePlan import LecturePlan

DEF_LECTUREPLANURL = "LecturePlanURL"


class LecturePlanGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.loadedWebsite = False

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignTop)

        # -----------------
        # First Side
        self.nameLabel = QLabel()
        self.nameLabel.setText('Vorlesungsplanurl:')
        self.line = QLineEdit()

        self.pybutton = QPushButton('Verbinden')
        self.pybutton.clicked.connect(self.setLecturePlan)

        # Add Widgets
        main_layout.addWidget(self.nameLabel)
        main_layout.addWidget(self.line)
        main_layout.addWidget(self.pybutton)

        # -----------------
        # Second Side
        self.webView = QWebEngineView()
        self.webView.loadStarted.connect(self.loadStartedHandler)
        self.webView.loadProgress.connect(self.loadProgressHandler)
        self.webView.loadFinished.connect(self.loadFinishedHandler)

        self.pybutton2 = QPushButton('Neu Verbinden')
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
        main_layout.addWidget(self.webView)
        main_layout.addWidget(self.pybutton2)
        main_layout.addWidget(self.progressWidget)

        # -----------------
        # Set Side
        self.setLayout(main_layout)

        url = Defaults().get(DEF_LECTUREPLANURL)
        if url != "":
            self.webView.setUrl(QUrl(url))
        else:
            self.setFirstSide()

    def setFirstSide(self):
        self.loadedWebsite = False

        self.hideAll()

        self.nameLabel.setHidden(False)
        self.line.setHidden(False)
        self.pybutton.setHidden(False)

    def setSecondSide(self):
        self.hideAll()

        self.webView.setHidden(False)
        self.pybutton2.setHidden(False)

    def setLecturePlan(self):
        url = self.line.text()
        if "vorlesungsplan.dhbw-mannheim.de" in url:
            # remove date parameter
            dateIndex = url.find("date=")
            if dateIndex != -1:
                url = url[0:dateIndex-1]
                print(url)

            try:
                lecturePlan = LecturePlan(url).getLP()

                if len(lecturePlan) > 0:
                    Defaults().set(DEF_LECTUREPLANURL, url)
                    self.webView.setUrl(QUrl(url))

            except (URLError, ValueError) as e:
                print(e)
                print(url)

    def hideAll(self):
        for i in range(self.layout().count()):
            self.layout().itemAt(i).widget().hide()

    def loadStartedHandler(self):
        if not self.loadedWebsite:
            self.hideAll()
            self.progressWidget.setHidden(False)

    def loadProgressHandler(self, prog):
        if not self.loadedWebsite:
            self.progress.setValue(prog)

    def loadFinishedHandler(self):
        if not self.loadedWebsite:
            self.loadedWebsite = True
            self.setSecondSide()
