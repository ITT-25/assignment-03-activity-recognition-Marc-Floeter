# this program visualizes activities with pyglet

import random, time
import activity_recognizer as ar

ACTIVITIES = ["jumpingjack", "lifting", "rowing", "running"]
ROUND_TIME = 10
SCORING_INTERVAL = 1
current_activity = None

training = False

def main():
    print("Fitness Trainer gestartet")
    ar.main()
    choose_activity()
    print("Hallo Sportskanone! Bereit für ein paar Übungen?")
    print(f'Starte deine erste Runde {current_activity} mit Button 1 und mache die Übung für {ROUND_TIME} Sekunden!')
    start_activity()


def choose_activity():
    global current_activity
    current_activity = ACTIVITIES[random.randint(0, len(ACTIVITIES) - 1)]


def wait_for_start():
    while not training:
        if ar.training == True:
            training = True
            start_activity()
        else:
            print("Warte auf Start durch Buttonklick")


def start_activity():
    start_time = time.time()
    while training:
        if (time.time() - start_time) > ROUND_TIME:
            ar.stop_training()

        else:
            if current_activity == ar.current_prediction:
                print(f'Richtige Aktivität erkannt: {current_activity}')
            else:
                print(f'Richtige Aktivität erkannt: {ar.current_prediction} statt {current_activity}')
            time.sleep(SCORING_INTERVAL)


if __name__ == "__main__":
    main() 