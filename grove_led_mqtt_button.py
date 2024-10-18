#!/usr/bin/env python

import time
import grovepi
import paho.mqtt.client as mqtt

led = 6 #D6
button = 4 #D4

grovepi.pinMode(led,"OUTPUT")
grovepi.pinMode(button,"INPUT")
time.sleep(1)

button_state = False
hostname = "192.192.2.13" #gstfill in
broker_port = 1883
topic = "/command"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))
    client.subscribe(topic)
    print("Subscribed to topic :" + topic)

def on_message(client, userdata, msg):
    command =  msg.payload.decode()
    print("Message received: " + command)

    if command == "ON" :
        button_state = True
        grovepi.digitalWrite(led, button_state)
        client.publish(topic, "ON_OK")
    elif command == "OFF" :
        button_state = False
        grovepi.digitalWrite(led, button_state)
        client.publish(topic, "OFF_OK")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Connecting to MQTT broker")

client.username_pw_set("thinkuldeep", "mqtt")
client.connect(hostname, broker_port, 60)
client.loop_start()

time.sleep(1)
client.publish(topic, "OFF_OK")

print ("Press button to switch on/off LED")

while True:
    try:
        bInput = grovepi.digitalRead(button)
        if bInput == 1 :
            button_state = not button_state
            if button_state :
                client.publish(topic, "ON")
            else :
                client.publish(topic, "OFF")

        time.sleep(0.2)

    except KeyboardInterrupt:   # Turn LED off before stopping
        digitalWrite(led,0)
        client.loop_stop()
        client.disconnect()
        break
    except IOError:             # Print "Error" if communication error encountered
        print ("Error")