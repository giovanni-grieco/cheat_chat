import socket
import network_utils as nu
if __name__ == "__main__":
    message = "Hello, UDP!"
    address = "192.168.1.255"  # Replace with the target address
    port = 10011  # Replace with the target port
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    nu.send_udp_packet(message, address, port, sock)