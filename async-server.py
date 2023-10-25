# async-server.py
import asyncio
import logging
import signal
import socket
import argparse

from main import event_queue, get_events, process_events

logging.basicConfig(level=logging.DEBUG)
MTU_SIZE = 1400
PORT = 20001
stop_event = asyncio.Event()

parser = argparse.ArgumentParser(description="Async Server")
parser.add_argument("--log-msg", action="store_true", help="Log each message received")
args = parser.parse_args()

def log_message(self, msg):
    if args.log_msg:
        logging.debug(f"Message: {msg}")


class ErrorHandling():
    @staticmethod
    async def handle_exit(sig: signal.Signals):
        logging.info(f"Received exit signal {sig.name}... Exiting...")
        stop_event.set()


class PortHandler():
    @classmethod
    def port_check(cls, port: int, host: str = '0.0.0.0') -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                sock.bind((host, port))
                logging.info(f"Port {port} is available")
                return True
            except OSError:
                logging.info(f"Port {port} is not available")
                return False

    @classmethod
    async def select_port(cls) -> int:
        port = PORT
        while not cls.port_check(port):
            port += 1
        return port


class DiscoveryHandler():
    def __init__(self, transport, IPaddr, port=PORT):
        self.transport = transport
        self._IPAddr = IPaddr
        self.port = port
        self.should_broadcast = True

    async def broadcast(self):
        if self._IPAddr is None:
            print("IP address not set, cannot broadcast")
            return

        broadcast_address = (self._IPAddr, self.port)
        while self.should_broadcast:
            self.transport.sendto(b"discovery", broadcast_address)
            await asyncio.sleep(5)


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
        logging.info("Entered start_sending method.")
        while True:
            try:
                event = await self.queue.get()
                logging.debug(f"Received event from queue: {event}")

                msg = f"x:{event['x']},y:{event['y']}"
                self.log_message(msg)

                if len(msg.encode()) > MTU_SIZE:  # set max MTU size
                    logging.warning("Message too large to send")
                    continue

                if self.client_addr:
                    logging.info(f"Sending to {self.client_addr}")
                    self.transport.sendto(msg.encode(), self.client_addr)
            except Exception as e:
                logging.error(f"An error occurred while sending: {e}")


    def connection_made(self, transport):
        self.transport = transport
        self.discovery_handler = DiscoveryHandler(
            self.transport, self._IPaddr, port=self.port)
        self.sending_task = asyncio.create_task(self.start_sending())
        sock = transport.get_extra_info("socket")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print("Connection made.")

        if self.on_connection_made:
            self.on_connection_made(self)

    def datagram_received(self, data, addr):
        print(f"Received {data.decode()} from {addr}")
        self.client_addr = addr
        self.discovery_handler.should_broadcast = False

    def connection_lost(self, exc):
        self.sending_task.cancel()
        print("Socket closed, stop the event loop")
        self.discovery_handler.should_broadcast = True

    def get_hostname(self):
        self._hostname = socket.gethostname()
        self._IPaddr = socket.gethostbyname(self._hostname)
        print("hostname: " + self._hostname, "IP: " + self._IPaddr)


def on_connection_made(protocol):
    asyncio.create_task(protocol.discovery_handler.broadcast())


def add_signal_handlers():
    loop = asyncio.get_running_loop()
    for sig in [signal.SIGTERM, signal.SIGINT]:
        loop.add_signal_handler(sig, lambda s=sig: asyncio.create_task(ErrorHandling.handle_exit(s)))


async def main():
    port = await PortHandler.select_port()
    loop = asyncio.get_running_loop()

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
