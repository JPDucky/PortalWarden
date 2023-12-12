from pynput.mouse import Controller
import time

mouse = Controller()

# Move pointer relative to current position
mouse.move(5, -5)

time.sleep(5)

# Move pointer relative to current position
mouse.move(-5, 5)

