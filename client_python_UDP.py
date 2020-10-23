#!/usr/bin/python
from socket import *
import time

## line 2,3,6,38,63 from computer networking by Kurose and ross
clientSocket = socket(AF_INET, SOCK_DGRAM)
IP = input('Enter server name or IP address: ')
port = input('Enter port: ')

if (int(port)<0) | (int(port)>65535):
	print("Invalid port number")
	clientSocket.close()
	exit()

try:
	clientSocket.connect((IP, int(port)))
except:
	print("Could not connect to server")
	exit()

command = input('Enter command: ')
clength = str(len(command))

## sending length of message
clientSocket.sendto(clength.encode(), (IP, int(port)))
##sending message
# print(command.encode())
clientSocket.sendto(command.encode(), (IP, int(port)))
acked = False

for i in range(3):
	# print("client - in for loop starting timer")
	start = time.time()
	end = time.time()
	while(end - start < 1):
		end = time.time()
		# print("client - in while loop getting server info")
		modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
		# print("client - got message")

		if(modifiedMessage.decode() == 'ACK'):
			# print("client - got ack!")
			acked = True
			break

	if(acked == True):
		break

	if(end - start > 1 and modifiedMessage.decode() != 'ACK'):
		# print("client - did not get ACK resending command")
		clientSocket.sendto(command.encode(), (IP, int(port)))


# print("client - out of for loop")

if acked == False:
	print("Failed to send command. Terminating.")

else:
	savedfile, serverAddress = clientSocket.recvfrom(2048)
	print("File " + savedfile.decode() + " saved")

clientSocket.close()