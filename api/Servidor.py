import sys
sys.path.insert(0, 'C:\\Users\\pbexp\\Documents\\GitHub\\CCPBL2')

from paho.mqtt import client as mqtt_client
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
import numpy as np
import quicksort
import socket
import json
import time
from datetime import datetime
 
fogsID = np.arange(2)
patientsResponse = []

patientResponse = ""
found = False

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/patients/<int:n>', methods=['GET'])
@cross_origin(supports_credentials=True)
def patients(n: int):
    client = mqtt_client.Client("ServerApiPatients")
    client.on_connect = on_connect
    client.on_message = on_message_patients

    client.connect('127.0.0.1', 1883)
    client.subscribe(f'api/patients')

    init = time.time()
    for fogID in fogsID:
        client.publish(f'fog/{fogID}/patients', n)     
        client.loop_forever()

    diff = (time.time() - init) * 1000
    print(diff)
    quicksort.quickSort(patientsResponse)
    return jsonify(patientsResponse[0:n])

@app.route("/patient/<int:id>", methods=['GET'])
@cross_origin(supports_credentials=True)
def patient(id: int):
    client = mqtt_client.Client("ServerApiPatient")
    client.on_connect = on_connect
    client.on_message = on_message_patient

    client.connect('127.0.0.1', 1883)
    client.subscribe(f'api/patient')

    for fogID in fogsID:
        client.publish(f'fog/{fogID}/patient', id)  
        client.loop_forever()     
        if found:
            break

    if patientResponse == "":
        return jsonify({"message": "Paciente não encontrado."}), 404

    return jsonify(patientResponse)

def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker.")

def on_message_patients(client, userdata, msg):
    patientsResponse.extend(json.loads(msg.payload.decode('UTF-8')))
    client.disconnect()

def on_message_patient(client, userdata, msg):
    payload = msg.payload.decode('UTF-8') 
    if payload != "-1":
        global found, patientResponse
        found = True
        patientResponse = json.loads(payload)
    client.disconnect()