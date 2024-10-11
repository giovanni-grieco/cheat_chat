import time
import address_book
import network_utils as nu
import socket
import threading
import random
import peer

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
        default_interface = nu.get_default_interface()
        settings["netinterface"] = default_interface
        print("Default network interface:", default_interface)
        local_ip = nu.get_local_ip(settings["netinterface"])
        subnet_mask = nu.get_subnet_mask(settings["netinterface"])
        broadcast_address = nu.calculate_broadcast_address(local_ip, subnet_mask)
        print("Local IP address:", local_ip)
        print("Subnet mask:", subnet_mask)
        print("Broadcast address:", broadcast_address)
        settings["broadcast_address"] = broadcast_address #"desktop-fedora"
        settings["local_ip"] = local_ip
        settings["subnet_mask"] = subnet_mask
        self.address_book = address_book.ConcurrentAddressBookProxy()
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

    def run(self):
        try:
            listenerThread = threading.Thread(target=self.listen_udp)
            advertiserThread = threading.Thread(target=self.advertise)
            listenerThread.start()
            advertiserThread.start()
            listenerThread.join()
            advertiserThread.join()
        except KeyboardInterrupt:
            self.stop_event.set()
            listenerThread.join()
            advertiserThread.join()
            self.listen_sock.close()
            self.send_sock.close()
            print("Exiting...")

    def listen_udp(self):
        print(f"Listening on {settings["local_ip"]}:{int(settings["port"])}")
        self.listen_sock.settimeout(1)
        while not self.stop_event.is_set():
            try:
                data, addr = self.listen_sock.recvfrom(1024)
                address_string = addr[0]
                #print(f"Received message: {data} from {addr}")
                if(address_string != settings["local_ip"]):
                    print(f"Received message: {data} from {addr}")
                    event = str(data.split(b"|")[1])
                    username = str(data.split(b"|")[2])
                    if(event == "Hello"):
                        new_peer : peer.Peer = peer.Peer(username, address_string, time.time())
                        self.address_book.addPeer(new_peer) #Forse non funziona lui?
                    elif(event == "Bye"):
                        self.address_book.remove_address(address_string)
                else:
                    print("Received message from self")
            
                print(self.address_book.to_string()) # NON FUNZIONA???

            except socket.timeout:
                continue
        print("Stopping listener")
        
                
        

    def advertise(self):
        while not self.stop_event.is_set():
            nu.send_udp_packet(f"CCProto|Hello|{settings["username"]}", settings["broadcast_address"], int(settings["port"]), self.send_sock)
            time.sleep(10+random.randint(-5, 5))
        print("Stopping advertiser")
        nu.send_udp_packet(f"CCProto|Hello|{settings["username"]}", settings["broadcast_address"], int(settings["port"]), self.send_sock)

if __name__ == "__main__":
    daemon = CheatChatDaemon()
    daemon.run()

