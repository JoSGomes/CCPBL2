<?php

class Patient{

    public Sensor $sensor;
    public $id;
    public $state;

    public function __construct($sensor, $id){
        $this->sensor = $sensor;
        $this->id = $id;
        $this->state = $this->verifyState($this->sensor); 
    }

    public function verifyState($sensor)
    {
        if($sensor->getBloodOxygenation() <= 96)
        {
            return "Grave";
        }
        else
        {
            return "Estável";
        } 
    }

    public function getPacientState()
    {
        return $this->state;
    }

    public function getPatientSensor()
    {
        return $this->sensor;
    }

    public function getPatientID(){
        return $this->id;
    }

    public function generateNormalValuesSensor()
    {
        $this->sensor->setTemperature(random_int(360, 380)/10);
        $this->sensor->setRespiratoryRate(random_int(9, 14));
        $this->sensor->setHeartRate(random_int(51, 100));
        $this->sensor->setBloodOxygenation(random_int(97, 99));
        $this->sensor->setArterialPressure(random_int(100, 120));
        $this->state = $this->verifyState($this->sensor);
    }

    public function generateMediumValuesSensor()
    {
        $this->sensor->setTemperature(random_int(370, 390)/10);
        $this->sensor->setRespiratoryRate(random_int(12, 22));
        $this->sensor->setHeartRate(random_int(100, 112));
        $this->sensor->setBloodOxygenation(random_int(90, 97));
        $this->sensor->setArterialPressure(random_int(80, 100));
        $this->state = $this->verifyState($this->sensor);
    }

    public function generateLargeValuesSensor()
    {
        $this->sensor->setTemperature(random_int(380, 400)/10);
        $this->sensor->setRespiratoryRate(random_int(9, 29));
        $this->sensor->setHeartRate(random_int(51, 129));
        $this->sensor->setBloodOxygenation(random_int(30, 96));
        $this->sensor->setArterialPressure(random_int(71, 110));
        $this->state = $this->verifyState($this->sensor);
    }

}