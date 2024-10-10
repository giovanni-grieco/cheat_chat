import time
import address_book
import network_utils as nu
import socket

settings = {}

def load_settings():
    global settings
    with open("settings.conf") as f:
        for line in f:
            key, value = line.strip().split("=")
            settings[key] = value

class CheatChatDaemon:
    def __init__(self):
        self.address_book = address_book.ConcurrentAddressBookProxy()

    def run(self):
        self.listen_udp()

    def listen_udp(self):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the local IP address and port
        sock.bind((settings["local_ip"], int(settings["port"])))
        print(f"Listening on {settings["local_ip"]}:{int(settings["port"])}")
        while True:
            # Receive data from the socket
            data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
            print(f"Received message: {data} from {addr}")

if __name__ == "__main__":
    daemon = CheatChatDaemon()
    load_settings()
    local_ip = nu.get_local_ip(settings["netinterface"])
    subnet_mask = nu.get_subnet_mask(settings["netinterface"])
    broadcast_address = nu.calculate_broadcast_address(local_ip, subnet_mask)
    print("Local IP address:", local_ip)
    print("Subnet mask:", subnet_mask)
    print("Broadcast address:", broadcast_address)
    settings["broadcast_address"] = broadcast_address
    settings["local_ip"] = local_ip
    settings["subnet_mask"] = subnet_mask
    daemon.run()

