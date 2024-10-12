import protocol
from protocol import MessageType


class MessageParser:

    def parse_message(self, data: bytes) -> (MessageType, str, str):
        return protocol.parse_packet(data)