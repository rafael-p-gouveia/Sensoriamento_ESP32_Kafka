FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3

RUN apt-get install -y curl

RUN curl -O "https://dlcdn.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz"

RUN tar -xzf kafka_2.13-3.5.0.tgz

RUN apt-get install -y pip

RUN pip install pymongo

RUN pip install pykafka

RUN pip install datetime

RUN pip install matplotlib

RUN pip install paho.mqtt

RUN dpkg --configure -a

RUN apt-get -y update

RUN apt-get install -y gnupg

RUN curl -fsSL https://pgp.mongodb.com/server-4.4.asc | gpg -o /usr/share/keyrings/mongodb-server-4.4.gpg    --dearmor --yes

RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-4.4.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list

RUN apt install -y mongodb-org=4.4.15 mongodb-org-server=4.4.15 mongodb-org-shell=4.4.15 mongodb-org-mongos=4.4.15 mongodb-org-tools=4.4.15

RUN systemctl enable mongod


RUN git clone  https://github.com/rafael-p-gouveia/Sensoriamento_ESP32_Kafka.git

RUN python3 ~/mongo_db/create_server_mongodb.py

ADD index.html .
EXPOSE 9041
ENTRYPOINT ["cd", "Sensoriamento_ESP32_Kafka", "&&", "bash", "start_script.sh"]