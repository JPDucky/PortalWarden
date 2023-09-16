# mouse_handler/factory.py

import platform
import sys
from .multi_device import LinuxMouseHandler_wayland
from .x11 import LinuxMouseHandler_X11
from .windows import WindowsMouseHandler
from .compositor_detector import detect_compositor


# factory function to return correct mouse handler
def get_mouse_handler():
    if platform.system() == 'Linux':
        if detect_compositor() == 'Wayland':
            print("wayland found")
            return LinuxMouseHandler_wayland()
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
