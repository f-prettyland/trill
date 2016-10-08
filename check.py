#!/usr/bin/env python3
import re
import os
import csv
import string
import argparse
from xml_writer import IncidentXMLWriter

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
CATAGORIES="catagories.csv"
ASK_FOR_IN="Gimme a SMS\n"

def check_for(checkee, words):
  regex = re.compile('|'.join(r'(?:|^)'+re.escape(x)+r'(?:|$)'
                      for x in words))
  return re.search( regex, checkee)

def loadWords(loc):
  catagories = {}
  f = open(os.path.join(__location__,loc),'r')
  csv_f = csv.reader(f)
  r_count = 0
  for row in csv_f:
    catagories[row[0]] = row[1:]
    r_count+=1

  return catagories

def identify_str(to_parse, catagories):
  id_catagories = []
  for catagory in catagories.keys():
    if check_for(to_parse, catagories[catagory]):
      id_catagories.append(catagory)
  return id_catagories

def main(results):
  input_loc = os.path.join(__location__,results.input_folder + "/" + \
                          results.lang + "/"+CATAGORIES)
  output_loc = os.path.join(__location__,results.output)

  catagories = loadWords(input_loc)
  for catagory in catagories.keys():
    print(catagory)
    print("     ", catagories[catagory])

  to_parse = ""
  if results.input:
    to_parse = results.input
  else:
    to_parse = input(ASK_FOR_IN)

  print("\nidentifying ", to_parse)
  print("\nGot these:")
  id_catagories = identify_str(to_parse, catagories)
  print(id_catagories)

  incident = IncidentXMLWriter(to_parse,
                              id_catagories,
                              "45.34",
                              "34.56",
                              "2016-10-07T20:47:56.000-04:00")
  incident.printXML()
  incident.writeXML(output_loc)

if __name__ == "__main__":
  prsr = argparse.ArgumentParser(description='Identify what someone\'s chatting about')

  prsr.add_argument('-d', dest='input_folder',
                      help='File locaiton of word dictionaries')
  prsr.add_argument('-l', dest='lang',
                      help='Two letter language representation')
  prsr.add_argument('-i', dest='input',
                      help='A string to parse')
  prsr.add_argument('-o', dest='output',
                      help='Where output xml goes to')

  prsr.set_defaults(input_folder="input")
  prsr.set_defaults(lang="en")
  prsr.set_defaults(output="out/test.xml")
  results = prsr.parse_args()
  main(results)