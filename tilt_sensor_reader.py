#! /usr/bin/python

import paho.mqtt.client as mqtt

# def on_msg(client, userdata, msg):

client = mqtt.Client()
# client.on_message = on_msg

client.connect("broker.mqttdashboard.com", 1883, 60)
client.subscribe(topic="be5/impact")




import serial
ser = None

try:
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200)
except serial.SerialException as e:
    print(e)

print("Connected")

i = 1

while True:
    msg = ser.read(1)
    # print(msg)

    if msg == '1':
        client.publish("be5/impact2", msg)
        print("SOFT")

    if msg == '2':
        client.publish("be5/impact2", msg)
        print("HARD")
