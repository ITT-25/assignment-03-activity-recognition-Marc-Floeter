import time
from collections import deque
from DIPPID import SensorUDP

PORT = 5700
sensor = SensorUDP(PORT)

ACTIVITIES = ["jumpingjack", "lifting", "rowing", "running"]
WINDOW_SIZE = 100
SAMPLE_RATE = 0.01

training = False

id = 0

ids = deque(maxlen=WINDOW_SIZE)
timestamp = deque(maxlen=WINDOW_SIZE)
acc_x = deque(maxlen=WINDOW_SIZE)
acc_y = deque(maxlen=WINDOW_SIZE)
acc_z = deque(maxlen=WINDOW_SIZE)
gyro_x = deque(maxlen=WINDOW_SIZE)
gyro_y = deque(maxlen=WINDOW_SIZE)
gyro_z = deque(maxlen=WINDOW_SIZE)


def handle_button_1(data):
    global training, id, timestamp, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z

    if data == 1:
        if not training:
            print("Input aktiviert")
            training = True
            get_live_sensor_data()

sensor.register_callback('button_1', handle_button_1)

def get_live_sensor_data():
    while training:
        start_time = time.time()
        ids.append(id)
        timestamp.append(start_time)
        acc_x.append(sensor.get_value('accelerometer')['x'])
        acc_y.append(sensor.get_value('accelerometer')['y'])
        acc_z.append(sensor.get_value('accelerometer')['z'])
        gyro_x.append(sensor.get_value('gyroscope')['x'])
        gyro_y.append(sensor.get_value('gyroscope')['y'])
        gyro_z.append(sensor.get_value('gyroscope')['z'])

        print(f'id: {id}, t: {timestamp[-1]}, ax: {acc_x[-1]}, ay: {acc_y[-1]}, az: {acc_z[-1]}, gx: {gyro_x[-1]}, gy: {gyro_y[-1]}, gz: {gyro_z[-1]}')
        id += 1
        elapsed_time = time.time() - start_time
        sleep_time = SAMPLE_RATE - elapsed_time

        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            print(f'Daten Abfangen dauert länger als ein Sample-Interval! Sleep-Time: {sleep_time}')


def stop_training():
    global training

    print("Training gestoppt (DIPPID)")
    training = False 