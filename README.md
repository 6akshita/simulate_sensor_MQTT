# simulate_sensor_MQTT

configuration file - sensor.json 
Broker-broker.hivemq.com
Add more sensors in "sensor"
Change interval_ms to configure sensor data generation interval

To run publisher: python publish.py sensor.json
To run subscriber: python subscribe.py

Subscriber will receice data over a MQTT topic {topic_mension_in_conf.file/<sensor_name>} and then generate an email if average of values received is more than 80% for more than 5 min.

To generate email edit generate_email.py. Add email_address,username,password.
