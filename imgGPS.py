from __future__ import print_function,with_statement,division

import sys
from imgFetch import testForExif,interpretGPS

def main():
	
	gpsTag = testForExif(sys.argv[1])
	if gpsTag:
		print(interpretGPS(gpsTag))

if __name__=="__main__":
	main()