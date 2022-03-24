from datetime import datetime, date
import datetime as dt
import pandas as pd

import DBHelper
import ProcessModule

db = DBHelper.DBHelper()
pData = ProcessModule.ProcessData()


class UserData(object):
    class __UserData:
        name = "user1"
        score = 0

    instance = None

    def __new__(cls, *args, **kwargs):
        if not UserData.instance:
            UserData.instance = UserData.__UserData()
        return UserData.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)


class CurrentDayData(object):
    class __CurrentDayData:
        data = db.readData(date.today())

        def updateData(self):

            currData = pData.getData()
            currData.drop_duplicates(subset=['name'], inplace=True)

            if len(self.data) != 0:
                if currData["date"].iloc[0] == self.data["date"].get(0):

                    df = pd.merge(currData["name"], self.data, how="outer", on="name")
                    df.set_index("name", inplace=True)
                    df.update(currData.set_index("name"))
                    df.reset_index(inplace=True)

                    self.data = df

                else:
                    print(2)
                    self.writeData()
                    self.data = currData
            else:
                print(3)
                self.data = currData
                self.writeData()
                self.data = db.readData(date.today())
                return

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


class ReviewData(object):
    class __ReviewData:
        data = []

        def createReview(self):
            currDate = date.today()
            lastSevenDays = [currDate - dt.timedelta(days=x + 1) for x in range(7)]

            for d in lastSevenDays:
                self.data.append(db.readData(d))

            return self.data

    instance = None

    def __new__(cls, *args, **kwargs):
        if not ReviewData.instance:
            ReviewData.instance = ReviewData.__ReviewData()
        return ReviewData.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)