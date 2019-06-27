import sys
import json
import time
import random

import paho.mqtt.client as mqtt

def generate(host, port, topic, sensors, interval_ms, verbose):
    """generate data and send it to an MQTT broker"""
    client = mqtt.Client()
    client.loop_start()
    client.connect(host, port)

    sensors_list = list(sensors.keys())
    interval_secs = interval_ms / 1000.0

    while True:
        for sensor_name in sensors_list:
            sensor = sensors[sensor_name]
            min_val, max_val = sensor.get("range",)
            val = random.randint(min_val, max_val)
            data = {
                "Sensor": sensor_name,
                "value": val,
                "max": max_val,
                "min": min_val
            }
            for key in [ "unit", "type", "description"]:
                value = sensor.get(key)
                if value is not None:
                    data[key] = value

            topic_1 = topic + "/"+ sensor_name
            payload = json.dumps(data)
            if verbose:
                print("%s: %s" % (topic_1, payload))
            client.publish(topic_1, payload)
            time.sleep(interval_secs)

def main(config_path):
    """main entry point, load and validate config and call generate"""
    try:
        with open(config_path) as handle:
            config = json.load(handle)
            mqtt_config = config.get("mqtt", {})
            misc_config = config.get("misc", {})
            sensors = config.get("sensors")

            interval_ms = misc_config.get("interval_ms")
            verbose = misc_config.get("verbose")

            if not sensors:
                print("no sensors specified in config, nothing to do")
                return

            host = mqtt_config.get("host")
            port = mqtt_config.get("port")
            topic = mqtt_config.get("topic")

            generate(host, port, topic, sensors, interval_ms, verbose)
    except IOError as error:
        print("Error opening config file '%s'" % config_path, error)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage %s sensor.json" % sys.argv[0])