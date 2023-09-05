# mouse_handler/base.py -> class contract

# base class to define mouse event interface 
class BaseMouseHandler: 
    def move(self, x, y):
        raise NotImplementedError("This method should be over-written by subclass")

    def click(self, x, y, button):
        raise NotImplementedError("This method should be over-written by subclass")

    def scroll(self, dx, dy):
        raise NotImplementedError("This method should be over-written by subclass")
