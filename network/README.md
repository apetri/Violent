Contents
========

interceptWeb.py
---------------

Parses network traffic coming from a network interface and looks for the web history of the user, updating the sniffer on any new websites visited. Usage is as follows

	python interceptWeb.py -i <network interface to sniff on (e.g. en1)>

sniffpkt.py
-----------

Uses the scapy funcionalities to intercept 802.11 beacon frames captured by the sniffer's network adapter in monitor mode (mon0 in this example). Usage is as follows
	
	python sniffpkt.py

Dependencies
------------

Both the scripts above depend on the [scapy](http://www.secdev.org/projects/scapy/doc/) library