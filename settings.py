#!/usr/bin/env python3
import os
from datetime import datetime

CATAGORIES_FILE="catagories.csv"
JAAAASON="temp.json"

FILE_LOC = "out/"
DEFAULT_LANG = "en"

NONMATCH_RESP=FILE_LOC+"log.csv"
LOCATION="start"
FINALE="end"
QUESTION="question"
ANSWERS="answers"
ANSWER_NUM="answer_number"
ANSWER_VAL="answer_text"
SMRT_KEY="smart_key"
SMRT_KEY_TYPE="smart_key_type"
SMRT_VAL_KEY="smart_value_key"
SEPARATOR="  "

NON_REGISTERED_NUM="Your number is not registered"
UNKNOWN_REQ="Unknown request"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
INPUT_FOLD="input"
debug=True

def log_response(number, sms):
  with open(NONMATCH_RESP, "a") as responses_file:
    responses_file.write("{0}, {1}, {2}".format(datetime.now().time(), number, sms))
