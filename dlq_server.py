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

#Parses the grep options and flags from client to something readable for the server
def parser_grep(grepcmd):
	grepcmd_d = grepcmd.decode('utf-8')
	return grepcmd_d
								
#Runs the server and waits for the connection to happen, then sends the output from the grep subprocess to the client.
if __name__ == "__main__":
    s = TCPSocket()
    s.bind(('', PORT))
    s.listen(10)

    while True:
        c, addr = s.accept()
        msg = c.sock.recv(BUF_SIZE)
        grep_cmd = parser_grep(msg)
        # do query
        print(grep_cmd)
        #query_result = doQuery(pattern, filename)
        for output in callGrepOnVM(grep_cmd):
            c.send(output.encode())
        c.close()
        



