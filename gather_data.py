# this program gathers sensor data

import csv, time, os
from DIPPID import SensorUDP

ACTIVITIES = ["jumpingjack", "lifting", "rowing", "running"] # jumpingjack, lifting, rowing oder running
REPS_PER_ACTIVITY = 5
SAMPLE_LENGTH = 10 # in s
SAVE_DATA_PATH = "data/marc"

logging = False
writer = None
file = None
activity_no = 3
rep_start_time = 0
rep_no = 5
id = 0
acc_x = 0
acc_y = 0
acc_z = 0
gyro_x = 0
gyro_y = 0
gyro_z = 0

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

def handle_button_1(data):
    global logging, writer, file, rep_no, rep_start_time
    if data == 1 and not logging:
        print(f'Logging aktiviert für {ACTIVITIES[activity_no]}-{rep_no}/{REPS_PER_ACTIVITY}')
        file = open(f'{SAVE_DATA_PATH}/marc-{ACTIVITIES[activity_no]}-{rep_no}.csv', mode='w', newline='')
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z'])
        rep_start_time = time.time()
        logging = True

sensor.register_callback('button_1', handle_button_1)

print(f'Verbinde DIPPID, dann drücke Button 1, um Runde 1 von Aktivität {ACTIVITIES[0]} zu starten. Die Aufnahme beendet sich nach {SAMPLE_LENGTH}s automatisch')

while True:
    if logging:
        if time.time() - rep_start_time < SAMPLE_LENGTH:
            id += 1
            timestamp = time.time()
            acc_x = sensor.get_value('accelerometer')['x']
            acc_y = sensor.get_value('accelerometer')['y']
            acc_z = sensor.get_value('accelerometer')['z']
            gyro_x = sensor.get_value('gyroscope')['x']
            gyro_y = sensor.get_value('gyroscope')['y']
            gyro_z = sensor.get_value('gyroscope')['z']
            writer.writerow([timestamp, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z])
            print(f'id: {id}, t: {timestamp}, ax: {acc_y}, ay: {acc_x}, az: {acc_z}, gx: {gyro_x}, gy: {gyro_y}, gz: {gyro_z}')
        else:
            print(f'Logging beendet für {ACTIVITIES[activity_no]}-{rep_no}/{REPS_PER_ACTIVITY}.') 
            logging = False
            file.close()
            id = 0
            rep_start_time = 0
            rep_no += 1
            if rep_no > REPS_PER_ACTIVITY:
                rep_no = 1
                activity_no += 1
                if activity_no >= (len(ACTIVITIES)):
                    print("Alle Activities sind durch, Versuch abgeschlossen!")
                    os._exit(0)
            else:
                print(f'Drücke Button 1, um die nächste Wiederholung von {ACTIVITIES[activity_no]} zu starten')

    time.sleep(0.0001)