import time
from evdev import UInput, ecodes as e

# Define capabilities of the virtual mouse device
capabilities = {
    e.EV_REL: [e.REL_X, e.REL_Y],  # Relative coordinates
    e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT],  # Buttons
}

# Create the virtual mouse device
with UInput(capabilities, name='virtual-mouse', version=0x3) as ui:
    # Loop to jiggle the mouse
    while True:
        # Move right
        ui.write(e.EV_REL, e.REL_X, 5)
        ui.syn()
        time.sleep(0.2)  # Pause

        # Move down
        ui.write(e.EV_REL, e.REL_Y, 5)
        ui.syn()
        time.sleep(0.2)  # Pause

        # Move left
        ui.write(e.EV_REL, e.REL_X, -5)
        ui.syn()
        time.sleep(0.2)  # Pause

        # Move up
        ui.write(e.EV_REL, e.REL_Y, -5)
        ui.syn()
        time.sleep(0.2)  # Pause

