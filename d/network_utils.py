import socket
import netifaces
import struct

def get_local_ip(interface: str):
    # Create a socket and connect to an external server
    info = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    return info

def get_subnet_mask(interface: str):
    # Get the subnet mask for the specified interface
    netmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
    return netmask

def calculate_broadcast_address(local_ip: str, subnet_mask: str) -> str:
    # Convert IP address and subnet mask to binary form
    ip_bin = struct.unpack('!I', socket.inet_aton(local_ip))[0]
    mask_bin = struct.unpack('!I', socket.inet_aton(subnet_mask))[0]
    
    # Calculate the broadcast address
    broadcast_bin = ip_bin | ~mask_bin & 0xFFFFFFFF
    
    # Convert the broadcast address back to dotted decimal format
    broadcast_address = socket.inet_ntoa(struct.pack('!I', broadcast_bin))
    return broadcast_address