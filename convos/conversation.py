from convos.message import Message
from observer.observer import Publisher
import threading

class Conversation(Publisher):

    def __init__(self):
        super().__init__()
        self.messages = []
        self.lock = threading.Lock()

    def add_message(self, message: Message):
        with self.lock:
            self.messages.append(message)
            self.notify(message)

    def __str__(self):
        return f"{self.messages}"