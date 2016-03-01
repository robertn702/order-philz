"""listens for dash button press"""
import binascii
import socket
import struct

from order_coffee import order_coffee

# Replace these fake MAC addresses and nicknames with your own
MACS = {
    '600308a708f0': 'macbook_pro',
    '74da3841131e': 'pi_web_server',
    '881fa12a2ae1': 'C',
    '9c207bf187d6': 'D',
    'a0edcd73b608': 'iphone5',
    'f0272dea868d': 'coffee_dash',
    '00a0deb8c82f': 'yamaha_receiver',
    '985aeb8de038': 'work_macbook_pro',
    '9cd21e6c1933': 'cheap_dell'
}

if hasattr(socket, 'AF_PACKET'):
    RAW_SOCKET = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
elif hasattr(socket, 'AF_INET'):
    RAW_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.htons(0x0003))

while True:
    PACKET = RAW_SOCKET.recvfrom(2048)
    ETHERNET_HEADER = PACKET[0][0:14]
    ETHERNET_DETAILED = struct.unpack("!6s6s2s", ETHERNET_HEADER)
    # skip non-ARP packets
    ETHERTYPE = ETHERNET_DETAILED[2]
    if ETHERTYPE != '\x08\x06':
        continue
    # read out data
    ARP_HEADER = PACKET[0][14:42]
    ARP_DETAILED = struct.unpack("2s2s1s1s2s6s4s6s4s", ARP_HEADER)
    SOURCE_MAC = binascii.hexlify(ARP_DETAILED[5])
    SOURCE_IP = socket.inet_ntoa(ARP_DETAILED[6])
    DEST_IP = socket.inet_ntoa(ARP_DETAILED[8])

    if SOURCE_MAC in MACS:
        print 'source: ' + MACS[SOURCE_MAC]
        if MACS[SOURCE_MAC] == 'coffee_dash':
            print 'coffee_dash button fired!'
            order_coffee()
    else:
        print "Unknown MAC " + SOURCE_MAC + " from IP " + SOURCE_IP
