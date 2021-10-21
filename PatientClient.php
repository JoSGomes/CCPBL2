<?php

require "vendor/autoload.php";
require "model/Patient.php";
require "model/Sensor.php";

use \PhpMqtt\Client\MqttClient;

class PatientClient {

    private $patient;
    private $tendency;
    private $addr;
    private $port;
    private $clientId;

    private $topic;
    private $fogID;

    public function __construct() { 
        $this->patient = new Patient(new Sensor(random_int(360, 400)/10,random_int(9, 29) ,random_int(51, 130), random_int(40, 99), random_int(71, 120) ),  random_int(1111, 9999));
        $this->tendency = random_int(0, 2);
        $this->addr = '127.0.0.1';
        $this->port = 1883;
        $this->clientId = rand(5, 15);
        $this->fogID = rand(0, 1); # [0, 4]
    }

    public function run() 
    {
        $mqtt = new MqttClient($this->addr, $this->port, $this->clientId);
        $mqtt->connect();
        while (!$this->topic)
        {
            $mqtt->subscribe('device/' . $this->patient->getPatientID(), function($topic, $message) use ($mqtt){
                $this->topic = $message;
                $mqtt->interrupt();
            }, 0); #inscreve em device/idDevice
            $mqtt->publish('fog/' . $this->fogID, $this->patient->getPatientID(), 0); #publica em fog/{idFog}
            $mqtt->loop(True);
        }
    
        while(true)
        {   
            $json = '';
              
            if($this->tendency == 0)
            {
                $this->patient->generateNormalValuesSensor();
                $json = PatientClient::sendValues($mqtt);
            }
            else if($this->tendency = 1)
            {
                $this->patient->generateMediumValuesSensor();
                $json = PatientClient::sendValues($mqtt);
            }
            else
            {
                $this->patient->generateLargeValuesSensor();
                $json = PatientClient::sendValues($mqtt);
            }

            echo "\nValores atuais...\n " . $json;                 
            sleep(3); 
        }       
    }

    public function sendValues($mqtt)
    {
        $json = json_encode($this->patient);
        $mqtt->publish($this->topic, $json, 0);  
        echo "\nPaciente " . $this->patient->id . " enviado.\n";
        return $json;
    }
}

$patient = new PatientClient();
$patient->run();