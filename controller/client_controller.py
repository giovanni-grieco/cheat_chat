import asyncio
import threading
from typing import Awaitable

import websockets
import protocol
from address_book.address_book import AddressBook
from conversation.message import Message
from address_book.peer import Peer
import network.network_utils as nu

class ClientController:

    address_book: AddressBook
    settings: {}
    stop_event: asyncio.Event
    loop: asyncio.AbstractEventLoop
    thread: threading.Thread

    def __init__(self, settings, address_book):
        self.address_book = address_book
        self.settings = settings
        self.stop_event = asyncio.Event()
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.run)

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.start())

    async def listen_client(self):
        async with websockets.serve(self.handle_client, "127.0.0.1", int(self.settings["cport"])):
            await self.stop_event.wait()  # Wait until the stop event is set

    async def handle_client(self, websocket):
        async for message in websocket:
            print(f"Received message: {message}")
            await self.handle_message(message)

    async def handle_message(self, message):
        print(message)

    async def send_message(self, dest_username, content):
        dest_peer: Peer = self.address_book.find_peer(dest_username)
        message: Message = Message(self.settings["username"], content)
        dest_peer.add_message(message)
        if dest_peer is not None:
            await nu.send_udp_packet(protocol.make_message_packet(self.settings["username"], content), dest_peer.ip, int(self.settings["dport"]), self.send_sock)
        else:
            print("Destination not found")

    async def start(self):
        await self.listen_client()

    def stop(self):
        self.stop_event.set()
        self.loop.stop()
        self.thread.join()