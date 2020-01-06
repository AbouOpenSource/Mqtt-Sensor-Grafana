
import serial
import paho.mqtt.client as mqtt
import json
from datetime import datetime
from Queue import Queue
from config import broker

#The parameter of broker 
broker="127.0.0.1"
port=1883
connected = False
dataToStore = []
queue = Queue()
def on_connect(client, userdata, flags, rc):
	if rc==0:
		connected = True
	else:
		connected = False

def on_publish(client,userdata,result):
    print("status of sending"+result)
    pass

client = mqtt.Client("producer1")
#client.username_pw_set(username=broker["user"],password=broker["passwd"])
client.on_publish = on_publish
client.on_connect = on_connect
client.connect(broker,port)

client.loop_start()
tes = serial.Serial(port="/dev/ttyACM0", baudrate=115200, timeout=1, writeTimeout=1) 
if tes.isOpen():
	while True:
		ligne = tes.readline()
		if ligne.decode("utf-8").startswith('{'):
			"""
				strore in influxdb part
			 
			
			"""
			ligne.decode("utf-8").replace("\r\n", "")
			text = json.loads(ligne)
			print(text["temperature"])
			text["date"]= str(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
			result, ret = client.publish("/topic/temperature", text["temperature"])
			result1, ret1 = client.publish("/topic/humidity", text["humidity"])
			
			result1, ret1 = client.publish("/topic/all", str(text))
			
			if result == 0:
				if not queue.isEmpty():
					queue.sendAll(client)
				print("online")
			else:
				queue.add(ligne)
				#dataToStore.append(ligne)
				print("offline")	
client.loop_stop()