import socket
import sys

if __name__ == "__main__":
	vmNum = sys.argv[1]
	HOST = 'fa18-cs425-g45-' + vmNum + '.cs.illinois.edu'
	print HOST
	PORT = 12345
	print PORT

	print 'Connecting to {one} at port {two}'.format(one=HOST,two=PORT)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.sendall(b'Hello world')
	data = s.recv(1024)

	print('Received', repr(data))
