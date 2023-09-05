# mouse_handler/wayland.py

from .base import BaseMouseHandler
import evdev

mouse = evdev.InputDevice('/dev/input/event5')
 
class LinuxMouseHandler_wayland(BaseMouseHandler):
    def __init__(self):
        self.mouse = mouse
        self.x = 0
        self.y = 0
        self.sequence_id = 0
        self.event_batch = []

    async def move(self):
        async for event in self.mouse.async_read_loop():
            if event.type == evdev.ecodes.EV_SYN:

                self.sequence_id += 1
                yield {'events': self.event_batch, 'sequence_id': self.sequence_id}
                continue

               # TODO: make the sequence_id/timestamp part of verbose output,
                # dont enable it for normal mode for speed's sake

            if event.code in [evdev.ecodes.REL_X, evdev.ecodes.REL_Y]:
                if event.code == evdev.ecodes.REL_X:
                    self.x = event.value
                if event.code == evdev.ecodes.REL_Y:
                    self.y = event.value

                yield {
                    'x': self.x,
                    'y': self.y,
                    'timestamp': event.timestamp()
                }

print("wayland.py loaded")
