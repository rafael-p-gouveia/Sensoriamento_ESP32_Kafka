# Weather Data Collection

## QuickStart setup in the server side:

### Server side requiriments:
  
  -Apache Kafka
  
  -Mongo DB 4.4.15
  
  -Python 3.10
  
  -pymongo library
  
  -paho-mqtt library
  
  -pykafka
  
### Easy Start:
   -Start all the Weather Data Collection enviroment by running the start_script.sh
    
      bash start_script.sh
      
### Easy Kill:
   -Kill all the Weather Data Collection enviroment by running the kill_processes.sh
    
      bash kill_processes.sh
      
## Manual setup in the server side:

### Starting the Kafka environment:
  
  -Start Zookeeper by running this command in the Apache Kafka directory:
  
    bin/zookeeper-server-start.sh config/zookeeper.properties
    
  -Start Kafka broker service by running this command in the Apache Kafka directory:
  
    bin/kafka-server-start.sh config/server.properties
    
  -If you haven't created the Kafka topic yet, run this command in the Apache Kafka directory:
  
    bin/kafka-topics.sh --create --topic climateInfo --bootstrap-server localhost:9092
    
### Starting the MQTT Bridge:
 
   -In /mqtt_bridge Run this python script:
   
     python3 mqtt_kafka_bridge.py
      
### Starting the MongoDB:
    
   -If you haven't started the MongoDB yet, run this command in /mongoDB:
   
      python3 create_server_mongodb.py
      
   -Start the MongoDB Bridge by running this command in /mongoDB :
   
      python3 kafka_mongodb_bridge.py
      
## ESP32 Configuration
      
This repository contains code for collecting weather data using ESP32 microcontrollers and two types of sensors: the SHT11 and DHT22. Both sensors are capable of measuring temperature and humidity.

### Hardware Setup
  To use this code, you will need the following components:

### Software Setup
  Before running the code, you will need to install the necessary software libraries:

  SHT1x.h for SHT11 sensor
  
  DHT.h for DHT22 sensor
  
To connect to your WiFi network, open the config.h file and enter your network name and password.

Next, open the code for your sensor and make sure the pins for data (SDA) and clock (SCL) are correct. If necessary, update the pin numbers.

To adjust the frequency of data transmission, change the value of the DELAY_TIME variable in the code.
