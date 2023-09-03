from evdev import InputDevice
from selectors import DefaultSelector, EVENT_READ

selector = DefaultSelector()

mouse = InputDevice('/dev/input/event5')
keyboard = InputDevice('/dev/input/event3')

selector.register(mouse, EVENT_READ)
selector.register(keyboard, EVENT_READ)

while True:
    for key, mask in selector.select():
        device = key.fileobj
        for event in device.read():
            print(event)
