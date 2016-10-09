#!/usr/bin/env python
'''
Example call:
  curl -d "phone=0000000822&sms=Hello world&time=2016-10-07T20:47:56.000-04:00" http://localhost:88

Run this with "sudo python3 http_server.py"
'''
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
    qs = urllib.parse.parse_qs(post_str)
    self._set_headers()
    if qs['sms']:
      massage = msg_gen.message_request(qs['phone'],qs['sms'],qs['time'])
    elif qs['lat']:
      massage = msg_gen.gps_message_request(qs['phone'],
                                            qs['long'],
                                            qs['lat'],
                                            qs['time'])
    else:
      massage = UNKNOWN_REQ
    self.wfile.write(bytes(massage, "utf8"))

def run(server_class=HTTPServer, handler_class=S, port=88):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print('Listening for reports...')
  httpd.serve_forever()

run()
