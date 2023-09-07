import asyncio

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


async def main(loop):
    transport, protocol = await loop.create_datagram_endpoint(
        UDPClientProtocol,
        remote_addr=({RHOST}, {RPORT})
    )
    try:
        await asyncio.sleep(60)
    finally:
        transport.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.run_forever()
