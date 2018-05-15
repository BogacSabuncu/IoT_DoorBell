
from twilio.rest import Client
import sys
from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
import subprocess
import sys
import socket
#note: Bogac has to pass off both name && picture
RasPiPic= ""
IdentifiedPerson = []
ButtonPresser=""
#DO NOT: write to a file, makes it impossible to know if it is passed to an array
#MediaFile = open("FaceFile.txt","r")
#PersonFile = open("PersonFile.txt","r")
#MediaFileList = MediaFile.readlines()
#PersonFileList=

def CheckBaseWithUser(SupposedPerson, Caller):
	#maybe don't need these, since they'll be my args...		
	global RasPiPic
	print ("this checks base")
	global IdentifiedPerson
	global ButtonPresser
	#RasPiPic = FacePic
	#IdentifiedPerson = SupposedPerson
	#ButtonPresser = Caller,.aaaaa
	# Find these values at https://twilio.com/user/account
	account_sid = "########"
	auth_token = "#######"
	numberToSend = ""
	#media = "http://www.bu.edu/lernet/cyber/years/2016/images/Assel.jpg"
	
	media = "https://github.com/DanielOved/DoorBellLabs/blob/master/latest.jpg?raw=true" #"https://raw.githubusercontent.com/mattmakai/fullstackpython.com/master/static/img/logos/f.png" #edit interactively, allow this to be an arg
	if(Caller == "Bogac"):
		numberToSend="+#####"
	elif(Caller == "Josh"):
		numberToSend=="+#####"	
	elif(Caller == "Dan"):
		numberToSend="+######"
	elif(Caller == "josh"):
		numberToSend="+######"
		#print "I entered this if statement"
	
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
	    from_="+#####",
	    body=messageToSend, #SupposedPerson
	    media_url=media
	)
	print ("message sent")
		
	



app = Flask(__name__)

noCounter = 0
yesCounter=0


@app.route('/sms', methods=['GET','POST'])
def sms():
	global noCounter
	global yesCounter

	#smsState=True
	global SupposedPerson
	
	number = request.form['From']
	message_body = request.form['Body']
	print (message_body)
	#Enter State Machine
	if(noCounter<=0 and yesCounter <=0):
		if((message_body=="yes" or message_body=="Yes")):

			YesMsg=MessagingResponse()
			YesMsg.message("Are you sure? Please respond 'Yes' or 'No'!")
			yesCounter+=1
			
			return str(YesMsg)
	
		elif((message_body=="No" or message_body=="no")):
			NoMsg = MessagingResponse()
			NoMsg.message("Are you sure? Please respond 'Yes' or 'No'")
			noCounter += 1
			return str(NoMsg)
		else:
			InvalidMessage = MessagingResponse()
			InvalidMessage.message("Invalid response.  Please respond 'Yes' or 'No'.")
			return str(InvalidMessage)
	
	elif(yesCounter>0):
		if(message_body=="yes" or message_body=="Yes"):
			UnlockingMsg = MessagingResponse()
			UnlockingMsg.message("All right, the door will unlock for this person.")
			yesCounter = 0
		
			SupposedPerson = []
			host = '127.0.0.1'
			port = 5050
			mysocket = socket.socket()
			mysocket.connect((host,port))
			sock_messg = "double yes"
			print(sock_messg)
			mysocket.send(sock_messg.encode())
			mysocket.close()
			#implement door unlocking.
			return str(UnlockingMsg)
		elif(message_body=="No" or message_body=="no"):
			yesCounter=0
			host = '127.0.0.1'
			port = 5050
			mysocket = socket.socket()
			mysocket.connect((host,port))
			sock_messg = "not sure"
			print(sock_messg)
			mysocket.send(sock_messg.encode())
			mysocket.close()
			RetakePicMsg = MessagingResponse()
			RetakePicMsg.message("We will retake a picture")
			return str(RetakePicMsg)
			#print "I entered the yes category"

		else:
			InvalidMessage = MessagingResponse()
			InvalidMessage.message("Invalid response.  Please respond 'Yes' or 'No'.")
			return str(InvalidMessage)

	elif(noCounter > 0):
		if(message_body=="Yes" or message_body=="yes"):
			#go to the 'go away functionality'
			ReassuringMsg= MessagingResponse()
			ReassuringMsg.message("All right, your door will not be unlocked, and the person will not be allowed in.")
			#reinit			
			noCounter = 0
			
			return str(ReassuringMsg)
			#red LED or something
		elif(message_body=="No" or message_body=="no"):
			noCounter=0
			host = '127.0.0.1'
			port = 5050
			mysocket = socket.socket()
			mysocket.connect((host,port))
			sock_messg = "not sure"
			print(sock_messg)
			mysocket.send(sock_messg.encode())
			mysocket.close()
			RetakePicMsg = MessagingResponse()
			RetakePicMsg.message("We will retake a picture")
			return str(RetakePicMsg)
			#print "I entered the no category"

			#go back to the beginning
		else:
			InvalidMessage = MessagingResponse()
			InvalidMessage.message("Invalid response.  Please respond 'Yes' or 'No'.")
			return str(InvalidMessage)
      
if __name__ == '__main__':
    app.run()


