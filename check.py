#!/usr/bin/env python3
import re
import os
import json
import string
import argparse
from datetime import datetime
from xml_writer import IncidentXMLWriter
from survey_handler import SurveyHandler
from person import Person

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
CATAGORIES="catagories.csv"
JAAAASON="temp.json"
ASK_FOR_IN="Gimme a SMS\n"
svr_handler = None

def check_for(checkee, words):
  regex = re.compile('|'.join(r'(?:|^)'+re.escape(x)+r'(?:|$)'
                      for x in words))
  return re.search( regex, checkee)

def get_initial_text_catagories(to_parse):
  id_catagories = []
  for catagory in svr_handler.catagories.keys():
    if check_for(to_parse, svr_handler.catagories[catagory]):
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

def main(results):
  global svr_handler
  input_loc = os.path.join(__location__,results.input_folder + "/" + \
                          results.lang + "/"+CATAGORIES)
  input_json_loc = os.path.join(__location__,results.input_folder + "/" + \
                          results.lang + "/"+JAAAASON)

  data_file = open(input_json_loc)
  json_data = json.load(data_file)
  svr_handler = SurveyHandler(input_loc, json_data)

  to_parse = ""
  if results.input:
    to_parse = results.input
  else:
    to_parse = input(ASK_FOR_IN)

  p = make_person(to_parse,"0909090909")
  p.generateXML()

if __name__ == "__main__":
  prsr = argparse.ArgumentParser(description='Identify what someone\'s chatting about')

  prsr.add_argument('-d', dest='input_folder',
                      help='File locaiton of word dictionaries')
  prsr.add_argument('-l', dest='lang',
                      help='Two letter language representation')
  prsr.add_argument('-i', dest='input',
                      help='A string to parse')
  # prsr.add_argument('-o', dest='output',
  #                     help='Where output xml goes to')

  prsr.set_defaults(input_folder="input")
  prsr.set_defaults(lang="en")
  # prsr.set_defaults(output="out/test.xml")
  results = prsr.parse_args()
  main(results)
