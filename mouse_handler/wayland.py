# mouse_handler/wayland.py

from .base import BaseMouseHandler
from evdev import InputDevice
from selectors import DefaultSelector, EVENT_READ

selector = DefaultSelector()

mouse = InputDevice('/dev/input/event5')

selector.register(mouse, EVENT_READ)
 
class LinuxMouseHandler_wayland(BaseMouseHandler):
    def __init__(self):
        self.mouse = mouse
        self.x = 0
        self.y = 0

    def move(self):
        while True:
            for key, mask in selector.select():
                device = key.fileobj
                for event in device.read():
                    if event.code == 53:
                        self.x = event.value
                        return {self.x}
                    if event.code == 54:
                        self.y = event.value
                        return {self.y}




print("wayland.py loaded")
#
    # async def move(self):
    #     async for event in self.mouse.async_read_loop():
    #         for key, mask in selector.select():
    #             device = key.fileobj
    #             for event in device.read():
    #                 if event.code == 53: # x axis
    #                     # print(f"x-axis-abs: {event.value}")
    #                     self.x = event.value
    #                 if event.code == 54:
    #                     # print(f"y-axis-abs: {event.value}")
    #                     self.y = event.value
    #                 yield {self.x, self.y}
#
#
#
#
    # async def move(self):
    #     async for event in self.mouse.async_read_loop():
    #         # if event.type == evdev.ecodes.EV_SYN:
    #         #
    #         #     self.sequence_id += 1
    #         #     yield {'events': self.event_batch, 'sequence_id': self.sequence_id}
    #         #     continue
    #         #
    #         #    # TODO: make the sequence_id/timestamp part of verbose output,
    #         #     # dont enable it for normal mode for speed's sake
    #         #
    #
    #         # if event.code in [evdev.ecodes.REL_X, evdev.ecodes.REL_Y]:
    #         #     if event.code == evdev.ecodes.REL_X:
    #         #         self.x = event.value
    #         #     if event.code == evdev.ecodes.REL_Y:
    #         #         self.y = event.value
    #
    #             # yield {
    #             #     'x': self.x,
    #             #     'y': self.y,
    #             #     'timestamp': event.timestamp()
    #             # }
    #         for key, mask in selector.select():
    #             device = key.fileobj
    #             for event in device.read():
    #                 if event.code == 53: # x axis
    #                     # print(f"x-axis-abs: {event.value}")
    #                     yield {self.x == event.value} 
    #                 if event.code == 54:
    #                     # print(f"y-axis-abs: {event.value}")
    #                     yield {self.y == event.value}
    #                 yield {}
    #
    #
    #
