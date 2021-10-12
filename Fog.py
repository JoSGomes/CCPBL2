import json
import random
from threading import Thread
from paho.mqtt import client as mqtt_client

MAX_CONNECTIONS = 10

class FogThread(Thread):

    def __init__(self, idThread, idFog):
        Thread.__init__(self)
        self.id = idThread
        self.broker = '127.0.0.1'
        self.port = 1883
        self.topic = f'fog/{idFog}/{idThread}'
        self.data = []
        self.numConnections = 0

    def run(self):
        client = self.connect_mqtt(f'FogThread {self.id}')
        client.subscribe(self.topic)
        client.loop_forever()

    def connect_mqtt(self, client_id):
        client = mqtt_client.Client(client_id)
        client.on_connect = self.on_connect
        client.on_message = self.on_message       
        client.connect(self.broker, self.port)
        return client

    def on_message(self, client, userdata, msg):
        patientReceived = json.loads(msg.payload.decode('UTF-8'))
        i = 0
        att = False
        for patient in self.data:
            if patient['id'] == patientReceived['id']:
                self.data[i] = patientReceived
                att = True
            i += 1
        if not att:
            self.data.append(patientReceived)           
        print("tamanho:", len(self.data), patientReceived['id'], self.id)

    def on_connect(self, client, userdata, flags, rc):
        print("rc: ", rc)
    


class Fog:

    def __init__(self, id):
        self.id = id
        self.threads = []
        self.devices = []
        self.broker = '127.0.0.1'
        self.port = 1883
        self.topic = f'fog/{id}'
        

    def run(self):
        client = self.connect_mqtt(f'fog {self.id}')
        client.subscribe(self.topic)
        client.loop_forever()
    
    def connect_mqtt(self, client_id):       
        client = mqtt_client.Client(client_id)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.broker, self.port)
        return client

    def on_connect(self, client, userdata, flags, rc):
        print("rc: ", rc)

    def on_message(self, client, userdata, msg):
        idThread = None
        sizeTheads = len(self.threads)
        
        if sizeTheads == 0:
            idThread = 0
            newThread = FogThread(idThread, self.id) 
            newThread.numConnections += 1 
            newThread.start()        
            self.threads.append(newThread)

        else:
            for thread in self.threads:
                if thread.numConnections < MAX_CONNECTIONS:
                    idThread = thread.id
                    thread.numConnections += 1
                    break
            if idThread == None:
                idThread = sizeTheads
                newThread = FogThread(idThread, self.id)
                newThread.start()
                self.threads.append(newThread)
        idDevice = msg.payload.decode('UTF-8')
        client.publish(f'device/{idDevice}', f'fog/{self.id}/{idThread}')
        

fog = Fog(0)
fog.run()