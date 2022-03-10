"""
Automatically reads out a DHBW lecture plan and stores it in a LecturePlan object
"""
from urllib.request import urlopen

def lecturePlanData(url):
    page = urlopen(url)
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
        lects = lects.split("</li>")    # split single lectures
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

class LecturePlan():

    def __init__(self, url):
        self.lecturePlanArray = lecturePlanData(url)

    def printLP(self):
        print(self.lecturePlanArray)

    def getLP(self):
        return self.lecturePlanArray


if __name__ == "__main__":
    lp = LecturePlan("https://vorlesungsplan.dhbw-mannheim.de/index.php?action=view&gid=3067001&uid=7761001")
    lp.printLP()
    print(lp.getLP())

