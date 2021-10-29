from threading import Thread
from paho.mqtt import client as mqtt_client
import socket
import json
import quicksort
import random
import pickle

MAX_CONNECTIONS = 2

class FogThread(Thread):

    def __init__(self, idThread, idFog):       
        Thread.__init__(self)
        self.id = idThread
        self.idFog = idFog
        self.broker = '127.0.0.1'
        self.port = 1883
        self.topic = f'fog/{idFog}/{idThread}'
        self.data = []
        self.numConnections = 0

    def run(self):
        client = self.connect_mqtt(f'FogID {self.idFog} / ThreadID {self.id}')
        client.subscribe(self.topic)
        client.loop_forever()

    def connect_mqtt(self, client_id):
        client = mqtt_client.Client(client_id)
        client.on_connect = self.on_connect
        client.on_message = self.on_message       
        client.on_disconnect = self.on_disconnect      
        client.connect(self.broker, self.port)
        return client

    def on_message(self, client, userdata, msg):
        patientReceived = json.loads(msg.payload.decode('UTF-8'))
        idPatient = patientReceived['id']
        i = 0
        att = False
        for patient in self.data:
            if patient['id'] == idPatient:
                self.data[i] = patientReceived
                att = True
            i += 1
        if not att:
            self.data.append(patientReceived) 
            client.publish(f'fog/{self.idFog}/save-id', f'{idPatient},{self.id}')

        quicksort.quickSort(self.data)
        print("tamanho:", len(self.data), patientReceived['id'], self.id)

    def on_connect(self, client, userdata, flags, rc):
        print("rc: ", rc)
        print("flags: ", flags)
    
    def on_disconnect(self, client, userdata, rc):
        print("desconectou", "rc: ", rc)

class Fog:

    def __init__(self, id):
        self.id = id
        self.threads = []
        self.patientsID = {}
        self.broker = '127.0.0.1'
        self.port = 1883
        self.topicHandshake = f'fog/{id}'
        self.topicPatients = f'fog/{id}/patients'
        self.topicPatient = f'fog/{id}/patient'
        self.topicSaveID = f'fog/{id}/save-id'
        
    def run(self):
        client = self.connect_mqtt(f'fog {self.id}')
        client.subscribe(self.topicHandshake)
        client.subscribe(self.topicPatients)
        client.subscribe(self.topicPatient)
        client.subscribe(self.topicSaveID)
        client.loop_forever()
    
    def connect_mqtt(self, client_id):       
        client = mqtt_client.Client(client_id)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.broker, self.port)
        return client

    def on_connect(self, client, userdata, flags, rc):
        print("flag: ", flags)
   
        
    def on_message(self, client, userdata, msg):
        if (msg.topic == self.topicPatients):
            n = int(msg.payload.decode('utf-8'))
            #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            threadData = []
            for thread in self.threads:
                threadData.extend(thread.data[0:n])

            quicksort.quickSort(threadData)
            client.publish(f'api/patients', json.dumps(threadData))
            #s.sendto(json.dumps(threadData[0:n]).encode('utf-8'), ('127.0.0.1', 40000))

        
        elif(msg.topic == self.topicSaveID):
            splited = msg.payload.decode('utf-8').split(',')
            self.patientsID[int(splited[0])] = int(splited[1])

        elif(msg.topic == self.topicPatient):
            id = int(msg.payload.decode('utf-8'))
            found = False
            if id in self.patientsID:
                threadID = self.patientsID[id]
                patientsData = self.threads[threadID].data
                for patient in patientsData:
                    if(patient['id'] == id):
                        client.publish(f'api/patient', json.dumps(patient))
                        found = True
                        break
            if not found:
                client.publish(f'api/patient', "-1") #Paciente não está presente nessa Fog.               
            
        else:
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
        

fog = Fog(int(input("Digite o número da Fog:")))
fog.run()