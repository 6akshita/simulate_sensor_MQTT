import paho.mqtt.client as mqttClient
import time
import json
import generate_email
from collections import defaultdict

d=defaultdict(list)

def check_alert(sensor_name, sensor_value, threshold_value, topic):
    if sensor_name not in d.keys():
        d[sensor_name].append(sensor_value)
    else:
        last_n_record= d[sensor_name]
        if len(last_n_record)<5:
            last_n_record.append(sensor_value)
        if len(last_n_record) == 5:
            avg_of_n_value=sum(last_n_record)/5
            if avg_of_n_value >= threshold_value:
                print("Sending alert email")
                generate_email.send_alert_email("ALERT : Please turn {} off. Running on topic {}.Last record {}".format(sensor_name, topic, last_n_record))
            del last_n_record[0]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    data=json.loads(message.payload)
    print("{} {} ".format(message.topic, data))
    min_value=data["min"]
    max_value=data["max"]
    threshold_value=(max_value-min_value)*0.8 + min_value
    check_alert(data["Sensor"], data["value"], threshold_value, message.topic)

if __name__ == '__main__':
    Connected = False   #global variable for the state of the connection
    broker_address= "broker.hivemq.com"
    port = 1883
    client = mqttClient.Client()
    client.on_connect= on_connect
    client.on_message= on_message

    client.connect(broker_address, port=port)
    client.loop_start()
    while Connected != True:
        time.sleep(0.1)

    client.subscribe("sensor_data/Thermistor")
    client.subscribe("sensor_data/HS_1101")
    client.subscribe("sensor_data/BMP280")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("exiting")
        client.disconnect()
        client.loop_stop()
