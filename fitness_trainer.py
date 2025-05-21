# this program visualizes activities with pyglet

import random
import activity_recognizer, dippid_reciever
import pyglet

ACTIVITIES = ["jumpingjack", "lifting", "rowing", "running"]
ROUND_TIME = 10
current_activity = None

def main():
    choose_activity()
    print("Hallo Sportskanone! Bereit für ein paar Übungen?")
    print(f'Starte deine erste Runde {current_activity} mit Button 1 und mache die Übung für {ROUND_TIME} Sekunden!')

def choose_activity():
    global current_activity
    current_activity = ACTIVITIES[random.randint(0, len(ACTIVITIES) - 1)]

if __name__ == "__main__":
    main() 