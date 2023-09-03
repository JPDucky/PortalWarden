import socket

HOST = "0.0.0.0"

PORT_UDP = 20001

PORT_TCP = 20002

UDPserverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
TCPserverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# now bind declared address to freshly declared server sock
UDPserverSock.bind((HOST, PORT_UDP))
TCPserverSock.bind((HOST, PORT_TCP))

TCPserverSock.listen()
conn, addr = TCPserverSock.accept()

while True:
    udp_data, udp_addr = UDPserverSock.recvfrom(1024)
    tcp_data = conn.recv(1024)
    print("UDP data:", udp_data)
    print("TCP data:", tcp_data)
