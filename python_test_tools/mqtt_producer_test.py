import paho.mqtt.client as mqtt
from pykafka import KafkaClient
from random import uniform
import time

mqtt_broker = 'mqtt.eclipseprojects.io'
mqtt_client = mqtt.Client('Temperature')
mqtt_client.connect(mqtt_broker)

kafka_client = KafkaClient(hosts='localhost:9092')
kafka_topic = kafka_client.topics['temperature3']
kafka_producer = kafka_topic.get_sync_producer()

while True:
    randNumber = uniform(20.0,21.0)
    mqtt_client.publish("temperature3",randNumber)
    print('MQTT: Just published ' + str(randNumber) + ' to topic temperature3')
    
    kafka_producer.produce(str(randNumber).encode('ascii'))
    print('KAKFA: Just published ' + str(randNumber) + ' to topic temperature3')
    time.sleep(3)

