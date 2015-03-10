#!/usr/bin/python

import webapp
import urllib

class shortUrl(webapp.webApp):
	dicUrlShort = {}
	dicUrlShortInv = {}
	counter = -1;

	def parse(self, request):
		metodo = request.split(' ',2)[0]
		if metodo == "GET":
			peticion = request.split(' ',2)[1][1:]
		elif metodo == "POST":
			peticion = request.split("\r\n\r\n")[-1]
			peticion = peticion.split("url=",2)[-1]
			peticion = peticion.split("http%3A%2F%2F",2)[-1]
			peticion = "http://" + peticion
		return (metodo,peticion)

	def process(self, parsedRequest):
		(metodo,peticion) = parsedRequest
		if metodo == "GET":
			if peticion in self.dicUrlShortInv:
				print "HOOOOLAAA " + str(self.dicUrlShortInv[peticion])
				return("300 Redirect", "<html><head><meta http-equiv='refresh' content='0;url=" 
						+ str(self.dicUrlShortInv[peticion])+ "'></head></html>")
			else:
				if peticion == "":
					return ("200 OK", "<html>""<head></head><body>" +
						str(self.dicUrlShort) +
						"<h3>Url acortada</h3><form method=post action=http://localhost:1234>" + 
				   		"url sin acortar:<input type = name name = url original></body>")
				else:
					return("400 Error", "<html>""<head></head><body> resource not found</body>")
		elif metodo == "POST":
			if peticion in self.dicUrlShort:
				return("200 OK", "<html><head></head><h1><a href='" + str(peticion) + "'>" 
					+ "http://localhost:1234/" + str(self.dicUrlShort[peticion]) + "-->" + str(peticion) 
					+ "</a></h1></body></html>")
			else:
				try:
					pag = urllib.urlopen(peticion)
				except IOError:
					return("400 ERROR","<html><head>Origin page not found</head><body></body>")

				self.counter += 1
				self.dicUrlShort[peticion] = self.counter
				self.dicUrlShortInv[str(self.counter)] = peticion
				return("200 OK", "<html><head></head><h1><a href='" + str(peticion) + "'>" 
					+ str(peticion)+ "-->" + "http://localhost:1234/" + str(self.dicUrlShort[peticion]) + "</a></h1></body></html>")
		else:
			return("200 OK", "<html><head></head><h1>aun sin programar</h1></body></html>")

if __name__ == "__main__":
    testWebApp = shortUrl("localhost", 1234)