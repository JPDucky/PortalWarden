# client.py

from .mouse_handler.factory import get_mouse_handler

mouse = get_mouse_handler()

async def print_events():
    async for move_value in mouse.move():
        print(f"Mouse moved: {move_value}")
