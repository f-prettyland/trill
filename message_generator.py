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
from settings import __location__, INPUT_FOLD, debug, log_response

class MessageGenerator:
  svr_handler = None
  people = {}

  def __init__(self):
    input_loc = os.path.join(__location__,INPUT_FOLD + "/")

    self.svr_handler = SurveyHandler(input_loc)

  def get_initial_text_catagories(self, to_parse):
    id_catagories = []
    inputted_lang = None
    for lang in self.svr_handler.catagories.keys():
      for catagory in self.svr_handler.catagories[lang].keys():
        if check_for(to_parse, self.svr_handler.catagories[lang][catagory]):
          inputted_lang = lang
          id_catagories.append(catagory)

    return (id_catagories, inputted_lang)

  def make_person(self, number, to_parse, time):
    (id_catagories, lang) = self.get_initial_text_catagories(to_parse)
    debug_print("\nIdentifying: \n{0}\nGot these:\n{1}\n"
                .format(to_parse, id_catagories))
    incident_xml = IncidentXMLWriter(to_parse,
                              id_catagories,
                              time)
    if lang:
      question_catagories = self.svr_handler.getQuestionCatagories(id_catagories,
                                                                lang)
    else:
      question_catagories = []
    return Person(number, question_catagories, datetime.now(),
                  incident_xml, lang)

  def message_request(self, phone_nums, sms_bodys, times):
    phone_num = phone_nums[0]
    sms_body = sms_bodys[0]
    # trim off apos
    reg_endline = re.compile(r'\'$')
    time = reg_endline.sub("",times[0])
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

  def gps_message_request(self, phone_nums, longs, lats, times):
    phone_num = phone_nums[0]
    lon = longs[0]
    lat = lats[0]
    # trim off apos
    reg_endline = re.compile(r'\'$')
    time = reg_endline.sub("",times[0])
    response = None
    if phone_num in self.people.keys():
      response = self.svr_handler.mark_gps_answer(self.people[phone_num],
                                                  lon,
                                                  lat,
                                                  time)
      if self.people[phone_num].finished:
        del self.people[phone_num]

      return response
    else:
      log_response(phone_nums, "Unknown id with x:{0} and y:{1}".format(lon,lat))
      return NON_REGISTERED_NUM


def debug_print(string):
  if debug:
    print(string)

def check_for(checkee, words):
  regex = re.compile('|'.join(r'(?:|^)'+re.escape(x)+r'(?:|$)'
                      for x in words))
  return re.search( regex, checkee)
