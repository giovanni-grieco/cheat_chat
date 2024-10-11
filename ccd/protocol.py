from enum import Enum

class MessageType(Enum):
    HELLO = "Hello"
    BYE = "Bye"
    POKE = "Poke"
    MESSAGE = "Message"

def make_hello_packet(username: str) -> str:
    return f"CCProto|{MessageType.HELLO.value}|{username}"

def make_bye_packet(username: str) -> str:
    return f"CCProto|{MessageType.BYE.value}|{username}"

def make_poke_packet(username: str) -> str:
    return f"CCProto|{MessageType.POKE.value}|{username}"

