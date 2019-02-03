#! /usr/bin/python

import paho.mqtt.client as mqtt

def on_msg(client, userdata, msg):
    p = str(msg.payload)[2:][:-1]
    spl = p.split(',')

    vals = [float(s) for s in spl]

    print(vals)

    if (vals[3] == 0):
        print("not storing")
        return

    f = open('/tmp/impact.txt', 'a')
    f.write(p + '\n')
    f.close()

client = mqtt.Client()
client.on_message = on_msg

client.connect("broker.mqttdashboard.com", 1883, 60)
client.subscribe(topic="be5/impact")

client.loop_forever()

