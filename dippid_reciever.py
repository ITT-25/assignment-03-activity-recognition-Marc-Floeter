import time, os
from DIPPID import SensorUDP

ACTIVITIES = ["jumpingjack", "lifting", "rowing", "running"] # jumpingjack, lifting, rowing oder running
SAMPLE_RATE = 0.01

training = False
id = 0
timestamp = []
acc_x = []
acc_y = []
acc_z = []
gyro_x = []
gyro_y = []
gyro_z = []

PORT = 5700
sensor = SensorUDP(PORT)

def handle_button_1(data):
    global training, id, timestamp, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z
    print("Button 1")
    if data == 1:
        if training:
            print("Input deaktiviert")
            training = False
            id = 0
            timestamp.clear()
            acc_x.clear()
            acc_y.clear()
            acc_z.clear()
            gyro_x.clear()
            gyro_y.clear()
            gyro_z.clear()
        else:
            print("Input aktiviert")
            training = True

sensor.register_callback('button_1', handle_button_1)

while True:
    if training:
            id += 1
            timestamp.append(time.time())
            acc_x.append(sensor.get_value('accelerometer')['x'])
            acc_y.append(sensor.get_value('accelerometer')['y'])
            acc_z.append(sensor.get_value('accelerometer')['z'])
            gyro_x.append(sensor.get_value('gyroscope')['x'])
            gyro_y.append(sensor.get_value('gyroscope')['y'])
            gyro_z.append(sensor.get_value('gyroscope')['z'])
            print(f'id: {id}, t: {timestamp[-1]}, ax: {acc_y[-1]}, ay: {acc_x[-1]}, az: {acc_z[-1]}, gx: {gyro_x[-1]}, gy: {gyro_y[-1]}, gz: {gyro_z[-1]}')
    time.sleep(SAMPLE_RATE)