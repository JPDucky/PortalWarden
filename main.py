# main.py
import asyncio
from mouse_handler.factory import get_mouse_handler

mouse = get_mouse_handler() #LinuxMouseHandler_wayland()

event_queue = asyncio.Queue()

async def get_events(event_queue):
    print("Entered get_events")
    async for move_value in mouse.move():
        await event_queue.put(move_value)
        # print(f"Put {move_value} into queue")
        # print(move_value)


async def process_events(event_queue):
    print("Entered process_events")
    while True:
        event = await event_queue.get()
        # print(f"Processed1: {event}")
        # do a thing w/ event
        # print(f"Processed: {event}")

# if __name__ == "__main__":
#     asyncio.ensure_future(get_events(event_queue))
#     asyncio.ensure_future(process_events(event_queue))
#     loop = asyncio.get_event_loop()
#     loop.run_forever()
