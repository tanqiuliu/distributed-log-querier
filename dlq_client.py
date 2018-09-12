import socket
import sys
from Socket import *

SERVER_PORT = 12345
BUF_SIZE = 4096

if __name__ == "__main__":
    node = sys.argv[1]
    pattern = sys.argv[2]
    filename = sys.argv[3]

    s = TCPSocket()
    try:
        s.connect((node, SERVER_PORT))
        m = ' '.join([pattern, filename])
        s.send(m.encode())
        # recv
        chunks = []
        while True:
            if s.activityDetected(5):
                chunk = s.recv(BUF_SIZE)
                if chunk == b'':
                    break
                chunks.append(chunk)
            else:
                break
        rtn_msg = b''.join(chunks)

        print(rtn_msg.decode())
    except ConnectionRefusedError as e:
        print(str(e) + ': ' + node)