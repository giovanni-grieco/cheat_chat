import socket
import time
from ccd import network_utils
from ccd import system_utils

if __name__ == "__main__":

    system_utils.send_notification("Hello, UDP!")

    message = "Hello, UDP!"
    address = "192.168.1.255"  # Replace with the target address
    port = 10011  # Replace with the target port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        while True:
            network_utils.send_udp_packet(message, address, port, sock)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
