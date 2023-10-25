# mouse_handler/factory.py

import platform
import sys
from .multi_device import LinuxMouseHandler_wayland, device_discovery
from .x11 import LinuxMouseHandler_X11
from .windows import WindowsMouseHandler
from .compositor_detector import detect_compositor


# factory function to return correct mouse handler
def get_mouse_handler():
    mouse_device = device_discovery().discover_mouse_device()
    if platform.system() == 'Linux':
        if detect_compositor() == 'Wayland':
            print("wayland found")
            return LinuxMouseHandler_wayland(mouse_device)
        else:
            print("x11 found")
            return LinuxMouseHandler_X11
    elif platform.system() == 'Windows':
        print("windows found")
        return WindowsMouseHandler()
    else:
        print("platform not detected, please edit the config file and try again")
        sys.exit(1)

print("factory completed")
