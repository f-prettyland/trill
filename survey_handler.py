#!/usr/bin/env python3
import csv
import json

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
