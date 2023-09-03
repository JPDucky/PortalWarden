import asyncio
import socket
import evdev

SERVER_ADDRESS = "10.10.10.123"
UDP_PORT_NO = 20001
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mouse = evdev.InputDevice('/dev/input/event5')

keyboard = evdev.InputDevice('/dev/input/event2')


async def print_events(device):
    async for event in device.async_read_loop():
        print(device.path, evdev.categorize(event), sep=': ')
        message = str.encode(f"{evdev.categorize(event)}")
        clientSock.sendto(message, (SERVER_ADDRESS, UDP_PORT_NO))



async def events_send(mouse, keyboard):
    asyncio.create_task(print_events(mouse))
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


