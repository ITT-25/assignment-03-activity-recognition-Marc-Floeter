[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/EppqwQTz)

# Beide Aufgaben:
- venv starten
- requirements aus txt installieren

# 3.1: Gather Data
- python datei starten -> Durchlauf durch alle Aktivitäten mit je 5 Wiederholungen startet
- Aufzeichnung der Daten mit DIPPID Button 1 starten, nach 10s beendet sich die Wiederholung automatisch
- Anweisungen im Terminal beachten
- Speicherort und Dateinamen können per Konstante geregelt werden

# 3.2: Fitness Trainer
- Leider unvollständig aus Zeitmangel!
- Problem: ich habe mich zuletzt bei der Verarbeitung der DIPPID-Sensordaten in while-Schleifen verzettelt, die dann den Programmverlauf blockieren. Ein lösbares Problem, hätte ich noch die Zeit gehabt
- Theoretisch sollte es so funktionieren:
  - fitness_trainer.py starten
  - activity_recognizer.py wird gestartet, liest alle Trainingsdaten ein, startet Vorverarbeitung, trennt nach Trainings- und Testdaten, trainiert das Modell und evaluiert es (Ein Plot dazu öffnet sich, den man erst schließen muss, bevor es weitergeht). Als Features habe ich ganz einfach mean, std, min und max von 1s Zeitfenstern benutzt, was zu einer Accuracy von 98% geführt hat!
  - dippid_reciever.py sollte nach Trainingsstart dauerhaft Daten liefern, die der activity_recognizer vorverarbeitet und predicted, damit fitness_trainer beurteilen kann, ob es die aktuell auszuführende Übung ist, oder nicht. Das hätte dann Punkte geben sollen. Da aber diese Prüfschleifen nicht parallel laufen können und DIPPIDs Sensordaten nicht innerhalb einer Methode aufgerufen werden können, blockiert sich alles gegenseitig.
- pyglet Interface hat es leider noch nicht
- Ich würde euch bitten, euch die Einzelteile anzusehen und in die Mühe, die darin steckt, in die Bewertung einzubeziehen, auch wenn sie nicht zusammenspielen
