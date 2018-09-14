import socket
import sys
from Socket import *
from functools import reduce
import json
import copy

SERVER_PORT = 12345
MSGLEN = 4096

if __name__ == "__main__":
    pattern = sys.argv[1:]

    with open('./conf.json','r') as handle:
        nodes = json.loads(handle.read())

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
            print(str(e) + ': ' + node['name'] + ' ' + node['ip'])
            node['status'] = False
            node['complete'] = True

    while True:
        for node in nodes:
            if node['status'] and not node['complete']:
                try:
                    if node['sock'].activityDetected(5):
                        chunk = node['sock'].recv(MSGLEN).decode()
                        if chunk == '':
                            print("Finished receiving stuff")
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
        #print(finish_flag)
        if reduce((lambda x,y:x and y), [node['complete'] for node in nodes]):
            for node in nodes:
                print(node)
            break
