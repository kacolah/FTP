import socket
import json
import sys
from math import ceil
import os
import threading
import Queue

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
	while True:
		message = sys.stdin.readline()
		client_socket.send(message)
		total_data = []
		header = json.loads(client_socket.recv(1024))
		parse = ("client address : "+header[2][0]+" : "+str(header[2][1]) + "\nfile-size : "+str(header[1])+"\n\n\n") 
		print parse
		loop = int(ceil(header[1]/1024.0))
		for i in range (loop):
			data = client_socket.recv(1024)
			total_data.append(data)
		os.chdir('unduhan')
		with open(header[0], 'wb') as outfile:
			outfile.write(''.join(total_data))
			os.chdir('..')
		sys.stdout.write('>> ')

except KeyboardInterrupt:
	client_socket.close()
	sys.exit(0)