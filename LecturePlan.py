"""
Automatically reads out a DHBW lecture plan and stores it in a LecturePlan object
"""
from datetime import datetime
import ssl
from urllib.request import urlopen

import certifi
import pandas as pd


def lecturePlanData(url):
    page = urlopen(url, context=ssl.create_default_context(cafile=certifi.where()))
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    index = html.find(
        '<li data-role="list-divider">')  # find start and end index of the calendar data by given dividers
    index = index + len('<li data-role="list-divider">')
    end = html.find('<div class="footer-txt-l">')
    list = html[index:end]
    x = list.split('<li data-role="list-divider">')  # split to get the single days of the week
    p = []
    for i in x:  # iterate over all days
        ind = i.find('</li><li class="">')
        dayDate = i[:ind]
        inde = ind + len('</li><li class="">')
        lects = i[inde:]  # extract days and lectures

        if '<' in dayDate:
            r = dayDate.find('<')
            dayDate = dayDate[:r]
            p.append(dayDate)
            continue
        dayDate = dayDate.split(',')
        lects = lects.split("</li>")  # split single lectures
        for lect in lects:
            temp = dayDate.copy()
            split = lect.split('</div>')
            content = []
            for s in split:
                if "cal" not in s:
                    continue
                if '<li class="">' in s:
                    index2 = s.find('<li class="">') + len('<li class="">')
                    s = s[index2:]
                i2 = s.find('cal')
                end2 = s.find('>')
                info = s[i2:end2 - 1] + ':' + s[end2 + 1:]
                content.append(info)
            if len(content) == 0:
                continue
            temp.extend(content)
            p.append(temp)
    return p


class LecturePlan:

    def __init__(self, url):
        self.lecturePlanArray = lecturePlanData(url)

    def printLP(self):
        print(self.lecturePlanArray)

    def getLP(self):
        return self.lecturePlanArray

    def getStartBeginLP(self):
        dfLecture = pd.DataFrame(columns=["date", "begin", "end"])
        index = 0
        for lecture in self.lecturePlanArray:
            if isinstance(lecture, list):
                today = datetime.now()
                date = lecture[1].strip() + "." + str(today.year)
                time = lecture[2]
                time = remove_prefix(time, "cal-time:")
                timeArr = time.split("-")
                begin = timeArr[0]
                end = timeArr[1]
                act = datetime.strptime(date + " " + end, "%d.%m.%Y %H:%M")
                if act >= today:
                    new_row = pd.DataFrame({'date': date, 'begin': begin, 'end': end}, index=[index])
                    dfLecture = pd.concat([dfLecture, new_row])
                    index += 1
        return dfLecture


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


if __name__ == "__main__":
    lp = LecturePlan("https://vorlesungsplan.dhbw-mannheim.de/index.php?action=view&gid=3067001&uid=7761001")
    lp.printLP()
    print(lp.getLP())
