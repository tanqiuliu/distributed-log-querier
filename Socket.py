import socket
import select

#The functions of this class are made to make it easier to work with the buffer for message sending very long files
class TCPSocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host_port):
        self.sock.connect(host_port)
    
    def close(self):
        self.sock.close()

    def send(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

	#A fix to the message being sent from server to client using a buffer, or else the message will be sent cut off
    def recv(self, msgLen):
        chunks = []
        bytes_recd = 0
        while bytes_recd < msgLen:
            chunk = self.sock.recv(msgLen - bytes_recd)
            if chunk == b'':
                break
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def bind(self, address_port):
        self.sock.bind(address_port)
    
    def listen(self, backlog):
        self.sock.listen(backlog)

    def accept(self):
        client_sock, client_info = self.sock.accept()
        return TCPSocket(client_sock), client_info

	#Checks to see if there is more to be sent among server to client.  Uses select to run the client-server connection in parallel with each other
    def activityDetected(self, timeout = None):
        if timeout == None:
            ready_to_read, ready_to_write, in_error = select.select([self.sock], [], [])
        else:
            ready_to_read, ready_to_write, in_error = select.select([self.sock], [], [], timeout)
        return len(ready_to_read) > 0
