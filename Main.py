import GUI
from datetime import datetime, date
import pandas as pd
import numpy as np

import DBHelper
import ProcessModule

db = DBHelper.DBHelper()
pData = ProcessModule.ProcessData()

class UserData:
    name = "user1"
    score = 0


class CurrentDayData(object):
    class __CurrentDayData:
        data = db.readData(date.today())

        def updateData(self):

            currData = pData.getData()
            print(self.data)
            if len(self.data) != 0:
                print(currData["date"], self.data["date"])
                if currData["date"][0] == self.data["date"][0]:
                    print(1)
                    df = pd.merge(currData["name"], self.data, how="outer", on="name")
                    df.set_index("name", inplace=True)
                    df.update(currData.set_index("name"))
                    df.reset_index(inplace=True)

                else:
                    print(2)
                    self.writeData()
                    self.data = currData
            else:
                print(3)
                self.data = currData

            self.writeData()

            return

        def writeData(self):
            for i, row in self.data.iterrows():
                try:
                    db.writeData(row.date, row.runtime, row["name"])
                except Exception as e:
                    print(e)
            return

    instance = None

    def __new__(cls, *args, **kwargs):
        if not CurrentDayData.instance:
            CurrentDayData.instance = CurrentDayData.__CurrentDayData()
        return CurrentDayData.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

class ReviewData:
    data = []

    def createReview(self):
        currDate = datetime.datetime().today()
        lastSevenDays = [currDate - datetime.timedelta(days=x + 1) for x in range(7)]

        for d in lastSevenDays:
            self.data.append(db.readData(d))

        return


if __name__ == "__main__":
    #pData = ProcessModule.ProcessData
    GUI.startWindow()
