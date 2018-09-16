import socket
import sys
from Socket import *
from functools import reduce
import json
import copy

SERVER_PORT = 12345
MSGLEN = 4096

#Client main function that connects to a server with given HOST and PORT
def connect_to_server(pattern, filename='./conf.json'):
	#Opens a file to see the ip to connect, the ip's name, and the path to the file we want to grep
    with open(filename,'r') as handle:
        nodes = json.loads(handle.read())

	#Goes through every ip in order to try to connect an run grep on the virtual machines.  If we cannot connect we just 
	#set it to complete with an error.  Connection with 0 lines will print out 0 lines while errors will print out error.
    for node in nodes:
        node['buffer'] = ''
        node['complete'] = False
        node['count'] = 0
        try:
            node['sock'] = TCPSocket()
            node['sock'].connect((node['ip'], SERVER_PORT))
            patterncopy = copy.deepcopy(pattern)
            patterncopy.append(node['logfile'])
            m = ' '.join(patterncopy)
            node['sock'].send(m.encode())
            node['status'] = True
        except ConnectionRefusedError as e:
            node['status'] = False
            node['complete'] = True

	#Checks to see that the server is still sending messages to the client, if so then we want to store the messages
	#in the buffer and print them out.  Once the program is done printing everything that the servers have sent to client,
	#it will then print if the vm encountered an error or the line count of the grep commnand.
    while True:
        for node in nodes:
            if node['status'] and not node['complete']:
                try:
                    if node['sock'].activityDetected(5):
                        chunk = node['sock'].recv(MSGLEN).decode()
                        if chunk == '':
                            node['complete'] = True
                            continue
                        node['buffer'] += chunk
                        records = node['buffer'].split('\n')
                        for i in range(len(records) - 1):
                            print(node['name'] + ': ' + records[i])
                            node['count'] += 1
                        node['buffer'] = records[-1]
                    else:
                        node['complete'] = True
                        continue
                except ConnectionRefusedError as e:
                    print(str(e) + ': ' + node['name'])
                    node['status'] = False
                    node['complete'] = True

        if reduce((lambda x,y:x and y), [node['complete'] for node in nodes]):
            for node in nodes:
                if not node['status']:
                    print(node['name'] + " encountered an error.")
                else:
                    print(node['name'] + " finished with " + str(node['count']) + " lines")
            break
    return nodes
	

if __name__ == "__main__":
    pattern = sys.argv[1:]
    connect_to_server(pattern)

    

