import socket
import requests

def handle_client(client_socket):
    target_url = 'http://localhost'
    while True:
        data = client_socket.recv(1024) #buffer size 1024 bytes, can adjust
        if not data:
            break #if no data received connection closedk
        # fwd received data to target target_url
        command, payload = parse_data(data) #define the parse data # -*- coding: utf-8 -*-
        response = handle_command(command, payload) # define the handle_Command fn
        requests.post(target_url, data=data)
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AT_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)
    print('Server is listening on port 5000')
    while True:
        client_socket, _ = server_socket.accept()
        handle_client(client_socket)


start_server()
