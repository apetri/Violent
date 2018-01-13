#system
import socket
import logging
import urllib

#############
#Http server#
#############

class HTTPServer(object):

	#Constructor
	def __init__(self,port,maxcon):

		#Initialize server socket
		self.host = "localhost"
		self.port = port
		self.maxcon = maxcon
		self.serv = socket.socket()
		self.serv.bind(("localhost",port))
		self.serv.listen(maxcon)
		logging.info("Started HTTP server listening on {0}:{1}, maxcon={2}".format(self.host,self.port,self.maxcon))

	#Context manager
	def __enter__(self):
		return self

	def __exit__(self,*args):
		self.stop()

	#Accept connection
	def accept(self):
		return BrowserClient(*self.serv.accept())

	#Stop server
	def stop(self):
		logging.info("Stopped HTTP server on {0}:{1}".format(self.host,self.port))
		self.serv.close()


################
#Client browser#
################

class BrowserClient(object):

	_http_header = "HTTP/1.0 {0[0]} {0[1]}\r\n\r\n"

	#Constructor
	def __init__(self,clntsock,clntaddr):

		#Initalize client socket
		self.clntsock = clntsock
		self.clntip = clntaddr[0]
		self.clntport = clntaddr[1]
		self.clntfp = self.clntsock.makefile()
		logging.info("Accepted connection from client at {0}.".format(self.clntip))

	#Context manager
	def __enter__(self):
		return self

	def __exit__(self,*args):
		logging.info("Closed connection from client at {0}.".format(self.clntip))
		self.clntfp.close()
		self.clntsock.close()

	######################
	#Parse server request#
	######################

	def parseRequest(self):
		return self.clntfp.readline().strip("\r\n").split(" ")

	@staticmethod
	def parseQuery(request):

		#Split request string
		tok = request.find("?")
		if tok==-1:
			return None

		method = request[:tok]
		query = urllib.unquote_plus(request[tok+1:])
		if not len(query):
			return None

		#Parse the query
		if method!="/query":
			return None

		qdict = dict()
		for clause in query.split("&"):
			tok = clause.find("=")
			k = clause[:tok]
			v = clause[tok+1:]
			qdict[k] = v

		return qdict


	###############################
	#Send HTML formatted responses#
	###############################

	#Basic html formatted send
	def send(self,content,header="",code=[200,"OK"]):

		#Header
		self.clntsock.sendall(self._http_header.format(code))

		#Html body
		page = "<html>" + header  + "<body>\r\n" + content + "</body></html>\r\n"
		self.clntsock.sendall(page)

	#################################################################

	#Make formatted html table
	@staticmethod
	def makeTable(records):

		#Begin table
		content = "<p><table border>\n"
		
		#Header
		content += "<tr>" + "\n".join(["<th>{0}</th>".format(f) for f in records[0]]) + "\n</tr>\n"

		#Records
		for rec in records[1:]:
			content += "<tr>\n" + "\n".join(["<td>{0}</td>".format(f) for f in rec]) + "\n</tr>\n"
		
		#End table
		content += "</table></p>\n"
		return content

	####################################################

	#Make form
	@staticmethod
	def makeForm(button_name,action,fields):

		#Compose form
		form = "<form method=GET action=/{0}>\n".format(action)
		for f in fields:
			form += "{0[0]}: <input type={0[1]} name={0[0]}><br>\n".format(f)
		form += "<input type=submit value={0}>\n".format(button_name)
		form += "</form>\n</p>\n"

		#Return
		return form
