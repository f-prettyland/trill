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
ASK_FOR_IN="Gimme a SMS\n"

class MessageGenerator:
  svr_handler = None

  def __init__(self):
    input_loc = os.path.join(__location__,INPUT_FOLD + "/" + \
                              INPUT_LANG + "/"+CATAGORIES)
    input_json_loc = os.path.join(__location__,INPUT_FOLD + "/" + \
                            INPUT_LANG + "/"+JAAAASON)

    data_file = open(input_json_loc)
    json_data = json.load(data_file)
    self.svr_handler = SurveyHandler(input_loc, json_data)

  def check_for(checkee, words):
    regex = re.compile('|'.join(r'(?:|^)'+re.escape(x)+r'(?:|$)'
                        for x in words))
    return re.search( regex, checkee)

  def get_initial_text_catagories(to_parse):
    id_catagories = []
    for catagory in self.svr_handler.catagories.keys():
      if check_for(to_parse, self.svr_handler.catagories[catagory]):
        id_catagories.append(catagory)
    return id_catagories

  def make_person(to_parse, number):
    print("\nIdentifying: \n", to_parse)
    print("\nGot these:")
    id_catagories = get_initial_text_catagories(to_parse)
    print(id_catagories)
    print("\n")

    incident_xml = IncidentXMLWriter(to_parse,
                              id_catagories,
                              "45.34",
                              "34.56",
                              "2016-10-07T20:47:56.000-04:00")
    incident_xml.printXML()

    return Person(number, id_catagories, datetime.now(), incident_xml)

  def message_request(self, phone_num, sms_body, time):
    return "From: " + phone_num[0] + "  You sent me "+ sms_body[0] + "  at  " + time[0]

# def main(results):
#   global svr_handler
#   input_loc = os.path.join(__location__,results.input_folder + "/" + \
#                           results.lang + "/"+CATAGORIES)
#   input_json_loc = os.path.join(__location__,results.input_folder + "/" + \
#                           results.lang + "/"+JAAAASON)
#
#   data_file = open(input_json_loc)
#   json_data = json.load(data_file)
#   svr_handler = SurveyHandler(input_loc, json_data)
#
#   to_parse = ""
#   if results.input:
#     to_parse = results.input
#   else:
#     to_parse = input(ASK_FOR_IN)
#
#   p = make_person(to_parse,"0909090909")
#   p.generateXML()
#
if __name__ == "__main__":
  msg_gen = MessageGenerator()
  print(msg_gen.message_request("909102", "hello"))
#   prsr = argparse.ArgumentParser(description='Identify what someone\'s chatting about')
#
#   prsr.add_argument('-d', dest='input_folder',
#                       help='File locaiton of word dictionaries')
#   prsr.add_argument('-l', dest='lang',
#                       help='Two letter language representation')
#   prsr.add_argument('-i', dest='input',
#                       help='A string to parse')
#   # prsr.add_argument('-o', dest='output',
#   #                     help='Where output xml goes to')
#
#   prsr.set_defaults(input_folder="input")
#   prsr.set_defaults(lang="en")
#   # prsr.set_defaults(output="out/test.xml")
#   results = prsr.parse_args()
#   main(results)
