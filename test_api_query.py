#!/usr/bin/env python3
import re
import http.client, urllib.parse
'''
spin up http_server
>  python3 http_server.py
then call this function to hit it up.
cleanData should just be a nice string
'''

#Post message data to Trill API
def post_to_trill(body, numFrom, timeReceived):
  params = urllib.parse.urlencode({'phone': numFrom, 'sms': body, 'time':timeReceived})
  headers = {"Content-type": "text/plain","Accept": "text/plain"}
  conn = http.client.HTTPConnection("127.0.0.1",88)
  conn.request("POST", "", params, headers)
  response = conn.getresponse()
  data = response.read()
  conn.close()
  print(data)
  # regexData = re.compile(r"^'b(.*})\\n")
  cleanData = str(data).replace("\b'","")
  print("sleeeeep")
  #send_to_user(cleanData)
  print(cleanData)
  return(cleanData)
