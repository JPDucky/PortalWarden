# mouse_handler/windows.py

from .base import BaseMouseHandler

class WindowsMouseHandler(BaseMouseHandler):
    def move(self, x, y):
        print(f'Windows: mouse moved to ({x}, {y})')

    def click(self, x, y, button):
        print(f'Windows: mouse clicked at ({x}, {y}) with button {button}')

    def scroll(self, dx, dy):
        print(f'Windows: mouse scrolled with delta({dx}, {dy})')
