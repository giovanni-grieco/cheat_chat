import threading

from address_book.address_book import AddressBook
from address_book.peer import Peer


class ConcurrentAddressBookProxy(AddressBook):

    address_book : AddressBook

    def __init__(self, address_book):
        self.address_book = address_book
        self.lock = threading.Lock()

    def add_peer(self, peer: Peer):
        with self.lock:
            self.address_book.add_peer(peer)

    def remove_peer(self, peer: Peer):
        with self.lock:
            self.address_book.remove_peer(peer)

    def get_peers(self):
        with self.lock:
            return  self.address_book.peers

    def find_peer(self, username: str):
        with self.lock:
            return  self.address_book.find_peer(username)