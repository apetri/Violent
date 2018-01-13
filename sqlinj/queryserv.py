#!/usr/bin/env python

#system
import sys
import logging
import argparse
import sqlite3

#library
import lib.database
import lib.http

###############
#Handle client#
###############

def sendQueryForm(clnt,msg=""):
	clnt.send(msg+clnt.makeForm("submit","query",[("username","text"),("password","password")]))

def handleClient(serv,dbase,table_style,fields=["First","Last","Age","Phone","Address","City","Zip","Email"]):
	
	#Accept connection
	with serv.accept() as clnt:

		#Read initial line of the request
		method,request,version = clnt.parseRequest()

		if request=="/" or request.startswith("/query"):

			#################################
			#Handle queries from the browser#
			#################################

			qdict = clnt.parseQuery(request)
			
			#Terminate early
			if qdict is None:
				sendQueryForm(clnt)
				return

			#There is a password field, hash it
			qdict["password"] = dbase.hashpwd(qdict["password"])

			###########################################################
			#Build the query; build in the SQL injection vulnerability#
			###########################################################

			dbquery = "SELECT {0} FROM people WHERE username='{1}' AND password='{2}'".format(",".join(fields),qdict["username"],qdict["password"])
			dbquery = dbquery.split(";")[0]
			logging.info("Sending query: {0}".format(dbquery))

			#Execute the query
			try:
				results = dbase.query(dbquery)
			except sqlite3.OperationalError:
				logging.info("Invalid SQL query.")
				sendQueryForm(clnt,msg="Invalid query\n")
				return

			##############################################
			#Build the response formatted in a HTML table#
			##############################################

			content = clnt.makeTable(results)
			content += clnt.makeForm('"query again"',"query",[])
			clnt.send(content,header=table_style)

		elif request=="/favicon.ico":
			sendQueryForm(clnt)
			return
		
		else:
			logging.error(request)
			raise NotImplementedError


################
#Main execution#
################

def main():

	#Log
	logging.basicConfig(level=logging.INFO)
	
	#Command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-p","--port",dest="port",type=int,default=8888,help="Server port")
	parser.add_argument("-d","--database",dest="database",help="Database file")
	parser.add_argument("-s","--style",dest="table_style",default="table_style.html",help="HTML file with table styling")

	#Parse
	cmd_args = parser.parse_args()
	if (cmd_args.database) is None:
		parser.print_help()
		sys.exit(1)

	################################################################

	#Load style file
	logging.info("Loading HTML template from: {0}".format(cmd_args.table_style))
	with open(cmd_args.table_style,"r") as fp:
		table_style = fp.read()

	#################################
	#Open connection to the database#
	#################################

	with lib.database.PeopleDatabase(cmd_args.database) as dbase:

		##################
		#Start web server#
		##################

		with lib.http.HTTPServer(cmd_args.port,1) as serv:

			#Handle requests from client
			while True:
				handleClient(serv,dbase,table_style)


if __name__=="__main__":
	main()