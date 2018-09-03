import socket
import sys

PORT = 23333
BUF_SIZE = 4096

def query(pattern, filename):
    print("query function called: %s, %s" %(pattern, filename))

def parser_msg(msg):
    msg_d = msg.decode()
    pattern = msg_d.split(' ')[0]
    filename = msg_d.split(' ')[1]
    return pattern, filename

if __name__ == "__main__":
    s = socket.socket()
    s.bind(('', PORT))
    s.listen(10)

    while True:
        c, addr = s.accept()
        msg = c.recv(BUF_SIZE)
        pattern, filename = parser_msg(msg)
        # do query
        query(pattern, filename)
        rtn_msg = 'receipt from %s to %s' %(socket.gethostname(), c.getpeername())
        c.send(rtn_msg.encode())
        c.close()



