import socket
import threading
import time
import system_utils as su
import protocol
from address_book.address_book import AddressBook
from convos.peer import Peer
import network.network_utils as nu
import random
from message_parser.message_parser import MessageParser

class DaemonController:

    listen_sock: socket.socket
    send_sock: socket.socket
    address_book: AddressBook
    stop_event: threading.Event
    settings = {}
    listener_thread: threading.Thread
    advertiser_thread: threading.Thread
    message_parser: MessageParser

    def __init__(self, settings, address_book):
        self.settings=settings
        self.network_setup()
        self.stop_event = threading.Event()
        self.network_setup()
        self.address_book = address_book
        self.message_parser = MessageParser()

    def network_setup(self):
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen_sock.bind(("0.0.0.0", int(self.settings["dport"])))
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.send_sock.bind((self.settings["local_ip"], 47853))
        self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def listen_udp(self):
        print(f"Listening on {self.settings["local_ip"]}:{int(self.settings["dport"])}")
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
            nu.send_udp_packet(protocol.make_hello_packet(self.settings["username"]), self.settings["broadcast_address"], int(self.settings["dport"]), self.send_sock)
            time.sleep(10+random.randint(-5, 5))
        print("Stopping advertiser")
        nu.send_udp_packet(protocol.make_bye_packet(self.settings["username"]), self.settings["broadcast_address"], int(self.settings["dport"]), self.send_sock)

    def start(self):
        self.listener_thread = threading.Thread(target=self.listen_udp)
        self.advertiser_thread = threading.Thread(target=self.advertise)
        self.listener_thread.start()
        self.advertiser_thread.start()

    def wait(self):
        self.listener_thread.join()
        self.advertiser_thread.join()

    def stop(self):
        self.stop_event.set()
        self.listener_thread.join()
        self.advertiser_thread.join()