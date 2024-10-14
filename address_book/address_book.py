from convos.peer import Peer

class AddressBook:

    peers = []

    def add_peer (self, peer: Peer):
        if peer not in self.peers:
            print(peer)
            self.peers.append(peer)
        else:
            self.peers[self.peers.index(peer)].last_seen = peer.last_seen
    
    def remove_peer (self, peer: Peer):
        if peer in self.peers:
            self.peers.remove(peer)
    
    def get_peers (self):
        return self.peers
    
    def find_peer (self, username: str):
        for peer in self.peers:
            if peer.username == username:
                return peer
        return None
    
    def __str__ (self) -> str:
        string : str = "Address Book\n"
        linecount = 1
        for peer in self.peers:
            string += str(peer) + "\n"
            linecount += 1
        return string