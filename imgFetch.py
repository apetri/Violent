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
	netloc = urlsplit(url).netloc
	scheme = urlsplit(url).scheme
	path = urlsplit(url).path
	
	print("[+] Downloading image {0}...".format(imgSrc))
	
	try:
		imgContent = urllib2.urlopen(imgSrc).read()
	except:
		if "html" in urllib2.os.path.split(path)[-1]:
			root_path = urllib2.os.path.split(path)[0].lstrip("/")
		else:
			root_path = path.lstrip("/")
		
		imgUrl = urllib2.os.path.join("{0}://{1}".format(scheme,netloc),root_path,imgSrc.lstrip("/"))
		imgContent = urllib2.urlopen(imgUrl).read()
		
	finally:
		
		imgFileName = basename(urlsplit(imgSrc)[2])
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
				return exifGPS
			else:
				return None
	
	except Exception,e:
		print("ERROR: ",e)
		
		return None


#Interpret the GPS exif tag value
def interpretGPS(gpsTag):
	
	gpsInfo = dict()
	try:
		for key in gpsTag.keys():
			decoded = GPSTAGS.get(key,key)
			gpsInfo[decoded] = gpsTag[key]
		
		return gpsInfo
	
	except:
		return None

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
		gpsTag = testForExif(os.path.join(downloads,netloc,imgFileName))
		
		if gpsTag:
			print(interpretGPS(gpsTag))

if __name__=="__main__":
	main()
