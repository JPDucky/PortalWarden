import asyncio
import socket
import evdev
from evdev import ecodes

SERVER_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 20001


mouse = evdev.InputDevice('/dev/input/event5')
keyboard = evdev.InputDevice('/dev/input/event2')

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

async def print_events(device):
    async for event in device.async_read_loop():
        message = str.encode(f"{evdev.categorize(event)}")
        print(message)
        clientSock.sendto(message, (SERVER_ADDRESS, UDP_PORT_NO))

async def mouse_events(device):
    async for event in device.async_read_loop():
        if event.type == evdev.ecodes.EV_REL:
            if event.code in [evdev.ecodes.REL_X, evdev.ecodes.REL_Y]:
                message = str.encode(f"{evdev.categorize(event)}")
                clientSock.sendto(message, (SERVER_ADDRESS, UDP_PORT_NO))



async def events_send(mouse, keyboard):
    asyncio.create_task(mouse_events(mouse))
    asyncio.create_task(print_events(keyboard))

    # loop = asyncio.get_event_loop()
    # await loop.run_forever()
    await asyncio.Future()

asyncio.run(events_send(mouse, keyboard))

# while True:
#TODO: have the "Truth" be whether or not the mouse has crossed the event horizon or the key combo has been released


# for evdev, to get exclusive access to input events, use:
# dev.grab()
# dev.ungrab()


