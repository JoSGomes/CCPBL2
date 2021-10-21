from paho.mqtt import client as mqtt_client
from flask import Flask, jsonify
import socket
import json
import numpy as np

fogsID = np.arange(2)

app = Flask(__name__)

@app.route('/patients')
def patients():
    client = mqtt_client.Client("ServerApiPatients")
    client.on_connect = on_connect
    client.connect('127.0.0.1', 1883)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 40000))
    dataResponse = []

    for fogID in fogsID:
        client.publish(f'fog/{fogID}/patients', "10")       
        dataResponse.append(json.loads(s.recv(4096).decode('UTF-8')))
        #tem que ordenar as cabeçs
        #pegar a latencia

    s.close()
    return jsonify(dataResponse)

def on_connect(self, client, userdata, flags, rc):
    return rc

@app.route("/patient/<int:id>")
def patient(id: int):
    client = mqtt_client.Client("ServerApiPatient")
    client.on_connect = on_connect
    client.connect('127.0.0.1', 1883)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    s.bind(('127.0.0.1', 40000))

    
    for fogID in fogsID:
        client.publish(f'fog/{fogID}/patient', id)        
        socketResponse = s.recv(4096).decode('UTF-8')
        if(socketResponse != "-1"):
            patientResponse = json.loads(socketResponse)
            break
    s.close
    return jsonify(patientResponse)