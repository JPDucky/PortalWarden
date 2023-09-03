import socket

HOST = "127.0.0.1"

PORT_UDP = 20001

PORT_TCP = 20002

UDPserverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

TCPserverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# now bind declared address to freshly declared server sock
UDPserverSock.bind((HOST, PORT_UDP))
TCPserverSock.bind((HOST, PORT_TCP))

while True:
    data, addr = UDPserverSock.recvfrom(1024)
    data, addr = TCPserverSock.recvfrom(1024)
    print(data)
