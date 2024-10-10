class Peer:

    username : str
    ip : str
    lastSeen : str

    def __init__ (self, username:str, ip:str, lastSeen:str):
        self.username = username
        self.ip = ip
        self.lastSeen = lastSeen
    
    def to_string(self) -> str:
        return self.username + " " + self.ip + " " + str(self.lastSeen)

    def equals(self, peer) -> bool:
        return self.username == peer.username and self.ip == peer.ip

