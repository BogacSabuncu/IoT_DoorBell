import socket
import select

host = "127.0.0.1"
port=5050

mysocket = socket.socket()
mysocket.bind((host,port))
mysocket.settimeout(5)
#mysocket.listen(1)

isFact = True
try:
	mysocket.listen(1)
	conn, addr = mysocket.accept()
	while isFact:
		data = conn.recv(1024).decode()
		print ("the data is " + str(data))
		if (str(data) =="this works all right"):
			mysocket.close()
			conn.close()
			isFact=False
except socket.timeout:
	print ("well, it timed out allright")
	
print ("out of while")
num =1
for i in range (0,10):
	num*=2
print (num)
