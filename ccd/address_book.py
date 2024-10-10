from peer import Peer
import threading

class AddressBook:

    def __init__ (self):
        self.peers = []

    def addPeer (self, peer: Peer):
        self.peers.append(peer)
    
    def removePeer (self, peer: Peer):
        self.peers.remove(peer)
    
    def getPeers (self):
        return self.peers
    
    def findPeer (self, username: str):
        for peer in self.peers:
            if peer.username == username:
                return peer
        return None
    
    def to_string (self):
        string : str = ""
        for peer in self.peers:
            string += peer.to_string() + "\n"
        return string

class ConcurrentAddressBookProxy(AddressBook):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def addPeer(self, peer: Peer):
        with self.lock:
            if(peer not in self.peers):
                self.peers.append(peer)
            else:
                for p in self.peers:
                    if p.equals(peer):
                        p.last_seen = peer.last_seen

    def removePeer(self, peer: Peer):
        with self.lock:
            self.peers.remove(peer)

    def getPeers(self):
        with self.lock:
            return self.peers

    def findPeer(self, username: str):
        with self.lock:
            for peer in self.peers:
                if peer.username == username:
                    return peer
        return None