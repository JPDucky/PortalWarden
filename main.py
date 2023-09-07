# main.py
import asyncio
from mouse_handler.factory import get_mouse_handler

mouse = get_mouse_handler()

async def print_events(event_queue: asyncio.Queue):
    async for move_value in mouse.move(x, y):
        await event_queue.put(move_value)

async def process_events(event_queue: asyncio.Queue):
    while True:
        event = await event_queue.get()
        return event

async def main():
    event_queue = asyncio.Queue()

    producer = asyncio.create_task(print_events(event_queue))
    consumer = asyncio.create_task(process_events(event_queue))
    
    # asyncio.create_task(print_events())
    await asyncio.gather(producer, consumer)



if __name__ == "__main__":
    asyncio.run(main())
