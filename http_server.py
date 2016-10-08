#!/usr/bin/env python
import urllib.parse
from message_generator import MessageGenerator
from http.server import BaseHTTPRequestHandler, HTTPServer

msg_gen = MessageGenerator()

class S(BaseHTTPRequestHandler):

  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def do_GET(self):
    self._set_headers()
    self.wfile.write("<html><body><h1>Please don't get me</h1></body></html>")

  def do_HEAD(self):
    self._set_headers()

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    post_str = str(post_data).replace("b\'","")
    phone_and_sms = post_str.split("&")
    qs = urllib.parse.parse_qs(post_str)
    self._set_headers()
    massage = msg_gen.message_request(qs['phone'],qs['sms'])
    message = "\{\"body\":\""+ massage + "\"\}"
    self.wfile.write(bytes(message+"\n", "utf8"))

def run(server_class=HTTPServer, handler_class=S, port=88):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print('Starting httpd...')
  httpd.serve_forever()

run()
