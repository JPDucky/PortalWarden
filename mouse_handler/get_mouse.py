import sys
import evdev
import evdev.ecodes as ev
import time

def get_mice():
    mice = []
    for fn in evdev.list_devices():
        dev = evdev.InputDevice(fn)
        cap = dev.capabilities()
        if ev.EV_KEY in cap:
            if ev.BTN_MOUSE in cap[ev.EV_KEY]:
                print(f"Found mouse device: {dev.name}, {dev.path}")
                mice.append(dev)
    return mice


for mouse in get_mice():
    print(f"Found mouse device: {mouse.name}, {mouse.path}")

    event = next((event for event in mouse.read_loop() if event.type==ev.EV_KEY))
    if event:
        print(f"Found event: {event}")
