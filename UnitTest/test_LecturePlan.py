import os
from datetime import datetime
from unittest import TestCase
from urllib.error import URLError

from LecturePlan import LecturePlan
from defaults.Defaults import Defaults
from defaults.Values import DEF_LECTUREPLANURL


class TestLecturePlan(TestCase):
    def test_readLecturePlan(self):
        defaults = Defaults(filename="../defaults/defaults.pkl")

        url = "https://vorlesungsplan.dhbw-mannheim.de/index.php?action=view&gid=3067001&uid=7761001&date=1646002800" \
              "&view=month "
        print("InitUrl: ", url)
        if "vorlesungsplan.dhbw-mannheim.de" in url:
            # remove date parameter
            dateIndex = url.find("date=")
            if dateIndex != -1:
                url = url[0:dateIndex-1]

            try:
                lecturePlan = LecturePlan(url).getLP()

                if len(lecturePlan) > 0:
                    defaults.set(DEF_LECTUREPLANURL, url)

            except (URLError, ValueError) as e:
                print(e)
                print(url)

        url = defaults.get(DEF_LECTUREPLANURL)
        print("Changed Url: ", url)

        lecturePlan = LecturePlan(url).getStartBeginLP()
        print("LecturePlan:")
        print(lecturePlan)

        print("Timers:")
        for index, row in lecturePlan.iterrows():
            now = datetime.now()

            # Add Timer for begin
            begin = row["date"] + " " + row["begin"]
            beginDatetime = datetime.strptime(begin, "%d.%m.%Y %H:%M")
            difference = beginDatetime - now
            print("begin: " + begin + " -> starts in ", difference)

            # Add Timer for end
            end = row["date"] + " " + row["end"]
            endDatetime = datetime.strptime(end, "%d.%m.%Y %H:%M")
            difference = endDatetime - now
            print("end: " + end + " -> starts in ", difference)
