# async-server.py
import asyncio
from os import wait
from main import get_events, process_events, event_queue
import signal

# This is the server's file, set your sink PC's address below, or leave it alone
HOST = '127.0.0.1'
PORT = 20001

stop_event = asyncio.Event()


async def handle_exit(sig):
    print(f"Received exit signal {sig.name}...\nExiting...")
    stop_event.set()


class UDPServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue):
        self.queue = queue
        self.client_addr = None
        super().__init__()

    async def start_sending(self):
        print("Entered start_sending method.")
        while True:
            print(f"Waiting to get event from queue")
            event = await self.queue.get()
            msg = f"Processed: {event}"

            print(f"Attempting to send: {msg}")
            print(f"message length: {len(msg.encode())}")

            if len(msg.encode()) > 1400: # set max MTU size
                print("Message too large to send")
                continue

            if self.client_addr:
                print(f"Sending to {self.client_addr}")
                self.transport.sendto(msg.encode(), self.client_addr)


    def connection_made(self, transport):
        self.transport = transport
        self.sending_task = asyncio.create_task(self.start_sending())
        print("Connection made.")

    def datagram_received(self, data, addr):
        print(f"Received {data.decode()} from {addr}")
        self.client_addr = addr

    def connection_lost(self, exc):
        self.sending_task.cancel()
        print("Socket closed, stop the event loop")


async def main():
    loop = asyncio.get_running_loop()

    loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(handle_exit(signal.SIGTERM)))
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(handle_exit(signal.SIGINT)))
    
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(event_queue),
        local_addr=(HOST, PORT)
    )
    asyncio.create_task(get_events(event_queue))
    asyncio.create_task(process_events(event_queue))

    sentinel = asyncio.create_task(stop_event.wait())

    await sentinel


if __name__ == "__main__":
    asyncio.run(main())
