import protocol
from address_book.address_book import AddressBook
from conversation.message import Message
from address_book.peer import Peer
import network.network_utils as nu


class ClientController:

    address_book: AddressBook
    settings: {}

    def __init__(self, settings ,address_book):
        self.address_book = address_book
        self.settings = settings
        self.network_setup()

    def network_setup(self):
        pass


    def listen_client(self):
        pass


    def send_message(self, dest_username, content):
        dest_peer: Peer = self.address_book.find_peer(dest_username)
        message: Message = Message(self.settings["username"], content)
        dest_peer.add_message(message)
        if dest_peer is not None:
            nu.send_udp_packet(protocol.make_message_packet(self.settings["username"], content), dest_peer.ip, int(self.settings["dport"]), self.send_sock)
        else:
            print("Destination not found")

    def start(self):
        pass

    def wait(self):
        pass

    def stop(self):
        pass
