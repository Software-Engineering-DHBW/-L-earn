# [L]earn
[L]earn ist eine innovative Anwendung um den eigenen Lernfortschritt zu beschleunigen und die Zeitplanung zu verbessern.

## Prototyp
### Ausführung
Zum starten des Prototypen:
  1. Pycharm installieren
  2. Die folgenden Bibliotheken installieren
      - Pandas
      - psutil
      - PyQT5
  3. Main.py ausführen

### Doku
Main.py: Zum Starten des Programms <br>
GUI.py: Beinhaltet die Implementierung der Grafischen Oberfläche <br>
UserInterface.ui: Vom Designer kreierte Daten für die GUI <br>
ProcessModule.py: Beinhaltet die Implementierung aller Funktionen zu Prozessen und dem Prozess-Handling

Weitere Doku ist in Form von Kommentaren im Code zu finden.

## Coding Richtlinien
- Nie auf dem main Branch arbeiten, immer einen separaten Branch nutzen
- Branches sinnvolle Namen geben
- Nach dem Push den eigenen Branch über einen Pull Request auf den main Branch mergen
- Namensregularien:
  1. Codesprache: Englisch
  2. CamelCase: Variablen und Funktionen lowerCamelCase; Klassen und Files: UpperCamelCase
  3. Files, Klassen, Funktionen und Variablen aussagekräftig benennen, Ausnahme: Zählvariablen (in Schleifen u.ä.)
- Clean Code: <br>
  Darauf achten, wiederkehrenden bzw. öfter genutzten Code in granulare Funktionen umzuwandeln
