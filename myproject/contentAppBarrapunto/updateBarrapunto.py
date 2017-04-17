from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib2
import sys
import os

class myContentHandler(ContentHandler):
    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.link = []
        self.title = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem: #dentro de <item> vemos si encontramos <title> o <link>
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item': #etiqueta de cierre </...>
            self.inItem = False
        elif self.inItem: #tengo contenido que me interesa
            if name == 'title': #si lo que se cierra es title
                self.title = self.theContent
                self.inContent = False  #he terminado de leer una etiqueta y lo reinicializo
                self.theContent = ""
            elif name == 'link': #si lo que se cierra es link
                self.link.append("<li><h3><a href='" + self.theContent + "'>" + self.title + "</a></h3></li>")
                self.inContent = False  #he terminado de leer una etiqueta y lo reinicializo
                self.theContent = ""
                self.title = ""

    def characters (self, chars):  #si tenemos contenido, lo guardamos
        if self.inContent:
            self.theContent = self.theContent + chars

# Load parser and driver
def update():
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    f = urllib2.urlopen('http://barrapunto.com/index.rss')
    theParser.parse(f)
    return (theHandler.link)

#xmlfile = open('barrapunto.txt', "r")
#theParser.parse(xmlfile)

# creamos un fichero con la pagina barrapunto actual
# podemos meter lo que leamos en una variable no tiene porque ser un fichero
# tiene que ser una variable global
# cont_rss = cont_rss + nuevo_link

"""cont_rss = "<html><head></head><body><ul>"
# Load parser and driver
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)
cont_rss = cont_rss + "</ul></body></html>"
url = "http://barrapunto.com/barrapunto.rss"
f = urllib.request.urlopen(url)
theParser.parse(f)
"""
