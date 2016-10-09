#!/usr/bin/env python3
# curl -d "phone=0000000822&sms=1&time=2016-10-07T20:47:56.000-04:00" http://localhost:88
import http.client, urllib.parse
params = urllib.parse.urlencode({'phone': 123123, 'sms': 'Mortinta leonon kaj en kaptilo', 'time': '2016-10-07T20:47:56.000-04:00'})
headers = {"Content-type": "text/plain","Accept": "text/plain"}
conn = http.client.HTTPConnection("127.0.0.1",88)
conn.request("POST", "", params, headers)
response = conn.getresponse()
print(response)
