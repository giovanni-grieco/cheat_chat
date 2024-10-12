import random
import socket
import threading
import time

import network_utils as nu
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
    stop_event : threading.Event


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
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.network_setup()
        self.stop_event = threading.Event()

        #Address book e message parsers dovrebbero essere gestiti da un context e delle factory
        self.address_book = ConcurrentAddressBookProxy(AddressBook())
        self.message_parser = CryptoMessageParserProxy(MessageParser())

    def network_setup(self):
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen_sock.bind(("0.0.0.0", int(self.settings["port"])))
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.send_sock.bind((self.settings["local_ip"],47853))
        self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def listen_udp(self):
        print(f"Listening on {self.settings["local_ip"]}:{int(self.settings["port"])}")
        self.listen_sock.settimeout(1)
        while not self.stop_event.is_set():
            try:
                self.listen_for_message()
                #print(self.address_book.to_string())
            except socket.timeout:
                continue
        print("Stopping listener")

    def listen_for_message(self):
        data, addr = self.listen_sock.recvfrom(1024)
        address_string = addr[0]
        # print(f"Received message: {data} from {addr}")
        if address_string != self.settings["local_ip"]:
            print(f"Received message: {data} from {addr}")
            self.parse_message(data, address_string)
        else:
            print("Received message from self")

    def parse_message(self, data, address_string):
        event, sender_username, content = self.message_parser.parse_message(data)
        sender: Peer = Peer(sender_username, address_string, time.time())
        if event == protocol.MessageType.HELLO.value:
            self.address_book.add_peer(sender)  # Forse non funziona lui?
        elif event == protocol.MessageType.BYE.value:
            self.address_book.remove_peer(sender)
        elif event == protocol.MessageType.POKE.value:
            self.address_book.add_peer(sender)
            su.send_notification(f"{sender_username} poked you")
        elif event == protocol.MessageType.MESSAGE.value:
            print(f"Message from {sender_username}: {content}")
            #Capire se il messaggio è per l'utente corrente. In cosa non lo fosse, lo si ignora.
            #Accedere all'address-book, vedere se già esiste il contatto.
            #Se non esiste crearlo, e poi aggiungere il messaggio alla chat.

    def advertise(self):
        while not self.stop_event.is_set():
            nu.send_udp_packet(protocol.make_hello_packet(self.settings["username"]), self.settings["broadcast_address"], int(self.settings["port"]), self.send_sock)
            time.sleep(10+random.randint(-5, 5))
        print("Stopping advertiser")
        nu.send_udp_packet(protocol.make_bye_packet(self.settings["username"]), self.settings["broadcast_address"], int(self.settings["port"]), self.send_sock)

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
            listener_thread = threading.Thread(target=self.listen_udp)
            advertiser_thread = threading.Thread(target=self.advertise)
            listener_thread.start()
            advertiser_thread.start()
            listener_thread.join()
            advertiser_thread.join()
        except KeyboardInterrupt:
            self.stop_event.set()
            listener_thread.join()
            advertiser_thread.join()
            self.listen_sock.close()
            self.send_sock.close()
            print("Exiting...")