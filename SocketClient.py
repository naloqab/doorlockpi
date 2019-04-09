import socket

Host = '192.168.1.220'
Port = 5007

print ""
while 1:
	InputData = raw_input("Enter data to send across: ")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((Host, Port))
	s.sendall(InputData)
	data = s.recv(1024)
	s.close()
	print InputData
