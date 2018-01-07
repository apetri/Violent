#!/usr/bin/env python

#system
import sys
import logging
import argparse

#library
import lib


################
#Main execution#
################

def main():

	#Log
	logging.basicConfig(level=logging.INFO)
	
	#Command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-p","--port",dest="port",default=8888,help="Server port")
	parser.add_argument("-d","--database",dest="database",help="Database file")
	parser.add_argument("-s","--style",dest="table_style",default="table_style.html",help="HTML file with table styling")

	#Parse
	cmd_args = parser.parse_args()
	if (cmd_args.database) is None:
		parser.print_help()
		sys.exit(1)

	################################################################


if __name__=="__main__":
	main()