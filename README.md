# [L]earn

<p style="align:center;"><img src="images/Logo.png" style="width: 25%; height: 25%"></p>

[L]earn ist eine innovative Anwendung um den eigenen Lernfortschritt zu beschleunigen und die Zeitplanung zu verbessern.

## Entwicklersetup
### Ausführung
Zum starten des Prototypen:
  1. Repository forken/klonen
  2. PyCharm (oder andere Python-IDE) installieren
  3. Die folgenden Bibliotheken installieren
      - Pandas
      - psutil
      - PyQT5
      - PyQtWebEngine
      - qroundprogressbar
      - certifi
      - pyautogui
      - pywin32
      - wmctrl (bei Linux über: sudo apt install xprintidle)
      - win32process
      - win32gui
      - attrs
      - pync 
      - xprintidle (bei Linux über: sudo apt install xprintidle)
 
## Doku
Doku ist in Form von Kommentaren im Code zu finden.

## Coding Richtlinien
- Nie auf dem main Branch arbeiten, immer einen separaten Branch nutzen 
- Branches sinnvolle Namen geben 
- Für jede Task/Arbeitspaket einen Branch erstellen 
- Nach dem Push einen Pull Request erstellen und nach der Vorstellung im Meeting den eigenen Branch auf den main Branch mergen. Anschließend den eigenen Branch im Remote-Repository löschen 
- Bei Arbeitsbeginn am Code zuerst aktuellen Stand pullen 
- Namensregularien: 
  - Codesprache: Englisch 
  - CamelCase: Variablen und Funktionen lowerCamelCase; Klassen und Files: UpperCamelCase 
  - Files, Klassen, Funktionen und Variablen aussagekräftig benennen, Ausnahme: Zählvariablen (in Schleifen u.ä.) 
- Clean Code:  
<br>  Darauf achten, wiederkehrenden bzw. öfter genutzten Code in granulare Funktionen auszulagern 
- Sobald Codezeile länger als Sichtfeld wird à Zeilenumbruch 
- Einrückungen gemäß der Python-Regularien machen und regelmäßig mit Codelayout-Funktion der IDE überprüfen 
- Nach funktions- und sinnmäßig zusammenhängenden Codeblöcken, Funktionen, Klassen und Konstrukten (Schleifen, If-Else, etc.) eine Leerzeile einfügen 
- Python-Files, Klassen und Funktionen mit kurzem, vorangestelltem Kommentar erklären, sonst Kommentare dort einfügen, wo als sinnvoll erachtet, aber selbsterklärend nicht vor jede einzelne Codezeile 
