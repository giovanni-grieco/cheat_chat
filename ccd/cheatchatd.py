import time
import address_book
import network_utils as nu
import socket
import threading

settings = {}

def load_settings():
    global settings
    with open("settings.conf") as f:
        for line in f:
            key, value = line.strip().split("=")
            settings[key] = value

class CheatChatDaemon:
    def __init__(self):
        load_settings()
        local_ip = nu.get_local_ip(settings["netinterface"])
        subnet_mask = nu.get_subnet_mask(settings["netinterface"])
        broadcast_address = nu.calculate_broadcast_address(local_ip, subnet_mask)
        print("Local IP address:", local_ip)
        print("Subnet mask:", subnet_mask)
        print("Broadcast address:", broadcast_address)
        settings["broadcast_address"] = "desktop-fedora"               # broadcast_address
        settings["local_ip"] = local_ip
        settings["subnet_mask"] = subnet_mask
        self.address_book = address_book.ConcurrentAddressBookProxy()
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listen_sock.bind(("0.0.0.0", int(settings["port"])))
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.send_sock.bind((settings["local_ip"],47853))
        self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.stop_event = threading.Event()

    def run(self):
        listenerThread = threading.Thread(target=self.listen_udp)
        advertiserThread = threading.Thread(target=self.advertise)
        listenerThread.start()
        advertiserThread.start()
        reader = input("Press enter to stop\n")
        self.stop_event.set()
        listenerThread.join()
        advertiserThread.join()

    def listen_udp(self):
        print(f"Listening on {settings["local_ip"]}:{int(settings["port"])}")
        self.listen_sock.settimeout(1)
        while not self.stop_event.is_set():
            try:
                data, addr = self.listen_sock.recvfrom(1024)
                address_string = addr[0]
                print(f"Received message: {data} from {addr}")
                if(address_string != settings["local_ip"]):
                    print(f"Received message: {data} from {addr}")
            except socket.timeout:
                continue
        
                
        

    def advertise(self):
        while not self.stop_event.is_set():
            nu.send_udp_packet("CCProto|Hello", settings["broadcast_address"], int(settings["port"]), self.send_sock)
            time.sleep(1)
        print("Stopping advertiser")
        nu.send_udp_packet("CCProto|Bye", settings["broadcast_address"], int(settings["port"]), self.send_sock)

if __name__ == "__main__":
    daemon = CheatChatDaemon()
    daemon.run()

