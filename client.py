# The clients will be the hosts RECEIVING events

import asyncio
import socket
import evdev
from evdev import ecodes

SERVER_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 20001

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# TODO: connect to socket
# TODO: receive mouse events
# TODO: send input to desktop

async def events_send(mouse, keyboard):
    asyncio.create_task(mouse_events(mouse))
    asyncio.create_task(get_events()(keyboard))

    # loop = asyncio.get_event_loop()
    # await loop.run_forever()
    await asyncio.Future()

asyncio.run(events_send(mouse, keyboard))


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
