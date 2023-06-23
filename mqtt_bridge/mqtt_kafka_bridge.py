#Includes
import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import datetime as dt
import time

#Get the menssage from MQTT and publish in the Kafka
def on_message(client,userdate,message):
    msg_payload = str(message.payload)
    print('MQTT received: ' , msg_payload)
    now = dt.datetime.now()
    msg_payload = str(now) + "|" + msg_payload #Add Date/Time at the beginning of the string
    kafka_producer.produce(str(msg_payload).encode('ascii'))
    print('KAFKA published: ', msg_payload , ' to climateInfo\n')

#MQTT credentials
mqtt_broker = 'mqtt.eclipseprojects.io'
mqtt_client = mqtt.Client('MQTTBridge')
mqtt_client.connect(mqtt_broker)

#Kafka credentials
kafka_client = KafkaClient(hosts='localhost:9092')
kafka_topic = kafka_client.topics['climateInfo']
kafka_producer = kafka_topic.get_sync_producer()

#Send the menssage from MQTT to Kafka in climateInfo topic
while True:
    mqtt_client.loop_start()
    mqtt_client.subscribe('climateInfo')
    mqtt_client.on_message = on_message
    time.sleep(300)
    mqtt_client.loop_stop()

    
