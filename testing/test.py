import asyncio
import socket
import evdev

SERVER_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 20001

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

device = evdev.InputDevice('/dev/input/event5')  # Replace with your device's event number

async def get_events()(device):
    async for event in device.async_read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            if event.code in [evdev.ecodes.ABS_X, evdev.ecodes.ABS_Y, evdev.ecodes.ABS_MT_POSITION_X, evdev.ecodes.ABS_MT_POSITION_Y]:
                message = str.encode(f"Absolute axis event: code={event.code}, value={event.value}")
                clientSock.sendto(message, (SERVER_ADDRESS, UDP_PORT_NO))

async def events_send():
    asyncio.create_task(get_events()(device))
    await asyncio.Future()

asyncio.run(events_send())

