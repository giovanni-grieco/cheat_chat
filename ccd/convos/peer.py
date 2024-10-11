from ccd.convos.conversation import Conversation


class Peer:

    username : str
    ip : str
    last_seen : float
    conversation: Conversation

    def __init__ (self, username:str, ip:str, last_seen:float):
        self.username = username
        self.ip = ip
        self.last_seen = last_seen
        self.conversations = Conversation()

    def add_message(self, message):
        self.conversations.add_message(message)

    def flush_conversation(self):
        self.conversations = Conversation()

    def __str__(self) -> str:
        return self.username + " " + self.ip + " " + str(self.last_seen)

    def __eq__(self, peer):
        return self.username == peer.username and self.ip == peer.ip

    def __hash__(self):
        return hash(self.username + self.ip)
