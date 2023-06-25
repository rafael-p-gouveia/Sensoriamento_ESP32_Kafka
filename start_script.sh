#!/bin/bash

../kafka_2.13-3.5.0/bin/zookeeper-server-start.sh ../kafka_2.13-3.5.0/config/zookeeper.properties > /dev/null &
MY_PID=$!
echo $MY_PID >> pids.txt
echo "Primeiro comando executado"
sleep 40


../kafka_2.13-3.5.0/bin/kafka-server-start.sh  ../kafka_2.13-3.5.0/config/server.properties > /dev/null &
MY_PID=$!
echo $MY_PID >> pids.txt
echo "Segundo comando executado"
sleep 60

../kafka_2.13-3.5.0/bin/kafka-topics.sh --create --topic climateInfo --bootstrap-server localhost:9092 > /dev/null
echo "Terceiro comando executado"
sleep 40

python3 ./mqtt_bridge/mqtt_kafka_bridge.py > /dev/null &
MY_PID=$!
echo $MY_PID >> pids.txt
echo "Quarto comando executado"
sleep 20


sudo systemctl start mongod

echo "Quinto comando executado"
sleep 30

python3 ./mongo_db/kafka_mongodb_bridge.py > /dev/null &
MY_PID=$!
echo $MY_PID >> pids.txt

python3 -m http.server 9041 &> /dev/null &
MY_PID=$!
echo $MY_PID >> pids.txt
