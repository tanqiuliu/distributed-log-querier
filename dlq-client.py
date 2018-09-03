import socket
import sys

SERVER_PORT = 23333
BUF_SIZE = 4096

if __name__ == "__main__":
    node = sys.argv[1]
    pattern = sys.argv[2]
    filename = sys.argv[3]

    s = socket.socket()
    s.connect((node, SERVER_PORT))
    m = ' '.join([pattern, filename])
    s.send(m.encode())
    rtn_msg = s.recv(BUF_SIZE)
    print(rtn_msg.decode())