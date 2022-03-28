from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QLabel, QHBoxLayout, QFrame, QScrollArea
import datetime

import DataClasses


class WeekReview(QDialog):

    def __init__(self):
        super().__init__()

        self.setupUi()

    def setupUi(self):

        mainLayout = QVBoxLayout(self)

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #eeeeee;'
                           'border-radius: 5px;')

        # title
        titleLabel = QLabel("Wochenrückblick")
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
                                 "color: black;}")
        mainLayout.addWidget(titleLabel)

        # review
        # create frame for all time bars
        reviewFrame = QFrame()
        frameLayout = QVBoxLayout(reviewFrame)
        reviewFrame.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        reviewFrame.setStyleSheet("QFrame {"
                                  "background-color: white;"
                                  "border-radius: 5px}")
        self.createReviewBars(frameLayout)

        # put frame inside scrollable area
        scrollArea = QScrollArea()
        scrollArea.setWidget(reviewFrame)
        scrollArea.setWidgetResizable(True)
        scrollArea.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        scrollArea.setStyleSheet("""
                                QScrollArea 
                                {
                                    margin-left: 40px;
                                    margin-right: 40px;
                                    min-height: 485px;
                                    background-color: white;
                                }
                                QScrollBar:vertical
                                {
                                    background-color: white;
                                    width: 9px;
                                    border-radius: 5px;
                                }
                            
                                QScrollBar::handle:vertical
                                {
                                    background-color: #d6d6d6;
                                    border-radius: 5px;
                                }
                            
                                QScrollBar::sub-line:vertical
                                {
                                    margin: 3px 0px 3px 0px;
                                    border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
                                    height: 10px;
                                    width: 10px;
                                    subcontrol-position: top;
                                    subcontrol-origin: margin;
                                }
                            
                                QScrollBar::add-line:vertical
                                {
                                    margin: 3px 0px 3px 0px;
                                    border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
                                    height: 10px;
                                    width: 10px;
                                    subcontrol-position: bottom;
                                    subcontrol-origin: margin;
                                }
                            
                                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
                                {
                                    background: none;
                                }
                            
                                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
                                {
                                    background: none;
                                }""")
        mainLayout.addWidget(scrollArea)

        verticalSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        mainLayout.addItem(verticalSpacer)

    def createReviewBars(self, layout):

        data = DataClasses.ReviewData().createReview()

        # print message if there is no review data yet
        if data.empty:
            msgLabel = QLabel("Es gibt bisher leider nicht genug Daten um einen Rückblick zu erstellen!")
            msgLabel.setStyleSheet("QLabel{"
                                   "text-align: Center;"
                                   "color: black;}")
            msgLabel.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(msgLabel)
            return

        # merge data from all dates
        data.drop(['date'], axis=1, inplace=True)
        data = data.groupby(data['name']).aggregate({'runtime': 'sum'})
        data.sort_values(by=['runtime'], ascending=False, inplace=True)

        i = 0
        for name, row in data.iterrows():

            if i == 0:
                maxVal = row.runtime
            i += 1

            # create the string for the runtime of each process
            barTime = ""
            runtime = (datetime.timedelta(seconds=round(row.runtime)))
            if runtime.days != 0:
                barTime += str(runtime.days) + "d " + str(runtime.seconds // 3600) + "h " + str(
                    (runtime.seconds // 60) % 60) + "min"
            elif (runtime.seconds // 3600) != 0:
                barTime += str(runtime.seconds // 3600) + "h " + str((runtime.seconds // 60) % 60) + "min"
            elif ((runtime.seconds // 60) % 60) != 0:
                barTime += str((runtime.seconds // 60) % 60) + "min"
            else:
                return

            barText = "     " + name

            barBox = QFrame()
            barLayout = QHBoxLayout(barBox)
            barLayout.setSpacing(0)
            barLayout.setContentsMargins(0, 0, 0, 0)
            barBox.setAttribute(QtCore.Qt.WA_StyledBackground, True)
            barBox.setStyleSheet('background-color: white;')

            # create progress bar
            bar = QProgressBar()
            bar.setMinimum(0)
            bar.setMaximum(maxVal)
            bar.setValue(row.runtime)
            bar.setFormat(barText)
            bar.setAlignment(QtCore.Qt.AlignLeft)
            bar.setStyleSheet("QProgressBar {"
                              " border-radius: 5px;"
                              " text-align: left;"
                              " font-size: 18px;"
                              " font-family: 'Times New Roman', Times, serif;"
                              " color: black;"
                              " T min-height: 35px;}"
                              " QProgressBar::chunk {"
                              " background-color: #d6d6d6;"
                              " border-radius: 5px;}")

            timeLabel = QLabel(barTime)
            timeLabel.setAlignment(QtCore.Qt.AlignRight)
            timeLabel.setStyleSheet("QLabel{"
                                    "text-align: right;"
                                    "color: black;"
                                    "font-size: 18px;"
                                    "min-width: 100px;"
                                    "font-family: 'Times New Roman', Times, serif;}")
            barLayout.addWidget(bar)
            barLayout.addWidget(timeLabel)

            layout.addWidget(barBox)
