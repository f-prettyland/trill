#!/usr/bin/env python3
import re
import os
import json
import string
import argparse
from person import Person
from datetime import datetime
from xml_writer import IncidentXMLWriter
from survey_handler import SurveyHandler

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
INPUT_FOLD="input"
INPUT_LANG="en"
CATAGORIES="catagories.csv"
JAAAASON="temp.json"
debug=True

class MessageGenerator:
  svr_handler = None
  people = {}

  def __init__(self):
    input_loc = os.path.join(__location__,INPUT_FOLD + "/" + \
                              INPUT_LANG + "/"+CATAGORIES)
    input_json_loc = os.path.join(__location__,INPUT_FOLD + "/" + \
                            INPUT_LANG + "/"+JAAAASON)

    data_file = open(input_json_loc)
    json_data = json.load(data_file)
    self.svr_handler = SurveyHandler(input_loc, json_data)

  def get_initial_text_catagories(self, to_parse):
    id_catagories = []
    for catagory in self.svr_handler.catagories.keys():
      if check_for(to_parse, self.svr_handler.catagories[catagory]):
        id_catagories.append(catagory)
    return id_catagories

  def make_person(self, number, to_parse, time):
    id_catagories = self.get_initial_text_catagories(to_parse)
    debug_print("\nIdentifying: \n{0}\nGot these:\n{1}\n"
                .format(to_parse, id_catagories))
    incident_xml = IncidentXMLWriter(to_parse,
                              id_catagories,
                              time)
    incident_xml.print_XML()
    question_catagories = self.svr_handler.getQuestionCatagories(id_catagories)
    return Person(number, question_catagories, datetime.now(), incident_xml)

  def message_request(self, phone_nums, sms_bodys, times):
    phone_num = phone_nums[0]
    sms_body = sms_bodys[0]
    # trim off apos
    endline = re.compile(r'\'$')
    time = endline.sub("",times[0])
    response = None

    if phone_num in self.people.keys():
      response = self.svr_handler.mark_get_next_question(self.people[phone_num],
                                                          sms_body,
                                                          time)
    else:
      self.people[phone_num] = self.make_person(phone_num, sms_body, time)
      response = self.svr_handler.mark_get_next_question(self.people[phone_num],
                                                          None,
                                                          time)
    if self.people[phone_num].finished:
      del self.people[phone_num]

    return response

def debug_print(string):
  if debug:
    print(string)

def check_for(checkee, words):
  regex = re.compile('|'.join(r'(?:|^)'+re.escape(x)+r'(?:|$)'
                      for x in words))
  return re.search( regex, checkee)
