from conversation.conversation import Conversation
from observer.observer import Subscriber


class ConversationView(Subscriber):

    conversation: Conversation

    def __init__(self, conversation: Conversation, name):
        super().__init__(name)
        self.conversation = conversation
        self.conversation.register(self)

    def load_chat(self):
        messages = self.conversation.get_messages()
        for message in messages:
            self.write_on_output(message)

    def write_on_output(self, message):
        pass

    def notify(self, message):
        self.write_on_output(message)


