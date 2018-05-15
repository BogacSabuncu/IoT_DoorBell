#!/usr/bin/env python
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import json
from time import sleep

def sendMQTT(topicIndex, lightStatus):
    #Setting up MQTT Client
    myMQTTClient = AWSIoTMQTTClient("piPythonClientID")
    myMQTTClient.configureEndpoint("a1hd20ncaxgeuh.iot.us-east-1.amazonaws.com", 8883)
    myMQTTClient.configureCredentials("certs/piKeys/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem",
                                        "certs/piKeys/12d0293db7-private.pem.key", "certs/piKeys/12d0293db7-certificate.pem.crt")
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    #get info from arguments to determine whether to turn on/off light and on which board
    topicIndex =  topicIndex          #int(sys.argv[1])
    lightStatus = lightStatus          #int(sys.argv[2]) % 2
    topics = ["mbed/put/mbed-endpoint/43e34372-64af-4946-a448-546905a29b88/311/0/5850","sdk/test"]
    topic = topics[topicIndex]
    topicEndpoints = ["43e34372-64af-4946-a448-546905a29b88/311/0/5850","43e34372-64af-4946-a448-546905a29b88"]

    payload = {}
    payload['path'] = "/311/0/5850"
    payload['ep'] = topicEndpoints[1]
    payload['new_value'] = lightStatus
    payload['coap_verb'] = 'put'
    payloadJson = json.dumps(payload)
    #print(payloadJson)

    #Connecting to MQTT Server
    myMQTTClient.connect()
    myMQTTClient.publish(topic, payloadJson, 1)
    myMQTTClient.disconnect()
    print("Sent MQTT Message")
#sendMQTT(1,1)
#sendMQTT(0,1)
#sleep(1)
#sendMQTT(0,0)
