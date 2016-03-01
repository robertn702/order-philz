"""listens for dash button press"""
from order_coffee import order_coffee
import binascii
import socket
import struct

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

rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
# rawSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.htons(0x0003))

while True:
    packet = rawSocket.recvfrom(2048)
    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
    # skip non-ARP packets
    ethertype = ethernet_detailed[2]
    if ethertype != '\x08\x06':
        continue
    # read out data
    arp_header = packet[0][14:42]
    arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
    source_mac = binascii.hexlify(arp_detailed[5])
    source_ip = socket.inet_ntoa(arp_detailed[6])
    dest_ip = socket.inet_ntoa(arp_detailed[8])

    if source_mac in MACS:
        print 'source: ' + MACS[source_mac]
        if MACS[source_mac] == 'coffee_dash':
            print 'coffee_dash button fired!'
            order_coffee()
    else:
        print "Unknown MAC " + source_mac + " from IP " + source_ip
