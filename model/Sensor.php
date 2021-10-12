<?php

class Sensor{

    public $temperature;
    public $respiratoryRate;
    public $heartRate;
    public $bloodOxygenation;
    public $arterialPressure; 

    public function __construct($temperature, $respiratoryRate, $heartRate, $bloodOxygenation, $arterialPressure){
        $this->temperature = $temperature;
        $this->respiratoryRate = $respiratoryRate;
        $this->heartRate = $heartRate;
        $this->bloodOxygenation = $bloodOxygenation;
        $this->arterialPressure = $arterialPressure;
    }

    public function getTemperature(){
        return $this->temperature;
    }
    public function getRespiratoryRate(){
        return $this->respiratoryRate;
    }
    public function getHeartRate(){
        return $this->heartRate;
    }
    public function getBloodOxygenation(){
        return $this->bloodOxygenation;
    }
    public function getArterialPressure(){
        return $this->arterialPressure;
    }

    public function setTemperature($temperature){
        $this->temperature = $temperature;
    }

    public function setRespiratoryRate($respiratoryRate){
        $this->respiratoryRate = $respiratoryRate;
    }

    public function setHeartRate($heartRate){
        $this->heartRate = $heartRate;
    }
    public function setBloodOxygenation($bloodOxygenation){
        $this->bloodOxygenation = $bloodOxygenation;
    }
    public function setArterialPressure($arterialPressure){
        $this->arterialPressure = $arterialPressure;
    }
}