# async-server.py
import asyncio
from main import get_events, process_events, event_queue
import signal
import socket

stop_event = asyncio.Event()

PORT = 20001


class ErrorHandling():
    def __init__(self, err, signal):
        self.err = err
        self.signal = signal

    async def handle_exit(sig):
        print(f"Received exit signal {sig.name}...\nExiting...")
        stop_event.set()


class PortHandler():
    @classmethod
    def port_check(cls, port, host='0.0.0.0'):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind((host, port))
            sock.close()
            print(f"Port {port} is available")
            return True
        except OSError:
            print(f"Port {port} is not available")
            return False

    @classmethod
    async def select_port(cls):
        port = 20001
        while not cls.port_check(port):
            port += 1
        return port


class DiscoveryHandler():
    def __init__(self, transport, IPaddr, port=PORT):
        self.transport = transport
        self._IPAddr = IPaddr
        self.port = port

    async def broadcast(self):
        if self._IPAddr is None:
            print("IP address not set, cannot broadcast")
            return
        
        broadcast_address = (self._IPAddr, self.port)
        while True:
            self.transport.sendto(b"discovery", broadcast_address)
            await asyncio.sleep(15)


class UDPServerProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue, port, on_connection_made=None):
        self.queue = queue
        self.client_addr = None
        self.port = port
        self._IPaddr = None
        self.get_hostname()
        self.on_connection_made = on_connection_made
        super().__init__()

    async def start_sending(self):
        print("Entered start_sending method.")
        while True:
            print(f"Waiting to get event from queue")
            event = await self.queue.get()
            msg = f"Processed: {event}"

            print(f"Attempting to send: {msg}")
            print(f"message length: {len(msg.encode())}")

            if len(msg.encode()) > 1400:  # set max MTU size
                print("Message too large to send")
                continue

            if self.client_addr:
                print(f"Sending to {self.client_addr}")
                self.transport.sendto(msg.encode(), self.client_addr)

    def connection_made(self, transport):
        self.transport = transport
        self.discovery_handler = DiscoveryHandler(self.transport, self._IPaddr, port=self.port)
        self.sending_task = asyncio.create_task(self.start_sending())
        sock = transport.get_extra_info("socket")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print("Connection made.")

        if self.on_connection_made:
            self.on_connection_made(self)

    def datagram_received(self, data, addr):
        print(f"Received {data.decode()} from {addr}")
        self.client_addr = addr

    def connection_lost(self, exc):
        self.sending_task.cancel()
        print("Socket closed, stop the event loop")

    # async def broadcast(self):
    #     if self._IPaddr is None:
    #         print("IP address not set, cannot broadcast address")
    #         return
    #
    #     broadcast_address = (self._IPaddr, PORT)
    #     while True:
    #         self.transport.sendto(b"discovery", broadcast_address)
    #         await asyncio.sleep(5)

    def get_hostname(self):
        self._hostname = socket.gethostname()
        self._IPaddr = socket.gethostbyname(self._hostname)
        print("hostname: " + self._hostname, "IP: " + self._IPaddr)


def on_connection_made(protocol):
    asyncio.create_task(protocol.discovery_handler.broadcast())


async def main():
    port = await PortHandler.select_port()
    loop = asyncio.get_running_loop()

    loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(ErrorHandling.handle_exit(signal.SIGTERM)))
    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(ErrorHandling.handle_exit(signal.SIGINT)))

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UDPServerProtocol(event_queue, port, on_connection_made),
        local_addr=("0.0.0.0", port)
    )
    asyncio.create_task(get_events(event_queue))
    asyncio.create_task(process_events(event_queue))

    sentinel = asyncio.create_task(stop_event.wait())

    await sentinel


if __name__ == "__main__":
    asyncio.run(main())
