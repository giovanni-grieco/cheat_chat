from enum import Enum

class MessageType(Enum):
    HELLO = "Hello"
    BYE = "Bye"
    POKE = "Poke"
    MESSAGE = "Message"