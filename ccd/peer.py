class Peer:

    username : str
    ip : str
    last_seen : str

    def __init__ (self, username:str, ip:str, last_seen:str):
        self.username = username
        self.ip = ip
        self.last_seen = last_seen
    
    def to_string(self) -> str:
        return self.username + " " + self.ip + " " + str(self.last_seen)

    def equals(self, peer) -> bool:
        return self.username == peer.username and self.ip == peer.ip

