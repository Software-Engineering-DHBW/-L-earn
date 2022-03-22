from gui import GUI

import DBHelper
import ProcessModule


class UserData:
    name = "user1"
    score = 0


class CurrentDayData:
    global db
    data = db.readData(datetime.datetime.date())

    def updateData(self):

        currData = pData.data

        if currData["date"][0] == self.data["date"][0]:

            df = pd.merge(currData["name"], self.data, how="outer", on="name")
            df.set_index("name", inplace=True)
            df.update(currData.set_index("name"))
            df.reset_index(inplace=True)

        else:
            self.writeData()
            self.data = currData

        self.writeData()

        return

    def writeData(self):
        for p in self.data:
            db.writeData(p.date, p.time, p.name)
        return


class ReviewData:
    data = []

    def createReview(self):
        currDate = datetime.datetime().today()
        lastSevenDays = [currDate - datetime.timedelta(days = x+1) for x in range(7)]

        for d in lastSevenDays:
            self.data.append(db.readData(d))

        return


if __name__ == "__main__":

    db = DBHelper.DBHelper()
    pData = ProcessModule.ProcessData
    GUI.startWindow()
