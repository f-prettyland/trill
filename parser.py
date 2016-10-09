from flask import Flask, request, redirect
import re
from email.Utils import formatdate
import twilio.twiml

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
    



def debug_echo():
    message = "message was sent at " + incoming_sms_time() + " from " + incoming_sms_from() + " with the content - " + "'" + incoming_sms_body() + "'"
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
