from urllib.error import URLError

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout

from Defaults import Defaults
from LecturePlan import LecturePlan


class LecturePlanGUI(QWidget):

    def __init__(self):
        super().__init__()

        # -----------------
        # First Side
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Vorlesungsplanurl:')
        self.line = QLineEdit(self)

        self.line.move(150, 10)
        self.line.resize(300, 20)
        self.nameLabel.move(20, 20)

        self.pybutton = QPushButton('Verbinden', self)
        self.pybutton.clicked.connect(self.setLecturePlan)
        self.pybutton.resize(200, 32)
        self.pybutton.move(80, 60)

        self.setFirstSide()

        # -----------------
        # Second Side
        self.webView = QWebEngineView()

    def setFirstSide(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.nameLabel)
        main_layout.addWidget(self.pybutton)
        main_layout.addStretch(5)
        self.setLayout(main_layout)

    def setSecondSide(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.webView)
        main_layout.addStretch(5)
        self.setLayout(main_layout)

    def setLecturePlan(self):
        url = self.line.text()
        try:
            lecturePlan = LecturePlan(url).getLP()

            if len(lecturePlan) > 0:
                defaults = Defaults()
                defaults.set("LecturePlanURL", url)
                self.setSecondSide()
                self.webView.setUrl(QUrl(url))

        except URLError as e:
            print(e)
