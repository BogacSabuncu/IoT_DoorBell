
from twilio.rest import Client
import sys
from flask import Flask, request
from twilio.twiml.messaging_response import Message, MessagingResponse
import subprocess
import sys

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
	global IdentifiedPerson
	global ButtonPresser
	#RasPiPic = FacePic
	#IdentifiedPerson = SupposedPerson
	#ButtonPresser = Caller
	# Find these values at https://twilio.com/user/account
	account_sid = "####"
	auth_token = "#####"
	numberToSend = ""
	#media = "http://www.bu.edu/lernet/cyber/years/2016/images/Assel.jpg"

	media = "https://raw.githubusercontent.com/BUConnectedWorld/Group10/master/images/latest.jpg?token=AL985lggk690chx9t_kXaQ7H68IX9aYLks5a7oAdwA%3D%3D" #"https://raw.githubusercontent.com/mattmakai/fullstackpython.com/master/static/img/logos/f.png" #edit interactively, allow this to be an arg
	if(Caller == "Bogac"):
		numberToSend="+####"	
	elif(Caller == "Dan"):
		numberToSend="+#####"
	elif(Caller == "josh"):
		numberToSend="+####"
		#print "I entered this if statement"
	
	client = Client(account_sid, auth_token)
	print "The number is"
	print numberToSend
	ListOfNames= ["Dan", "Josh", "Mahesh"]
	NameTest =  ["Josh","Dan","Eric"]
	
	lengthOfArr = len(NameTest)
	messageToSend=""
	if(lengthOfArr==2):
		names = " and ".join(NameTest)
	else:
		names = " and ".join(NameTest)
	if(lengthOfArr==0):
		messageToSend = "I cannot see who it is, would you like to open the door anyways? Please respond 'Yes' or 'No'"
	elif(lengthOfArr==1):
		messageToSend="{} is at the door. Would you like to let them in? Please respond 'Yes' or 'No'.".format(names)
	elif(lengthOfArr>1):
		messageToSend="{} are at the door. Would you like to let them in? Please respond 'Yes' or 'No'.".format(names)
	
	client.api.account.messages.create(
	    to=numberToSend, #
	    from_="+####",
	    body=messageToSend, #SupposedPerson
	    media_url=media
	)
		
	

CheckBaseWithUser(sys.argv[1],sys.argv[2])
app = Flask(__name__)
#subprocess.Popen(['./run_ngrok.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
noCounter = 0
yesCounter=0
smsState = False
@app.route('/sms', methods=['POST'])
def server_shutdown():
	
def sms():
    global noCounter
    global yesCounter
    global FacePic
    #smsState=True
    global SupposedPerson
    global smsState
    number = request.form['From']
    message_body = request.form['Body']
    print message_body
    #Enter State Machine
    if(noCounter<=0 and yesCounter <=0):
		if((message_body=="yes" or message_body=="Yes")):
			print "Alrighty"
			YesMsg=MessagingResponse()
			YesMsg.message("Are you sure? Please respond 'Yes' or 'No'. Please note that a 'Yes' response will result in the door unlocking, while a 'No' will resend you the picture")
			yesCounter+=1
			return str(YesMsg)
	
		elif((message_body=="No" or message_body=="no")):
			NoMsg = MessagingResponse()
			NoMsg.message("Are you sure? Please respond 'Yes' or 'No'. Please note that a 'Yes' response will not open the door, while a 'No' will resend you the picture")
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
			noCounter = 0
			FacePic=""
			smsState=True
			SupposedPerson = []
			
			#implement door unlocking.
			return str(UnlockingMsg)
		elif(message_body=="No" or message_body=="no"):
			yesCounter=0
			#print "I entered the yes category"
			CheckBaseWithUser(sys.argv[1],sys.argv[2])   #NOTE: Change args
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
			yesCounter = 0
			SupposedPerson=[]
			FacePic=""
			smsState=False
			return str(ReassuringMsg)
			#red LED or something
		elif(message_body=="No" or message_body=="no"):
			noCounter=0
			#print "I entered the no category"
			CheckBaseWithUser(sys.argv[1],sys.argv[2])	#NOTE: Change args: FacePic
			#go back to the beginning
		else:
			InvalidMessage = MessagingResponse()
			InvalidMessage.message("Invalid response.  Please respond 'Yes' or 'No'.")
			return str(InvalidMessage)
'''
    resp = MessagingResponse()
	#change this so that it matches the simple sending thing Twiliotest.py
    msg =resp.message('Hello {}, you said: {}'.format(number, message_body))
	#resp.Media('https://raw.githubusercontent.com/mattmakai/fullstackpython.com/master/static/img/logos/f.png')
    print "I work fine, thank you"*3
    print (noCounter)
    msg.media('https://raw.githubusercontent.com/mattmakai/fullstackpython.com/master/static/img/logos/f.png')
    return str(resp)
           '''
           
if __name__ == '__main__':
    app.run()


