from __future__ import print_function,with_statement

import sys

import zipfile
import argparse
from threading import Thread

def extractFile(zFile,password):

	try:
		zFile.extractall(pwd=password)
		print("[+] Found password {0}".format(password))
	except:
		pass

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-f","--file",dest="zip_file",action="store",help="file name of the zip archive")
	parser.add_argument("-d","--dictionary",dest="dictionary",action="store",help="password dictionary file")

	args = parser.parse_args()

	zip_filename = args.zip_file
	dictionary = args.dictionary

	if zip_filename is None or dictionary is None:
		parser.print_help()
		sys.exit(0)

	#Main execution
	
	Found = False
	zFile = zipfile.ZipFile(zip_filename)
	
	#Read password dictionary
	with open(dictionary,"r") as dictfile:
		passwords = dictfile.readlines()
	
	#Brute force every password in the dictionary
	for line in passwords:
		password = line.rstrip("\n")
		t = Thread(target=extractFile,args=(zFile,password))
		t.start()

if __name__=="__main__":
	main()

