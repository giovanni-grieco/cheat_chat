from enum import Enum

class MessageType(Enum):
    HELLO = "Hello"
    BYE = "Bye"
    POKE = "Poke"
    MESSAGE = "Message"

def make_hello_packet(sender_username: str) -> str:
    return f"CCProto|{MessageType.HELLO.value}|{sender_username}|"

def make_bye_packet(sender_username: str) -> str:
    return f"CCProto|{MessageType.BYE.value}|{sender_username}|"

def make_poke_packet(sender_username: str) -> str:
    return f"CCProto|{MessageType.POKE.value}|{sender_username}|"

def make_message_packet(sender_username: str, content: str) -> str:
    return f"CCProto|{MessageType.MESSAGE.value}|{sender_username}|{content}"

def parse_packet(data: bytes) -> (MessageType, str, str):
    data = data.split(b"|")
    return MessageType(data[1].decode()), data[2].decode(), data[3].decode() if len(data) > 3 else None


