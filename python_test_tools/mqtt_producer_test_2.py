import paho.mqtt.client as mqtt
from random import uniform
import time

mqtt_broker = 'mqtt.eclipseprojects.io'
mqtt_client = mqtt.Client('ClimateInfoProducer1')
mqtt_client.connect(mqtt_broker)

while True:
    randTemp = uniform(20.0,21.0)
    randUmid = uniform(60.0,61.0)
    data = "Temp: {0} Umid: {1}".format(randTemp,randUmid)
    mqtt_client.publish("climateInfo",data)
    print('MQTT published: ' + str(data) + ' to topic climateInfo')
    time.sleep(3)

