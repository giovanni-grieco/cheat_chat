from ccd.convos.message import Message
from ccd.observer.observer import Publisher


class Conversation(Publisher):
    def __init__(self):
        super().__init__()
        self.messages = []

    def add_message(self, message: Message):
        self.messages.append(message)
        self.notify(message)

    def __str__(self):
        return f"{self.messages}"