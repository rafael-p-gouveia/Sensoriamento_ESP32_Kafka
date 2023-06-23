#!/bin/bash

~/kafka/kafka_2.13-3.4.0/bin/zookeeper-server-start.sh ~/kafka/kafka_2.13-3.4.0/config/zookeeper.properties > /dev/null &
MY_PID=$!
echo $MY_PID >> pids.txt
echo "Primeiro comando executado"
sleep 10


~/kafka/kafka_2.13-3.4.0/bin/kafka-server-start.sh  ~/kafka/kafka_2.13-3.4.0/config/server.properties > /dev/null &
MY_PID=$!
echo $MY_PID >> pids.txt
echo "Segundo comundo executado"
sleep 40

python3 ~/kafka/mqtt_bridge/mqtt_kafka_bridge.py > /dev/null &
MY_PID=$!
echo $MY_PID >> pids.txt
echo "Terceiro comando executado"
sleep 10


sudo systemctl start mongod

echo "Quarto comando inicial"
sleep 30

python3 ~/mongoDB/kafka_consumidor_mongo.py > /dev/null &
MY_PID=$!
echo $MY_PID >> pids.txt