import socket
from datetime import datetime
import struct
import binascii
import time
import json
import urllib2

# Replace these fake MAC addresses and nicknames with your own
macs = {
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

last_call = {}
max_time_diff = None
max_time_diff_2 = None

def order_coffee():
    print 'ordering coffee: '

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



    if source_mac in macs:
        print '['+str(datetime.now())+']' + ' mac: ' + macs[source_mac]
        # if macs[source_mac] == 'A':
        if macs[source_mac] == 'coffee_dash':
            if source_mac in last_call:
                time_diff = datetime.now() - last_call[source_mac]
                if max_time_diff == None or time_diff > max_time_diff:
                    max_time_diff = time_diff
                print 'time_diff: ' + str(time_diff)
                print 'max_time_diff: ' + str(max_time_diff)
        if macs[source_mac] == 'coffee_dash_2':
            if source_mac in last_call:
                time_diff = datetime.now() - last_call[source_mac]
                if max_time_diff_2 == None or time_diff > max_time_diff_2:
                    max_time_diff_2 = time_diff
                print 'time_diff: ' + str(time_diff)
                print 'max_time_diff_2: ' + str(max_time_diff_2)


        last_call[source_mac] = datetime.now()
    else:
        print "Unknown MAC " + source_mac + " from IP " + source_ip
