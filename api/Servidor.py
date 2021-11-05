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
 
fogsAddr = ['26.90.73.25', '26.183.229.122']
PORT = 40000
patientsResponse = []

patientResponse = ""
found = False

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/patients/<int:n>', methods=['GET'])
@cross_origin(supports_credentials=True)
def patients(n: int):
    global patientsResponse 
    client = mqtt_client.Client("ServerApiPatients")
    client.on_connect = on_connect
    client.on_message = on_message_patients
    
    init = time.time()
    i = 0
    
    patientsResponse = []
    for addr in fogsAddr:
        client.connect(addr, PORT)
        client.subscribe(f'api/patients')
        client.publish(f'fog/{i}/patients', n)     
        client.loop_forever()
        i += 1

    diff = (time.time() - init) * 1000
    #print(diff) #retire o comentário caso queira saber o tempo para pegar os dados das Fog's e execute novamente a API.
    quicksort.quickSort(patientsResponse)
    return jsonify(patientsResponse[0:n])

@app.route("/patient/<int:id>", methods=['GET'])
@cross_origin(supports_credentials=True)
def patient(id: int):
    client = mqtt_client.Client("ServerApiPatient")
    client.on_connect = on_connect
    client.on_message = on_message_patient

    i = 0
    for addr in fogsAddr:
        client.connect(addr, PORT)
        client.subscribe(f'api/patient')
        client.publish(f'fog/{i}/patient', id)  
        client.loop_forever()     
        if found:
            break
        i += 1
    if patientResponse == "":
        return jsonify({"message": "Paciente não encontrado."}), 404

    return jsonify(patientResponse)

def on_connect(client, userdata, flags, rc):
    rc = rc

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