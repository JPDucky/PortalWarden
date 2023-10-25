# mouse_handler/multi-device_test.py
import asyncio
from .base import BaseMouseHandler
from evdev import InputDevice, ecodes, list_devices
import evdev



# mouse = InputDevice('/dev/input/event5')
mouse = []

class device_discovery:
    def __init__(self):
        self.devices = [InputDevice(path) for path in list_devices()]
        self.mouse_devices = []

    def discover_mouse_device(self):
        for device in self.devices:
            capabilities = device.capabilities(verbose=False)
            
            if ecodes.EV_REL in capabilities:
                rel_codes = capabilities[ecodes.EV_REL]
                
                if ecodes.REL_X in rel_codes and ecodes.REL_Y in rel_codes:
                    self.mouse_devices.append(device)
                    
        return self.mouse_devices

mouse = device_discovery().discover_mouse_device()


class LinuxMouseHandler_wayland(BaseMouseHandler):
    def __init__(self, mouse_device):
        self.mouse_devices = mouse_device
        self.x = 0
        self.y = 0
        self.event_queue = asyncio.Queue()

    async def move(self):
        gather_tasks = [asyncio.create_task(self.read_device(device)) for device in self.mouse_devices]

        try:
            while True:
                event = await self.event_queue.get()
                yield event
        finally:
            # if exit, cleanup tasks
            for task in gather_tasks:
                task.cancel()

    async def read_device(self, device):
        async for event in device.async_read_loop():
            print(f"Raw event data: {event}")
            # if event.code in [evdev.ecodes.REL_X, evdev.ecodes.REL_Y]:
            if event.code == evdev.ecodes.REL_X:
                self.x = event.value
            if event.code == evdev.ecodes.REL_Y:
                self.y = event.value
            if self.x !=0: #this is here to remove the uneccesary noise/hardware softening that is created from the raw input (its a filter)
                await self.event_queue.put({'x': self.x, 'y': self.y})


async def consume_move_events(mouse_handler):
    print(f"Listening for events on device: {mouse_handler.mouse.path}")
    async for coords in mouse_handler.move():
        print(coords)



async def main():
    print("Started main")
    mouse_devices = device_discovery().discover_mouse_device()
    print(f"Type of mouse_devices: {type(mouse_devices)}")
    print(f"mouse_devices: {mouse_devices}")
    lent = len(mouse_devices)
    print(f"Number of mouse devices found: {lent}") 

    if not mouse_devices:
        print("No mouse devices found")
        return

    print("Initializing handlers")
    handlers = [LinuxMouseHandler_wayland(device) for device in mouse_devices]

    print(f"type of handlers: {type(handlers)}")
    print(f"handlers: {handlers}")

    for handler in handlers:
        print(f"Type of handler.mouse: {type(handler.mouse)}")
        print(f"handler.mouse: {handler.mouse}")
        asyncio.create_task(consume_move_events(handler))

    stop_event = asyncio.Event()
    
    sentinel = asyncio.create_task(stop_event.wait())
    
    await sentinel

if __name__ == "__main__":
    asyncio.run(main())
