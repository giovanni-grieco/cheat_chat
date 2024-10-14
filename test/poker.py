import socket

from network import network_utils as nu
from protocol import make_poke_packet

if __name__ == "__main__":
    message = "Hello, UDP!"
    address = "192.168.1.6"  # Replace with the target address
    port = 10011  # Replace with the target port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    nu.send_udp_packet(make_poke_packet("MARCO"), address, port, sock)
