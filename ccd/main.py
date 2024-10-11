import time
import network_utils as nu
import socket
import threading
import random
import system_utils as su
from address_book import ConcurrentAddressBookProxy
from peer import Peer
from protocol import MessageType

settings = {}

def load_settings():
    global settings
    try:
        with open("settings.conf") as f:
            for line in f:
                key, value = line.strip().split("=")
                settings[key] = value
    except FileNotFoundError:
        print("Settings file not found")

def load_default_fallback_settings():
    global settings
    if "port" not in settings:
        settings["port"] = "10011"
        print("Falling back on default port 10011")
    if "username" not in settings:
        settings["username"] = su.get_system_username()
        print("Falling back on system username: "+ su.get_system_username())#system user name
    if "netinterface" not in settings:
        default_interface = nu.get_default_interface()
        settings["netinterface"] = default_interface
        print("Falling back on default network interface:", default_interface)

class CheatChatDaemon:
    def __init__(self):
        self.send_sock = None
        load_settings()
        load_default_fallback_settings()
        local_ip = nu.get_local_ip(settings["netinterface"])
        subnet_mask = nu.get_subnet_mask(settings["netinterface"])
        broadcast_address = nu.calculate_broadcast_address(local_ip, subnet_mask)
        print("Local IP address:", local_ip)
        print("Subnet mask:", subnet_mask)
        print("Broadcast address:", broadcast_address)
        settings["broadcast_address"] = broadcast_address #"desktop-fedora"
        settings["local_ip"] = local_ip
        settings["subnet_mask"] = subnet_mask
        self.address_book = ConcurrentAddressBookProxy()
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.network_setup()
        self.stop_event = threading.Event()

    def network_setup(self):
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen_sock.bind(("0.0.0.0", int(settings["port"])))
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.send_sock.bind((settings["local_ip"],47853))
        self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def listen_for_message(self):
        data, addr = self.listen_sock.recvfrom(1024)
        address_string = addr[0]
        # print(f"Received message: {data} from {addr}")
        if address_string != settings["local_ip"]:
            print(f"Received message: {data} from {addr}")
            event = data.split(b"|")[1].decode()
            username = data.split(b"|")[2].decode()
            sender: Peer = Peer(username, address_string, time.time())
            if event == MessageType.HELLO.value:
                self.address_book.add_peer(sender)  # Forse non funziona lui?
            elif event == MessageType.BYE.value:
                self.address_book.remove_peer(sender)
            elif event == MessageType.POKE.value:
                self.address_book.add_peer(sender)
                su.send_notification(f"{username} poked you")
        else:
            print("Received message from self")

    def listen_udp(self):
        print(f"Listening on {settings["local_ip"]}:{int(settings["port"])}")
        self.listen_sock.settimeout(1)
        while not self.stop_event.is_set():
            try:
                self.listen_for_message()
                #print(self.address_book.to_string())
            except socket.timeout:
                continue
        print("Stopping listener")

    def advertise(self):
        while not self.stop_event.is_set():
            nu.send_udp_packet(f"CCProto|Hello|{settings["username"]}", settings["broadcast_address"], int(settings["port"]), self.send_sock)
            time.sleep(10+random.randint(-5, 5))
        print("Stopping advertiser")
        nu.send_udp_packet(f"CCProto|Bye|{settings["username"]}", settings["broadcast_address"], int(settings["port"]), self.send_sock)


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

def test():
    peer = Peer("Henderson", "1.2.3.4", time.time())
    print(peer.to_string())
    address_book = ConcurrentAddressBookProxy()
    address_book.add_peer(peer)
    print(address_book.to_string())

def run_daemon():
    daemon = CheatChatDaemon()
    daemon.run()

if __name__ == "__main__":
    #test()
    run_daemon()

