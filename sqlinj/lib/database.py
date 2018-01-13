#system
import logging
import sqlite3
import hashlib

#3rd party
try:
	import numpy as np
	import pandas as pd
except ImportError:
	np = None
	pd = None


###################################
#Random components of the database#
###################################

name = [["John","Jane","Adam","Toni","Puccio"],["Bastianelli","Smith","Cane"]]
address = [["St.","Ave.","Blvd."],["Wessex","Oak","Burrow"]]
city = ["New York","Boston","Philadelphia"]

def makeRandomDatabase(nrecords=100):

	#Need numpy and pandas
	if (np is None) or (pd is None):
		return None

	#First name, last name
	first = np.random.choice(name[0],nrecords)
	last = np.random.choice(name[1],nrecords)

	#Age
	age = np.random.randint(10,88,nrecords)

	#Address
	st1 = np.random.choice(address[0],nrecords)
	st2 = np.random.choice(address[1],nrecords)
	st3 = np.random.randint(1,1000,size=nrecords)
	zp = np.random.randint(10000,100000,size=nrecords)
	cty = np.random.choice(city,nrecords)

	#Phone number
	phone1 = np.random.randint(0,1000,size=nrecords)
	phone2 = np.random.randint(0,100,size=nrecords)
	phone3 = np.random.randint(0,10000,size=nrecords)

	#Build database
	db = pd.DataFrame({

		"First" : first,
		"Last" : last,
		"Age" : age,
		"Address" : [ str(st3[n]) + " " + st2[n] + " " + st1[n] for n in range(nrecords) ],
		"Zip" : zp,
		"City" : cty,
		"Email" : [ f+"@"+last[n]+".com" for n,f in enumerate(first) ],
		"Phone" : [ "{0:03d}-{1:02d}-{2:04d}".format(phone1[n],phone2[n],phone3[n]) for n in range(nrecords) ],
		"username" : [ f.lower()+last[n].lower() for n,f in enumerate(first) ],
		"password" : PeopleDatabase.hashpwd("puccio") 

		})

	#Return
	return db[["username","password","First","Last","Age","Phone","Address","City","Zip","Email"]]

#############################
#Connections to the database#
#############################

class PeopleDatabase(object):

	#Password hash
	@staticmethod
	def hashpwd(pwd):
		return hashlib.sha256(pwd).hexdigest()

	#Constructor, context managers
	def __init__(self,dbname):
		logging.info("Opened connection to database: {0}".format(dbname))
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname)
		self.cursor = self.conn.cursor()

	def __enter__(self):
		return self

	def __exit__(self,*args):
		logging.info("Closed connection to database: {0}".format(self.dbname))
		self.conn.close()

	#Send a query to the database and retrieve the results
	def query(self,q):
		records = self.cursor.execute(q)
		cnames = [ c[0] for c in self.cursor.description ]
		return [cnames] + list(records)