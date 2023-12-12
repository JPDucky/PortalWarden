from base import BaseMouseHandler
from evdev import InputDevice
from pynput.mouse import Controller
import evdev
import asyncio
from evdev import UInput, ecodes as e

mouse = InputDevice('/dev/input/event4')
mouse_out = Controller()


class LinuxMouseHandler_wayland(BaseMouseHandler):
    def __init__(self):
        self.mouse = mouse
        self.x = 0
        self.y = 0

    async def move(self):
        async for event in self.mouse.async_read_loop():
            # if event.code in [evdev.ecodes.REL_X, evdev.ecodes.REL_Y]:
            if event.code == evdev.ecodes.REL_X:
                self.x = event.value
            if event.code == evdev.ecodes.REL_Y:
                self.y = event.value
            if self.x !=0:
                yield {'x': self.x, 'y': self.y}


class MouseOutput:
    def __init__(self):
        cap = {
            e.EV_REL: [e.REL_X, e.REL_Y],
            e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT]
        }
        self.ui = UInput(cap, name='virtual-mouse', version=0x3)

    async def moveOut(self, events):
        for event in events:
            self.ui.write(e.EV_REL, e.REL_X, event['x'])
            self.ui.write(e.EV_REL, e.REL_Y, event['y'])
            self.ui.syn()
            await asyncio.sleep(0.01)  # Optional delay between movements




# async def main():
#     linux_mouse_handler = LinuxMouseHandler_wayland()
#     recorded_events = []
#
#     print("Recording moue movements. Move mouse.")
#     async for event in linux_mouse_handler.move():
#         recorded_events.append(event)
#         if len(recorded_events) > 100:
#             break
#         
#     print("Stopped recording. Replaying in 2 seconds")
#     await asyncio.sleep(2)
#
#     mouse_output = MouseOutput()
#     await mouse_output.moveOut(recorded_events)


# if __name__ == "__main__":
#     asyncio.run(main())
async def main():
    linux_mouse_handler = LinuxMouseHandler_wayland()
    recorded_events = []
    
    print("Recording mouse movements. Move your mouse.")
    async for event in linux_mouse_handler.move():
        recorded_events.append(event)
        if len(recorded_events) > 100:  # Stop after recording 100 events
            break
    
    print("Stopped recording. Replaying in 2 seconds.")
    await asyncio.sleep(2)  # 2-second delay
    
    mouse_output = MouseOutput()
    await mouse_output.moveOut(recorded_events)

if __name__ == "__main__":
    asyncio.run(main())

