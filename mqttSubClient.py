from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import os
from picamera import PiCamera
from time import sleep, strftime
import bogac
import gitUpdate
import mqttPubClient
#import TwilioFunctionality
import time
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
import subprocess
from multiprocessing import Process, Value
from datetime import datetime
import signal
import socket
#import TwilioFunctionality

#STATES = ['processImage','sendTwilio','recieveTwilio','openDoor','idle']
#CALLERS = ['Dan','josh','Bogac']
STATE = 'idle'
CALLER = ''
subprocess.Popen(['/home/pi/ec500/project/Group10/run_ngrok.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
def CheckBaseWithUser(SupposedPerson, Caller):

	account_sid = "AC9df18367390e313f33f46f2c14600478"
	auth_token = "1fd70198f932c3877b3fbe74f263abd3"
	numberToSend = ""
	
	
	media = "https://github.com/DanielOved/DoorBellLabs/blob/master/latest.jpg?raw=true" 
	
	if(Caller == "Bogac"):
		numberToSend="+18573649868"
	elif(Caller == "Josh"):
		numberToSend=="+16175485911"	
	elif(Caller == "Dan"):
		numberToSend="+12146841686"
	elif(Caller == "josh"):
		numberToSend="+16175485911"
			
	client = Client(account_sid, auth_token)
	print ("The number is")
	print (numberToSend)
	print("the caller is")
	print(Caller)
	ListOfNames= ["Dan", "Josh", "Mahesh"]
	NameTest =  ["Josh","Dan","Eric"]
	
	lengthOfArr = len(SupposedPerson)
	messageToSend=""
	if(lengthOfArr==2):
		names = " and ".join(SupposedPerson)
	else:
		names = " and ".join(SupposedPerson)
	if(lengthOfArr==0):
		messageToSend = "I cannot see who it is, would you like to open the door anyways? Please respond 'Yes' or 'No'"
	elif(lengthOfArr==1):
		messageToSend="{} is at the door. Would you like to let them in? Please respond 'Yes' or 'No'.".format(names)
	elif(lengthOfArr>1):
		messageToSend="{} are at the door. Would you like to let them in? Please respond 'Yes' or 'No'.".format(names)
	
	client.api.account.messages.create(
	    to=numberToSend, #
	    from_="+18572142872",
	    body=messageToSend, 
	    media_url=media
	)
	print ("message sent")

def captureImage():
    #Setup camera
    camera = PiCamera()
    camera.rotation = 0
    #take picture
    imageName = '/home/pi/ec500/project/Group10/images/img%s.jpg'%(strftime("-%m%d-%H%M%S"))
    camera.capture(imageName)
    camera.close()
    try:
        os.unlink("/home/pi/ec500/project/Group10/images/latest.jpg")
    except:

        #Do nothing
        pass
    os.symlink(imageName, "/home/pi/ec500/project/Group10/images/latest.jpg")
    print("Captured Image")

#Setup MQTT topics
danButton ="iotbutton/G030MD046432Q4F1"
joshButton = "iotbutton/G030MD0452227TWK"
bogacButton = "iotbutton/G030MD042164MXRM"

def callback(client, userdata, message):
    global STATE
    global CALLER
    if message.topic == danButton:
        print("Dan's Button")
        STATE = "processImage"
        CALLER = "Dan"

    elif message.topic == joshButton:
        print("Josh's Button")
        STATE = "processImage"
        CALLER = "josh"

    elif message.topic == bogacButton:
        print("Bogac's Button")
        STATE = "processImage"
        CALLER = "Bogac"

    else:
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
    print("--------------\n")


#Setting up MQTT Client
myMQTTClient = AWSIoTMQTTClient("piPythonClientID")
myMQTTClient.configureEndpoint("a1hd20ncaxgeuh.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("certs/piKeys/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem",
                                    "certs/piKeys/12d0293db7-private.pem.key", "certs/piKeys/12d0293db7-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#Connecting to MQTT Server
myMQTTClient.connect()
myMQTTClient.subscribe(danButton, 1, callback)
myMQTTClient.subscribe(joshButton, 1, callback)
myMQTTClient.subscribe(bogacButton, 1, callback)
myMQTTClient.subscribe("sdk/#", 1, callback)

print("MQTT Subscription set up")
app = Flask(__name__)
#Setting up the facial recognition for knownpeople
known_images, known_names, known_image_encodings = bogac.data_prep()
print("Done encoding images")




while True:
	if(STATE == 'idle'):
		#proc.kill()
		continue
	elif(STATE == 'processImage'):
		print(STATE)
		captureImage()
		#get the unknown image
		unknown_image, face_locations, face_encodings = bogac.unknown_image_prep()
		#draw the square with names
		names = bogac.draw_image(unknown_image, face_locations, face_encodings, known_image_encodings, known_names)
		
		print(names)
		print("CALLER is " + CALLER)
		#upload modified image to github URL
		print("Uploading img to github")
		gitUpdate.uploadImage()
		sleep(20)
		STATE = 'sendTwilio'
	elif(STATE == 'sendTwilio'):
		print(STATE)
		#josh's stuff
		CheckBaseWithUser(names,CALLER)
		#send CALLER as arg so you know who to send text to

		STATE = 'recieveTwilio'
	elif(STATE == 'recieveTwilio'):
		print(STATE)
		
		smsState = 0
		
		print("Server Start")
		#server.start()
		
		NAMES_ = str(names)
		cmd = ["python", "/home/pi/ec500/project/Group10/Twilio_saved.py"," " , str(NAMES_), " " ,  CALLER]
		#cmd = "python /home/pi/ec500/project/Group10/TwilioFunctionality.py " +  str(NAMES_) + " "  +  CALLER
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		host = '127.0.0.1'
		port = 5050
		mysocket = socket.socket()
		mysocket.bind((host,port))
		mysocket.settimeout(60)
		
		try:
			mysocket.listen(1)
			conn, addr = mysocket.accept()
			
			
			data = conn.recv(1024).decode()
			print ("the data is this homie: " + str(data))
			if(str(data) == "double yes"):
				
				conn.close()
				mysocket.close()
				STATE = 'openDoor'
			if(str(data)=="not sure"):
				print("in not sure, retaking picture")
				
				conn.close()
				mysocket.close()
				STATE = 'sendTwilio'
				proc.kill()
		except socket.timeout:
			print ("timed out, continue running pls")
			
			conn.close()
			mysocket.close()
			proc.kill()
			STATE = 'idle'
		print(STATE)
		noCounter = 0
		yesCounter=0

	elif(STATE == 'openDoor'):
		proc.kill()
		print(STATE)
		#send mqtt msg
		mqttPubClient.sendMQTT(0,1)
		sleep(3)
		mqttPubClient.sendMQTT(0,0)
		STATE = 'idle'
	else:
		STATE = 'idle'
		sleep(1)


