import evdev

# devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
# for device in devices:
#    print(device.path, device.name, device._rawcapabilities, device.phys)

# touchpad touch/click events:
# device = evdev.InputDevice('/dev/input/event5')
# print(device)
#
# for event in device.read_loop():
#     if event.type == evdev.ecodes.EV_KEY:
#         print(evdev.categorize(event))


# keyboard events:
# device = evdev.InputDevice('/dev/input/event2')
# print(device)
#
# for event in device.read_loop():
#     if event.type == evdev.ecodes.EV_KEY:
#         print(evdev.categorize(event))

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
# for device in devices:
#     print(device)

device = evdev.InputDevice('/dev/input/event5')
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        print(evdev.categorize(event))
