import socket
import sys
from Socket import *
from functools import reduce

SERVER_PORT = 12345
MSGLEN = 4096

if __name__ == "__main__":
    # node = sys.argv[1]
    pattern = sys.argv[1]
    filename = sys.argv[2]

    # nodes = ['127.0.0.1', '18.218.231.95']
    nodes = {'localhost':'127.0.0.1' , 'aws-ec2':'18.218.231.95'}
    socks = {}
    for node in nodes:
        try:
            socks[node] = TCPSocket()
            s = socks[node]
            s.connect((nodes[node], SERVER_PORT))
            m = ' '.join([pattern, filename])
            s.send(m.encode())
        except ConnectionRefusedError as e:
            print(str(e) + ': ' + nodes[node])
            nodes[node] = None
            if node in socks:
                socks[node] = None
    buffers = {node:'' for node in nodes if nodes[node] != None}
    finish_flag = {node:False for node in nodes if nodes[node] != None}
    counts = {node:0 for node in nodes if nodes[node] != None}
    while True:
        for node in nodes:
            if nodes[node] != None:
                try:
                    if socks[node].activityDetected(5):
                        chunk = socks[node].recv(MSGLEN).decode()
                        if chunk == '':
                            finish_flag[node] = True
                            continue
                        buffers[node] += chunk
                        records = buffers[node].split('\n')
                        for i in range(len(records) - 1):
                            print(nodes[node] + ': ' + records[i])
                            counts[node] += 1
                        buffers[node] = records[-1]
                    else:
                        finish_flag[node] = True
                        continue
                except ConnectionRefusedError as e:
                    print(str(e) + ': ' + node)
                    finish_flag[node] = True
        #print(finish_flag)
        if reduce((lambda x,y:x or y), [finish_flag[node] for node in finish_flag]):
            print(counts)
            break