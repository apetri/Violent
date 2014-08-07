from __future__ import print_function,with_statement

import sys,os
import urllib2
import argparse
from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS

#Find image tags in a webpage
def findImages(url):
	
	print("[+] Finding images on {0}".format(url))
	urlContent = urllib2.urlopen(url).read()
	soup = BeautifulSoup(urlContent)
	imgTags = soup.findAll("img")
	return imgTags

#Download the images
def downloadImage(url,imgTag,downloads):
		
	imgSrc = imgTag["src"]
	print("[+] Downloading image {0}...".format(imgSrc))
	
	try:
		imgContent = urllib2.urlopen(imgSrc).read()
	except:
		imgContent = urllib2.urlopen(urllib2.os.path.join(url,imgSrc.lstrip("/"))).read()
	finally:
		
		imgFileName = basename(urlsplit(imgSrc)[2])
		netloc = urlsplit(url)[1]
		imgFile = open(os.path.join(downloads,netloc,imgFileName),"wb")
		imgFile.write(imgContent)
		imgFile.close()

		return imgFileName

#Test images for exif tags
def testForExif(imgFileName):

	try:
		
		exifData = {}
		imgFile = Image.open(imgFileName)
		info = imgFile._getexif()

		if info:
			
			for (tag,value) in info.items():
				decoded = TAGS.get(tag,tag)
				exifData[decoded] = value
			
			exifGPS = exifData["GPSInfo"]

			if exifGPS:
				print("[*] {0} contains GPS MetaData".format(imgFileName))
	
	except Exception,e:
		print("ERROR: ",e)
		
		pass
			
def main():
	
	#Argument parsing
	parser = argparse.ArgumentParser()
	parser.add_argument("-u","--url",dest="url",action="store",help="URL to examine")
	parser.add_argument("-d","--donwloads",dest="downloads",action="store",default="downloads",help="image download folder")

	#Parse command line arguments
	cmd_args = parser.parse_args()

	#Check
	if cmd_args.url is None:
		parser.print_help()
		sys.exit(0)
	
	#Proceed with url analysis
	url = cmd_args.url
	netloc = urlsplit(url)[1]
	downloads = cmd_args.downloads

	if not os.path.isdir(downloads):
		os.mkdir(downloads)
	
	if not os.path.isdir(os.path.join(downloads,netloc)):
		os.mkdir(os.path.join(downloads,netloc))
	
	imgTags = findImages(url)

	for imgTag in imgTags:
		
		imgFileName = downloadImage(url,imgTag,downloads)
		testForExif(os.path.join(downloads,netloc,imgFileName))

if __name__=="__main__":
	main()
