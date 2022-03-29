"""
This file includes all classes that represent the stored data
"""

from datetime import date
import datetime as dt
import pandas as pd

from classes.DBHelper import DBHelper
import classes.ProcessModule as pm

db = DBHelper()
pData = pm.ProcessData()


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


# stores the process information of the current day
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
                    self.writeData()
                    self.data = currData
            else:
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


# represents the information used in the week review
class ReviewData(object):
    class __ReviewData:
        data = pd.DataFrame()

        def createReview(self):
            currDate = date.today()
            lastSevenDays = [currDate - dt.timedelta(days=x) for x in range(7)]

            for d in lastSevenDays:
                dayData = db.readData(d)
                if not dayData.empty:
                    self.data = pd.concat([self.data, dayData])

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