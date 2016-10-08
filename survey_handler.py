#!/usr/bin/env python3
import csv
import json

FINALE="start"
FINALE="end"

class SurveyHandler:
  catagories = None
  json = None

  def __init__(self, words_loc, json):
    self.loadWords(words_loc)
    self.json = json

  def loadWords(self, loc):
    print(loc)
    self.catagories={}
    f = open(loc,'r')
    csv_f = csv.reader(f)
    for row in csv_f:
      self.catagories[row[0]] = row[1:]

  def mark_get_next_question(person):
    json_catagory_node = self.json[person.current_catagory]
    try:
      json_catagory_node[current_question]
    except IndexError err:
      try:
        next_cat = person.catagories_matched.pop()
      except IndexError err:
        return self.json[last_elem]
