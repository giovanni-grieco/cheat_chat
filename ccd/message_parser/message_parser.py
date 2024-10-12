from ccd import protocol
from ccd.protocol import MessageType


class MessageParser:

    def parse_message(self, data: bytes) -> (MessageType, str, str):
        return protocol.parse_packet(data)