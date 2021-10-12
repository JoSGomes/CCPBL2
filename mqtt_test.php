<?php
require "vendor/autoload.php";
use \PhpMqtt\Client\MqttClient;

$server   = '127.0.0.1';
$port     = 1883;
$clientId = rand(5, 15);
$clean_session = false;

$mqtt = new MqttClient($server, $port, $clientId);
$mqtt->connect();
$mqtt->subscribe('main', function ($topic, $message) use ($mqtt){
    echo sprintf("Received message on topic [%s]: %s\n", $topic, $message);
    $mqtt->interrupt();
}, 0);

$input = fgets(STDIN);

$mqtt->loop(true);
$mqtt->disconnect();
