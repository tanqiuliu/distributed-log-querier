import socket
import sys
from dlq_querier import *
from Socket import *

PORT = 12345
BUF_SIZE = 4096

def parser_msg(msg):
    msg_d = msg.decode()
    pattern = msg_d.split(' ')[0]
    filename = msg_d.split(' ')[1]
    return pattern, filename

if __name__ == "__main__":
    s = TCPSocket()
    s.bind(('', PORT))
    s.listen(10)

    while True:
        c, addr = s.accept()
        msg = c.sock.recv(BUF_SIZE)
        pattern, filename = parser_msg(msg)
        # do query
        #query_result = doQuery(pattern, filename)
        for output in doQuery2(pattern, filename):
            c.send(output.encode())
        c.close()



