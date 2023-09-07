# The clients will be the hosts RECEIVING events

import asyncio
import socket
import .main

SERVER_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 20001


# TODO: connect to socket
# TODO: receive mouse events
# TODO: send input to desktop

class UDPServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue):
        #import event queue from main.py
        self.queue = queue
        super().__init__()

    async def start_sending(self):
        while True:
            event = await self.queue.get()
            msg = f"Processed: {event}"
            self.transport.sendto(msg.encode(), self.client_addr)

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        print(f"Received {data.decode()} from {addr}")
        self.client_addr = addr #save clients addr to use it in start_sending()

    def connection_lost(self, exc):
        print("Socket closed, stopping event loop")

async def main(loop):
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(event_queue),
        local_addr=({SERVER_ADDRESS}, {UDP_PORT_NO})
    )
    loop.create_task(get_events(event_queue))
    loop.create_task(protocol.start_sending())

    while True:
        print(f"current size of event queue:" {event_queue.qsize()})

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()
















# async def events_send(mouse, keyboard):
#     asyncio.create_task(mouse_events(mouse))
#     asyncio.create_task(get_events()(keyboard))
#
#     # loop = asyncio.get_event_loop()
#     # await loop.run_forever()
#     await asyncio.Future()
#
# asyncio.run(events_send(mouse, keyboard))
#
#
# def handle_server(UDPClientSock):
#     UDPserverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)





# async def get_events()(device):
#     async for event in device.async_read_loop():
#         message = str.encode(f"{evdev.categorize(event)}")
#         print(message)
#         clientSock.sendto(message, (SERVER_ADDRESS, UDP_PORT_NO))
#
# async def mouse_events(device):
#     async for event in device.async_read_loop():
#         if event.type == evdev.ecodes.EV_REL:
#             if event.code in [evdev.ecodes.REL_X, evdev.ecodes.REL_Y]:
#                 message = str.encode(f"{evdev.categorize(event)}")
#                 clientSock.sendto(message, (SERVER_ADDRESS, UDP_PORT_NO))
