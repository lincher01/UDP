#!/usr/bin/python
from socket import *
import sys
import os
import time


## some code from computer networking by Kurose and ross
serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print("The server is ready to receive")
while True:
	
	length, clientAddress = serverSocket.recvfrom(2048)

	message, clientAddress = serverSocket.recvfrom(2048)
	
	## get decoded message and length
	dLength = length.decode()
	## starting time
	
	start = time.time()
	end = time.time()
	ack_check = False

	ACK = "ACK"
	# checking if it's been more than 500 ms
	while(end - start < 0.5):
		end = time.time()
		if (str(len(message)) == dLength):
			ack_check = True
			serverSocket.sendto(ACK.encode(), clientAddress)
			# print("server - in while loop if")
			break

	# print("server - out of while loop")

	if ack_check == False:
		# print("server - ack_check is false")
		fail = "Failed to receive instructions from the client"
		serverSocket.sendto(fail.encode(), clientAddress)

	elif ack_check == True:
		# print("server - ack_check is true")
		decoded_message = message.decode()
		substring = '>'
		if substring in decoded_message:
			# print("server - given file")
			found = decoded_message[decoded_message.find('>')+1:]
			os.system(decoded_message)
		else:
			# print("server - no > found")
			found = "UDPresults.txt"
			os.system(decoded_message + ' > UDPresults.txt')

	# print("server - sending message back")
	serverSocket.sendto(found.encode(), clientAddress)