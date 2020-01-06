
import paho.mqtt.client as mqtt
import json
from config import influxconfig
from config import broker
from influxdb import InfluxDBClient
from config import broker
json_body_tem = [
    {
        "measurement": "temperature",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }
]
json_body_hum = [
    {
        "measurement": "humidity",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }
]


#client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
client = InfluxDBClient(influxconfig["host"], influxconfig["port"], influxconfig["user"],  influxconfig["passwd"], influxconfig["db"])

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    textBrute= msg.payload.decode("utf-8").replace("\r\n", "")	
    y = eval(textBrute)
    json_body_tem[0]["fields"]["value"]=y['temperature']
    json_body_tem[0]["time"]=y['date']
    json_body_hum[0]["fields"]["value"]=y['humidity']
    json_body_hum[0]["time"]=y['date']
    #print(json_body_hum)
    print("before")
    print(client.write_points(json_body_tem))
    print(client.write_points(json_body_hum))
    print("stored")
    


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)



mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect(broker["host"], broker["port"], 60)
mqttc.subscribe("/topic/all", 0)

mqttc.loop_forever()
