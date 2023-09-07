# async-client.py
import asyncio
import signal

# This is the client's address, input the drain's IP below
RHOST = '127.0.0.1'
RPORT = 20001


stop_event = asyncio.Event()


async def handle_exit(sig):
    print(f"Received exit signal {sig.name}...\nExiting...")
    stop_event.set()


class UDPClientProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport
        print('Sending:')
        self.transport.sendto(b'Hello Server')

    def datagram_received(self, data, addr):
        print(f"Received: {data.decode()} from {addr}")

    def connection_lost(self, exc):
        print("Server closed, stop event loop")
        loop = asyncio.get_event_loop()
        loop.stop()


async def main():
    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(handle_exit(signal.SIGTERM)))
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(handle_exit(signal.SIGINT)))
    
    transport, protocol = await loop.create_datagram_endpoint(
        UDPClientProtocol,
        remote_addr=(RHOST, RPORT)
    )

    sentinel = asyncio.create_task(stop_event.wait())

    await sentinel



if __name__ == "__main__":
    asyncio.run(main())
