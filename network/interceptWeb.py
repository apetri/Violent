from scapy.all import *
from socket import gethostbyaddr,herror

import argparse

import sys,signal

def handler(sig,frame):
	for client in traffic_data.keys():
		print("{0}->{1}".format(client,traffic_data[client]))
	
	sys.exit(0)

traffic_data = dict()

def interceptWeb(pkt):
	
	if pkt.haslayer(IP):
	
		ip = pkt.getlayer(IP)
		source = ip.src
		destination = ip.dst
	
	else:
		return
	
	if not(pkt.haslayer(Raw) and "GET" in pkt.getlayer(Raw).load):
		return

	if source not in traffic_data.keys():
		new_client = True
		for client in traffic_data.keys():
			if source not in traffic_data[client] and destination not in traffic_data.keys():
				continue
			else:
				new_client = False
				break
		
		if(new_client):
			print("[+] Found new client: {0}".format(source))
			traffic_data[source] = list()
		
		
	if source in traffic_data.keys():
		
		if destination not in traffic_data[source]:
			traffic_data[source].append(destination)
			try:
				print("[+] Client: {0} issued GET request to {1}({2})".format(source,gethostbyaddr(destination)[0],destination))
			except herror:
				print("[+] Client: {0} issued GET request to {1}".format(source,destination))


def main():
	
	signal.signal(signal.SIGINT,handler)
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--interface",dest="interface",action="store",default="eth0",help="network interface")
	
	cmd_args = parser.parse_args()
	
	conf.iface = cmd_args.interface
	
	try:
		print("[*] Starting web traffic interception on {0}".format(conf.iface))
		sniff(filter="tcp port 80",prn=interceptWeb,store=0)
	except (KeyboardInterrupt,SystemExit):
		print("[-]KeyboardInterrupt detected, quitting")
		exit(0)

if __name__ == "__main__":
	main()