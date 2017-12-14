import os
import socket
import select
import sys
import json
import threading
import Queue

server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)        
            
            else:
                header = []           
                data = sock.recv(1024)
                data = data.strip('\n')
                print data
                data = data.split(' ',1)
                os.chdir('filenya')
                if data[0] == 'unduh':
                    header.append(data[1])
                    size = os.path.getsize(data[1])
                    header.append(size)
                    header.append(client_address)
                    head=json.dumps(header)
                    parse = ("client address : "+header[2][0]+" : "+str(header[2][1]) + "\nfile-size : "+str(header[1])+"\n\n\n")
                    print parse
                    sock.send(head)
                    x_file = open(data[1], "rb")
                    x_file = x_file.read()    
                    if data[1]:
                        sock.send(x_file)
                    else:
                        sock.close()
                        input_socket.remove(sock)
                    os.chdir('..')
                else:
                    print "GAGAL!"
                    sys.exit()

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)