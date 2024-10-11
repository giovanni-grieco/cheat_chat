from peer import Peer
import threading

class AddressBook:

    def __init__ (self):
        self.peers = []

    def add_peer (self, peer: Peer):
        if peer not in self.peers:
            self.peers.append(peer)
        else:
            self.peers[self.peers.index(peer)].last_seen = peer.last_seen
    
    def remove_peer (self, peer: Peer):
        self.peers.remove(peer)
    
    def get_peers (self):
        return self.peers
    
    def find_peer (self, username: str):
        for peer in self.peers:
            if peer.username == username:
                return peer
        return None
    
    def to_string (self):
        string : str = "Address Book\n"
        linecount = 1
        for peer in self.peers:
            string += str(linecount)+") "+ peer.to_string() + "\n"
            linecount += 1
        return string

class ConcurrentAddressBookProxy(AddressBook):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def add_peer(self, peer: Peer):
        with self.lock:
            super().add_peer(peer)

    def remove_peer(self, peer: Peer):
        with self.lock:
            super().remove_peer(peer)

    def get_peers(self):
        with self.lock:
            return super().peers

    def find_peer(self, username: str):
        with self.lock:
            return super().find_peer(username)