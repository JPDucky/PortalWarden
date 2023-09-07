# The Server will be the host SENDING events

import socket
import requests

HOST = "127.0.0.1"
PORT_UDP = 20001

def handle_client(UDPserverSock):
    while True:
        udp_data, udp_addr = UDPserverSock.recvfrom(1024)
        print("UDP data:", udp_data)

        if not udp_data:
            break

        # command, payload = parse_data(udp_data, udp_addr)
        # response = handle_command(command, payload)



def start_server():
    UDPserverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPserverSock.bind((HOST, PORT_UDP))

    print(f'Server is listening on port {PORT_UDP}')
    while True:
        handle_client(UDPserverSock)


if __name__ == "__main__":
    start_server()

