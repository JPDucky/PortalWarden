from evdev import UInput, ecodes as e
import asyncio

class MouseOutput:
    def __init__(self):
        cap = {
            e.EV_REL: [e.REL_X, e.REL_Y],
            e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT]
        }
        self.ui = UInput(cap, name='virtual-mouse', version=0x3)

    async def moveOut(self, events):
        for event in events:
            self.ui.write(e.EV_REL, e.REL_X, event['x'])
            self.ui.write(e.EV_REL, e.REL_Y, event['y'])
            self.ui.syn()
            await asyncio.sleep(0.01)  # Optional delay between movements

async def main():
    linux_mouse_handler = LinuxMouseHandler_wayland()
    recorded_events = []
    
    print("Recording mouse movements. Move your mouse.")
    async for event in linux_mouse_handler.move():
        recorded_events.append(event)
        if len(recorded_events) > 100:  # Stop after recording 100 events
            break
    
    print("Stopped recording. Replaying in 2 seconds.")
    await asyncio.sleep(2)  # 2-second delay
    
    mouse_output = MouseOutput()
    await mouse_output.moveOut(recorded_events)

if __name__ == "__main__":
    asyncio.run(main())

