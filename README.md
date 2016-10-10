# trill  
<img src="https://github.com/f-prettyland/trill/blob/master/examples/trill.png" width="80">
A hackathon project from `#zoohackathon`


This is designed to work with a SMART instance to allow anyone to submit incident reports to empower local people to help combat poaching and help with wildlife reporting, currently via SMS.

### Example SMS  
![SMS Example Discussion on Traps](./examples/SMS-comms.jpg)

## How  
`xml2csv/` is used to make a csv file from a data model, to create your own localisation keywords from an initial message.  
`xls/` is used to follow up certain keywords with question chains (`gavlar.py` can generate that to json)  
`twilio` is used to handle twilio responses then asks our API for a response  
`http_server`, our API, is used to serve all responses, first classifying the message (and so the number) by language and content data model catagory. Then all subsequent messages for this phone number will follow the communication question flow given by the json.

[See how.md for more details](./docs/how.md)

## Dependancies  
- `python3`
- `twilio`
- `http.server`
- `flask`
- `pyOpenSSL`

## Todo  
[See TODO.md](./docs/TODO.md)
