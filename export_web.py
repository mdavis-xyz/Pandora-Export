#!/usr/bin/env python3

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from export import Exporter
from threading import Thread
from io import StringIO 
import sys

# mock exporter for testing
class FakeLogic(object):
  def __init__(self):
    object.__init__(self)
    print("logic inited")

  def login(self, userid, password):
    print("do fk login")

  def getLikes(self):
    print("do fk getLikes")

  def getJson(self, fname):
    return "[ %s ]" % fname

  def save(self, fullFileName='full.json', neatFileName = 'neat.json'):
    print("do fk save")

jsonThumbData = { }

class Server(BaseHTTPRequestHandler):


  def do_GET(self):
    if self.path == "/":
      jsonThumbData.clear()
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      with open("index.html") as infile:
        index_html = infile.read()
      self.wfile.write(bytes(index_html, "utf-8"))

# uncomment this if you want to put stylesheets etc. in
# a directory, e.g. "/assets"
#    elif self.path.startswith("/assets/"):
#      path = self.path[1:]
#      try:
#        with open(path) as infile:
#          conts = infile.read()
#        self.send_response(200)
#        self.end_headers()
#        self.wfile.write(bytes(conts, "utf-8"))
#      except FileNotFoundError:
#        pass

    elif (self.path[1:] in ["full.json", "neat.json"]) and self.path[1:] in jsonThumbData.keys():
      print("json req", self.path)

      path = self.path[1:]
      self.send_response(200)
      data = jsonThumbData[path]
      self.send_header("Content-type", "application/json")
      self.send_header("Content-Disposition", "attachment")
      self.end_headers()
      self.wfile.write(bytes(data, "utf-8"))

    else:
      print("bad req", self.path)
      self.send_response(404)
      self.send_header("Content-type", "text/plain")
      self.end_headers()
      self.wfile.write(bytes("", "utf-8"))

  def do_POST(self):

    print( "incomming http: ", self.path )
    if self.path.startswith("/export"):

      form = cgi.FieldStorage(
                 fp=self.rfile, 
                 headers=self.headers,
                 environ={'REQUEST_METHOD':'POST',
                          'CONTENT_TYPE':self.headers['Content-Type'],
                          })

      userid = form["userid"].value
      password = form["password"].value

      self.exporter = Exporter()
      #self.exporter = FakeLogic()
      exp = self.exporter
      exp.login(userid, password)

      def work():
        self.exporter.getLikes()
        for fname in ["full.json", "neat.json"]:
          jsonThumbData[fname] = self.exporter.getJson(fname)


      worker = Thread(target=work)
      worker.start()

      self.send_response(200)
      self.send_header("Content-type", "text/plain")
      self.end_headers()
      self.wfile.write(bytes("", "utf-8"))

 
def main(hostPort):
  hostName = ""
  server = HTTPServer((hostName, hostPort), Server)
  print("server started - %s:%s" % (hostName, hostPort))
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    pass

  server.server_close()

MAIN="__main__" 
#MAIN=None

if __name__ == MAIN:
  args = sys.argv[1:]
  if len(args) > 0:
    hostPort = int(args[0])
  else:
    hostPort = 8085
  main(hostPort)

