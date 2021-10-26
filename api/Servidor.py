import sys
sys.path.insert(0, 'C:\\Users\\pbexp\\Documents\\GitHub\\CCPBL2')

from paho.mqtt import client as mqtt_client
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import numpy as np
import quicksort
import socket
import json

 
fogsID = np.arange(2)

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/patients/<int:n>', methods=['GET'])
@cross_origin(supports_credentials=True)
def patients(n: int):
    client = mqtt_client.Client("ServerApiPatients")
    client.on_connect = on_connect
    client.connect('127.0.0.1', 1883)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 40000))
    dataResponse = []

    for fogID in fogsID:
        client.publish(f'fog/{fogID}/patients', n)       
        dataResponse.extend(json.loads(s.recv(4096).decode('UTF-8')))
        #pegar a latencia

    quicksort.quickSort(dataResponse)
    s.close()
    return jsonify(dataResponse[0:n])

@app.route("/patient/<int:id>", methods=['GET'])
@cross_origin(supports_credentials=True)
def patient(id: int):
    client = mqtt_client.Client("ServerApiPatient")
    client.on_connect = on_connect
    client.connect('127.0.0.1', 1883)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    s.bind(('127.0.0.1', 40000))
 
    patientResponse = None
    for fogID in fogsID:
        client.publish(f'fog/{fogID}/patient', id)        
        socketResponse = s.recv(4096).decode('UTF-8')
        if(socketResponse != "-1"):
            patientResponse = json.loads(socketResponse)
            break
    s.close
    if patientResponse == None:
        return jsonify({"message": "Paciente não encontrado."}), 404
    return jsonify(patientResponse)

def on_connect(self, client, userdata, flags, rc):
    return rc