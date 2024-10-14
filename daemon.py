import random
import socket
import threading
import time

from network import network_utils as nu
import system_utils as su
import protocol
from address_book.address_book import AddressBook
from address_book.concurrent_address_book_proxy import ConcurrentAddressBookProxy
from convos.message import Message
from convos.peer import Peer
from message_parser.crypto_message_parser_proxy import CryptoMessageParserProxy
from message_parser.message_parser import MessageParser


class CheatChatDaemon:

    settings = {}
    message_parser : MessageParser
    address_book : AddressBook
    listen_sock : socket.socket
    send_sock : socket.socket
    client_sock : socket.socket


    def __init__(self, settingss):
        self.settings = settingss
        local_ip = nu.get_local_ip(self.settings["netinterface"])
        subnet_mask = nu.get_subnet_mask(self.settings["netinterface"])
        broadcast_address = nu.calculate_broadcast_address(local_ip, subnet_mask)
        print("Local IP address:", local_ip)
        print("Subnet mask:", subnet_mask)
        print("Broadcast address:", broadcast_address)
        self.settings["broadcast_address"] = broadcast_address #"desktop-fedora"
        self.settings["local_ip"] = local_ip
        self.settings["subnet_mask"] = subnet_mask
        self.network_setup()
        self.stop_event = threading.Event()

        #Address book e message parsers dovrebbero essere gestiti da un context e delle factory
        self.address_book = ConcurrentAddressBookProxy(AddressBook())
        self.message_parser = CryptoMessageParserProxy(MessageParser())

    def network_setup(self):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, dest_username, content):
        dest_peer: Peer = self.address_book.find_peer(dest_username)
        message: Message = Message(self.settings["username"], content)
        dest_peer.add_message(message)
        if dest_peer is not None:
            nu.send_udp_packet(protocol.make_message_packet(self.settings["username"], content), dest_peer.ip, int(self.settings["port"]), self.send_sock)
        else:
            print("Destination not found")

    def run(self):
        try:
            listener_thread.join()
            advertiser_thread.join()
        except KeyboardInterrupt:
            self.stop_event.set()
            listener_thread.join()
            advertiser_thread.join()
            self.listen_sock.close()
            self.send_sock.close()
            print("Exiting...")