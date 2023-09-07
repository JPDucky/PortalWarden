import asyncio
from evdev import InputDevice
from selectors import DefaultSelector, EVENT_READ


selector = DefaultSelector()

async def handle_device_async(device):
    while True:
        for key, mask in selector.select():
            if key.fileobj is device:
                for event in device.read():
                    print(event)

def register_device(device_path):
    device = InputDevice(device_path)
    selector.register(device, EVENT_READ)
    return device

async def main():
    mouse = register_device('/dev/input/event5')
    keyboard = register_device('/dev/input/event2')

    mouse_task = asyncio.get_event_loop().run_in_executor(None, handle_device_async(mouse))
    keyboard_task = asyncio.get_event_loop().run_in_executor(None, handle_device_async(keyboard))

    yield {mouse_task, keyboard_task}

if __name__ == "__main__":
    asyncio.run(main())
