from __future__ import print_function
from scapy.all import *

#Print info about the sniffed packets

def pktPrint(pkt):
	
	if pkt.haslayer(Dot11Beacon):
		print("[+] Detected 802.11 Beacon Frame")
	elif pkt.haslayer(Dot11ProbeReq):
		print("[+] Detected 802.11 Probe Request Frame")
	elif pkt.haslayer(TCP):
		print("[+] Detected a TCP Packet")
	elif pkt.haslayer(DNS):
		print("[+] Detected a DNS Packet")

#Main execution
def main():
	
	conf.iface = "mon0"
	sniff(prn=pktPrint)

if __name__=="__main__":
	main()