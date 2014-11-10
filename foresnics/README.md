Contents
========

imgFetch.py
-----------

Takes a URL as input, connects to that URL and scans it for images; when it finds one it downloads it and searches for EXIF tags that can help with geolocation. Usage is as follows

	python imgFetch.py -u <url_to_scan> -d <image_download_folder>


imgGPS.py
---------

Same as imgFetch.py except that it works on local images and prints the complete GPS information. Usage is as follows

	python imgGPS.py <image_file to scan for GPS tags>

Dependencies
------------

Both the above scripts depend on the Python Imaging Library [PIL](http://www.pythonware.com/products/pil/) and on the [BeautifulSoup](https://pypi.python.org/pypi/BeautifulSoup) package