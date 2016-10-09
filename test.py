from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

# Try adding your own number to this list!
callers = {
    "+14158675309": "Curious George",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
    "+447787500884": "US!!",
}

@app.route("/", methods=['GET', 'POST'])

def incoming_sms_time():
    # Get the time of the message
    timeReceived = request.values.get('DateCreated', None)
    return str(timeReceived)

def incoming_sms_from():
    # Get the number of the sender
    numFrom = request.values.get('From', None)
    return str(numFrom)

def incoming_sms_body():
    # Get the body of the text and sanitise for &'s
    body = request.values.get('Body', None)
    re.sub(r'&(?![A-Za-z]+[0-9]*;|#[0-9]+;|#x[0-9a-fA-F]+;)',r'&amp;', body)
    return str(body)

def debug_echo():
    """Respond and greet the caller by name."""

    from_number = request.values.get('From', None)
    if from_number in callers:
        message = callers[from_number] + ", thanks for the message!"
    else:
        message = "Monkey, thanks for the message!"

    resp = twilio.twiml.Response()
    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
