from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QWidget, QComboBox, QSizePolicy

from gui.OnOffButton import Switch


class LimitsGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.columns = ['name', 'limit']
        self.banned = []

        self.timers = []

        # Create a QGridLayout instance
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        # main_layout.addStretch(10)

        # Add widgets to the layout
        limitsWidget = QWidget()
        limitsLayout = QHBoxLayout()
        limitsLayout.setAlignment(Qt.AlignLeft)

        limitsLabel = QLabel()
        limitsLabel.setText("Limit setzen für")
        limitsLabel.setFont()
        limitsLabel.adjustSize()
        limitsLayout.addWidget(limitsLabel)

        combo = QComboBox(self)
        combo.addItem("Steam")
        combo.addItem("Valorant")
        #combo.addItem("")
        combo.activated[str].connect(self.onChanged)
        limitsLayout.addWidget(combo)



        limitsWidget.setLayout(limitsLayout)
        main_layout.addWidget(limitsWidget)

        self.setLayout(main_layout)



    def onChanged(self, text):
        print(text)



