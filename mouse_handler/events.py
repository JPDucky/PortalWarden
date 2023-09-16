import evdev
import evdev.ecodes as ev

def print_mouse_events(mouse_device):
    for event in mouse_device.read_loop():
        if event.type == ev.EV_KEY:
            print(f"Found event: {event}")


mouse = evdev.InputDevice('/dev/input/event2')
print_mouse_events(mouse)
