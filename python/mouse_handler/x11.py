# mouse_handler/x11.py

from .base import BaseMouseHandler

class LinuxMouseHandler_X11(BaseMouseHandler):
    def move(self, x, y):
        print(f'Linux-X11: mouse moved to ({x}, {y})')

    def click(self, x, y, button):
        print(f'Linux-X11: mouse clicked at ({x}, {y}) with button {button}')

    def scroll(self, dx, dy):
        print(f'Linux-X11: mouse scrolled with delta({dx}, {dy})')
