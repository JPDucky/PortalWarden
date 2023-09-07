import asyncio
import evdev

mouse = evdev.InputDevice('/dev/input/event5')
keyboard = evdev.InputDevice('/dev/input/event3')

def events_send(device):
    async def get_events()(device):
        async for event in device.async_read_loop():
            print(device.path, evdev.categorize(event), sep=': ')

    for device in mouse, keyboard:
        asyncio.ensure_future(get_events()(device))

    loop = asyncio.get_event_loop()
    loop.run_forever()


# get exclusive access to input events
# dev.grab()
# dev.ungrab()
#

#TODO: implement a solution for catching the output and parsing only the necessary bits (mouse relative, value, etc.) and storing/sending them
