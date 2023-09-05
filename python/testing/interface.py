import platform
import sys
from compositor_detector import detect_compositor


# base class to define mouse event interface 
class BaseMouseHandler: 
    def move(self, x, y):
        raise NotImplementedError("This method should be over-written by subclass")

    def click(self, x, y, button):
        raise NotImplementedError("This method should be over-written by subclass")

    def scroll(self, dx, dy):
        raise NotImplementedError("This method should be over-written by subclass")

class LinuxMouseHandler_wayland(BaseMouseHandler):
    def move(self, x, y):
        print(f'Linux-wayland: mouse moved to ({x}, {y})')

    def click(self, x, y, button):
        print(f'Linux-wayland: mouse clicked at ({x}, {y}) with button {button}')

    def scroll(self, dx, dy):
        print(f'Linux-wayland: mouse scrolled with delta({dx}, {dy})')


class LinuxMouseHandler_X11(BaseMouseHandler):
    def move(self, x, y):
        print(f'Linux-X11: mouse moved to ({x}, {y})')

    def click(self, x, y, button):
        print(f'Linux-X11: mouse clicked at ({x}, {y}) with button {button}')

    def scroll(self, dx, dy):
        print(f'Linux-X11: mouse scrolled with delta({dx}, {dy})')

class WindowsMouseHandler(BaseMouseHandler):
    def move(self, x, y):
        print(f'Windows: mouse moved to ({x}, {y})')

    def click(self, x, y, button):
        print(f'Windows: mouse clicked at ({x}, {y}) with button {button}')

    def scroll(self, dx, dy):
        print(f'Windows: mouse scrolled with delta({dx}, {dy})')
    
# factory function to return correct mouse handler
def get_mouse_handler():
    if platform.system() == 'Linux':
        if detect_compositor() == 'Wayland':
            return LinuxMouseHandler_wayland()
        else:
            return LinuxMouseHandler_X11
    elif platform.system() == 'Windows':
        return WindowsMouseHandler()
    else:
        print("platform not detected, please edit the config file and try again")
        sys.exit(1)


# Example potential usage
# if __name__ == "__main__":
#     mouse_handler = get_mouse_handler()
#     mouse_handler.move(10, 20)
#     mouse_handler.click(30, 40, "left")
#     mouse_handler.scroll(1, -1)
#
