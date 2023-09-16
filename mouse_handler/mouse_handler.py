from evdev import InputDevice, list_devices, ecodes

def discover_mouse_device():
    devices = [InputDevice(path) for path in list_devices()]
    mouse_devices = []

    for device in devices:
        capabilities = device.capabilities(verbose=False)
        
        if ecodes.EV_REL in capabilities:
            rel_codes = capabilities[ecodes.EV_REL]
            
            if ecodes.REL_X in rel_codes and ecodes.REL_Y in rel_codes:
                mouse_devices.append({'path': device.path, 'name': device.name})
                
    return mouse_devices


def main():
    print(discover_mouse_device())


if __name__ == "__main__":
    main()
