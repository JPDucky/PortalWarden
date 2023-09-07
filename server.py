# The Server will be the host SENDING events
import asyncio
from main import get_events, event_queue

HOST = "127.0.0.1"
PORT_UDP = 20001
client = []

UDPserverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPserverSock.bind((HOST, PORT_UDP))

# TODO: get mouse events from main
# TODO: get keyboard events from main

def inputs_to_send():
    main.

def handle_client(UDPserverSock):
    while True:
        udp_data, udp_addr = UDPserverSock.sendto(1024)

        # command, payload = parse_data(udp_data, udp_addr)
        # response = handle_command(command, payload)



def start_server():

    print(f'Server is listening on port {PORT_UDP}')
    while True:
        handle_client(UDPserverSock)


if __name__ == "__main__":
    start_server()

