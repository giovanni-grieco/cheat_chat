from message_parser.message_parser import MessageParser
from protocol import MessageType


class CryptoMessageParserProxy(MessageParser):

    message_parser: MessageParser

    def __init__(self, message_parser: MessageParser):
        self.message_parser = message_parser

    def parse_message(self, data: bytes) -> (MessageType, str, str):
        #DO SOMETHING ADDITIONAL
        return self.message_parser.parse_message(data)
