import socket

def send_udp_packet(message, address, port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Send the UDP packet
        sock.sendto(message.encode(), (address, port))
        print(f"Sent message: {message} to {address}:{port}")
    finally:
        # Close the socket
        sock.close()

if __name__ == "__main__":
    message = "Hello, UDP!"
    address = "localhost"  # Replace with the target address
    port = 10011  # Replace with the target port
    send_udp_packet(message, address, port)