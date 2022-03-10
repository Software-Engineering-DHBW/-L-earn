import GUI
import datetime
import pandas as pd


class UserData:
    name = "user1"
    score = 0


class CurrentDayData:
    data = "hier aus db auslesen"

    def updateData(self):
        """
        currData = ProcessData().data

        if currData["date"][0] == self.data["date"][0]:

            df = pd.merge(cD["name"], df, how="outer", on="name")
            df.set_index("name", inplace=True)
            df.update(cD.set_index("name"))
            df.reset_index(inplace=True)

        else:
            writeData()
            self.data = currData

        self.writeData()
        """
        return

    def writeData(self):
        # write data to DB
        return


class ReviewData:
    data = "read data from DB"

    def createReview(self):
        """
        currDate = datetime.datetime().today()
        lastSevenDays = [currDate - datetime.timedelta(days = x+1) for x in range(7)

        self.data = "Hier mit lastSevenDays aus DB auslesen"
        """
        return


if __name__ == "__main__":
    GUI.startWindow()

