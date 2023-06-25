from pykafka import KafkaClient
from pymongo.errors import DuplicateKeyError
import datetime as dt
import time
import pymongo
import sys
import re
import matplotlib.pyplot as plt
import numpy as np
import os

def db_exists(client,db_name):
    dblist = client.list_database_names()
    if db_name in dblist:
        print("The database '{0}' exists.".format(db_name))
        return True
    else:
        print("The database '{0}' doesn't exists".format(db_name))
        return False

def col_exists(db,col_name):
    collist = db.list_collection_names()
    if col_name in collist:
        print("The collection '{0}' exists.".format(col_name))
        return True
    else:
        print("The collection '{0}' doesn't exists.".format(col_name))
        return False

#uses matplotlib to make charts from temperature and humidity
def make_chart(temperature_h_list, humidity_h_list,aux):
    fig,ax = plt.subplots()
    ax.plot(np.linspace(0,60,len(temperature_h_list)),temperature_h_list,linewidth=2.0)
    ax.set_title('Temperatura na Última Hora - Placa E00{}'.format(aux))
    ax.set(xticks=np.arange(0,61,10),xlabel='t (min)',
            ylabel='T (°C)')
    plt.savefig('temp_chart{}.png'.format(aux))
    del fig
    del ax

    fig2,ax2 = plt.subplots()
    ax2.plot(np.linspace(0,60,len(humidity_h_list)),humidity_h_list,linewidth=2.0)
    ax2.set_title('Humidade na Última Hora - Placa E00{}'.format(aux))
    ax2.set(xticks=np.arange(0,61,10),xlabel='t (min)',
            ylabel='H (%)')
    plt.savefig('hum_chart{}.png'.format(aux))
    del fig2
    del ax2

#takes data from kafka, send to mongo and send email per 10 hours
def run(kafka_consumer,mycol):
    while(True):
        now_time = time.time()

        datetime_h_list = []
        temperature_h_list_E1 = []
        temperature_h_list_E2 = []
        humidity_h_list_E1 = []
        humidity_h_list_E2 = []

        flag = False

        for msg in kafka_consumer:
            print(msg.value)
            payload = str(msg.value)
            datetime, remainder = payload.split("|")
            remainder = remainder[1:] #remainder = ["T:", TEMPERATURE, "U:", UMIDITY, SENSOR_NAME]
            remainder = remainder.split(" ")
            input_dict = {"_id": remainder[3] + "|" + datetime, "T": remainder[1], "U": remainder[3]}

            print("ID: {}; DATE: {}; Time: {};T: {:0.2}C; H: {:0.2}%".format(remainder[4],datetime.split(" ")[0], datetime.split(" ")[1],remainder[1],remainder[3]))

            try:
                mycol.insert_one(input_dict)

            except DuplicateKeyError:
                print("Entrada já inserida")

            id_h = remainder[4].split("'")[0]
            datetime_h_list.append(datetime)

            if (id_h.find('E001') != -1):
                temperature_h_list_E1.append(float(remainder[1]))
                humidity_h_list_E1.append(float(remainder[3]))
            elif (id_h.find('E002') != -1):
                temperature_h_list_E2.append(float(remainder[1]))
                humidity_h_list_E2.append(float(remainder[3]))

            if time.time() >= now_time + 20: #wait an hour to remake the charts

                if flag:
                    os.remove('temp_chart.png')
                    os.remove('hum_chart.png')
                    flag = False

                make_chart(temperature_h_list_E1,humidity_h_list_E1,1)
                make_chart(temperature_h_list_E2,humidity_h_list_E2,2)
                flag = True

                break

if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    try:
        myclient.admin.command('ping')
        print("Connection established")
    except:
        sys.exit("Connection failed to be established")

    mydb = myclient["SensorData"] 

    db_exists(myclient,"SensorData")

    mycol = mydb["data"] 

    assert col_exists(mydb,"data"), "Database and/or collection failed to be created"

    kafka_client = KafkaClient(hosts='localhost:9092')
    kafka_topic = kafka_client.topics['climateInfo']
    kafka_consumer = kafka_topic.get_simple_consumer() #no consumer_timeout_ms, waits forever if iterating

    run(kafka_consumer,mycol)
