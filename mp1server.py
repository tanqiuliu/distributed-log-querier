import socket
import sys

if __name__ == "__main__":
	vmNum = sys.argv[1]
	HOST = 'fa18-cs425-g45-' + vmNum + '.cs.illinois.edu'
	print HOST
	PORT = 12345
	print PORT

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('', PORT))
	print 'Server name is {one} at port {two}'.format(one=HOST,two=PORT) 
	s.listen(1)
	conn, addr = s.accept()
	print('Connected by', addr)
	
	while True:
		data = conn.recv(1024)
		if not data:
			break
		conn.sendall(data)
