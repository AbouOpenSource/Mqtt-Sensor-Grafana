import json
import numpy as np
from datetime import datetime

class Queue:
    def __init__(self):
        self.ligne = []
        self.listTemperature = []
        self.listHumidity = []
        self.full =[]

    def add(self,ligne):
        ligne.decode("utf-8").replace("\r\n", "")
        jsonl = json.loads(ligne)
        jsonl["date"]= str(datetime.utcnow())
        self.addTemperature(jsonl["temperature"])
        self.addHumidity(jsonl["humidity"])
        self.addFull(str(jsonl))

    def addTemperature(self,item):
        self.listTemperature.append(item)
    def addFull(self,item):
        self.full.append(item)


    def addHumidity(self,item):
        self.listHumidity.append(item)
    def sendTemperature(self,client):
        for item in self.listTemperature:
            client.publish("/topic/temperature",item)
        self.listTemperature = []

    def sendHumidity(self,client):
        for item in self.listHumidity:
            client.publish("/topic/humidity", item)
        self.listHumidity = []
    
    def sendFull(self,client):
        for item in self.full:
            client.publish("/topic/all", item)
        self.full = []
    

    def sendAll(self,client):
        if len(self.listTemperature) > 100:
            self.sendTemperature(client)
            self.sendHumidity(client)
            self.sendFull(client)

        else:
           a= np.array(self.listTemperature)
           b= np.array(self.listHumidity)
           data = {}
           data['meanT'] = np.mean(a)
           data['meanH'] = np.mean(b)
           data['minT']= min(a)
           data['minH']= min(b)
           data['maxT']= max(a)
           data['maxH']= max(b)
           #json_data = json.dumps(data)
           client.publish("statistics",str(data)) 
    
    def displayAll(self,client):
        for i in self.listTemperature:
            print(i)
    
    def countTemperature(self):
        return len(self.listTemperature)        
    
    def isEmpty(self):
        return not self.listTemperature and not self.listHumidity
