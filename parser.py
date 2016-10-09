from flask import Flask, request, redirect
import re
from email.utils import formatdate
import twilio.twiml
import http.client, urllib.parse

app = Flask(__name__)

#set recieiving message data

def incoming_sms_time():
    # Get the time of the message
    timeReceived = request.values.get('DateCreated', formatdate())
    return str(timeReceived)

def incoming_sms_from():
    # Get the number of the sender
    numFrom = request.values.get('From', None)
    return str(numFrom)

def incoming_sms_body():
    # Get the body of the text and sanitise for &'s
    badBody = request.values.get('Body', None)
    regexBody = re.compile(r'\&')
    body = regexBody.sub("+",badBody)
    return str(body)

@app.route("/", methods=['GET', 'POST'])

#receive message functions

def post_to_trill():
    timeReceived = incoming_sms_time()
    numFrom = incoming_sms_from()
    body = incoming_sms_body()
    params = urllib.parse.urlencode({'phone': numFrom, 'sms': body, 'time':timeReceived})
    headers = {"Content-type": "text/plain","Accept": "text/plain"}
    conn = http.client.HTTPConnection("192.168.80.2",88)
    conn.request("POST", "", params, headers)
    response = conn.getresponse()
    print(response)


# def debug_echo():
#     message = "message was sent at " + incoming_sms_time() + " from " + incoming_sms_from() + " with the content - " + "'" + incoming_sms_body() + "'"
#     resp = twilio.twiml.Response()
    # resp.message(message)
    # return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
