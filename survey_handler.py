#!/usr/bin/env python3
import csv
import json
from os import listdir
from os.path import isdir, join
from settings import log_response,debug_print,CATAGORIES_FILE,JAAAASON,LOCATION,FINALE,QUESTION,ANSWERS,ANSWER_NUM,ANSWER_VAL,SMRT_KEY,SMRT_KEY_TYPE,SMRT_VAL_KEY,SEPARATOR

class SurveyHandler:
  catagories = None
  json_data = None
  json_data_lang = None
  loc_data = None
  loc_data_lang = None
  input_fold = None

  def __init__(self, in_fold):
    self.input_fold = in_fold
    self.load_words()

  def get_json(self, lang):
    if self.json_data_lang is not None and self.json_data_lang == lang:
      return self.json_data
    else:
      data_file = open(join(join(self.input_fold, lang),JAAAASON),'r')
      self.json_data = json.load(data_file)
      self.json_data_lang = lang
      return self.json_data

  def get_places(self, lang):
    if self.loc_data_lang is not None and self.loc_data_lang == lang:
      return self.loc_data
    else:
      self.loc_data = {}
      f = open(join(join(self.input_fold, lang),LOCATIONS),'r')
      csv_f = csv.reader(f)
      for row in csv_f:
        for name in row[2:]:
          self.loc_data[name] = (row[0],row[1])
      return self.loc_data

  def load_words(self):
    self.catagories = {}
    onlyfolders = [f for f in listdir(self.input_fold) if isdir(join(self.input_fold, f))]
    debug_print("Language support for:")
    for lang_folder in onlyfolders:
      debug_print("   "+lang_folder)
      lang_catagories={}
      f = open(join(join(self.input_fold, lang_folder),CATAGORIES_FILE),'r')
      csv_f = csv.reader(f)
      for row in csv_f:
        lang_catagories[row[0]] = row[1:]
      self.catagories[lang_folder] = lang_catagories

  def getQuestionCatagories(self, matched_catagories, lang):
    matched_question_cats = []
    for catagory in matched_catagories:
      trimmed_catagory = catagory
      if catagory.endswith("."):
        trimmed_catagory = catagory[:-1]
      if trimmed_catagory in self.get_json(lang):
        matched_question_cats.append(trimmed_catagory)
    return matched_question_cats

  def mark_get_next_question(self, person, sms, time):
    if sms:
      if person.current_catagory == LOCATION:
        return self.mark_location_answer(person, sms, time)
      person.last_time_of_contact=time
      poss_reask = self.mark_answer(sms, person)
      if poss_reask:
        return poss_reask
      # next question
      person.current_question+=1
    next_q = self.next_q_from_catagory(person)
    return next_q

  def mark_gps_answer(self, person, lon, lat, time):
    person.xml.set_location(lon, lat)
    person.last_time_of_contact=time

  def mark_location_answer(self, person, sms, time):
    lon = None
    lat = None
    # IF GPS
    # FIND COORDS in message
    latlong = re.compile(r".*?(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?).*?")
    if latlong.match(sms):
      lon = latlong.sub(r"\1",sms))
      lat = latlong.sub(r"\3",sms))
    else:
      # ELSE LOOKUP LOCATIONS IN FILE FROM SMS, and get GPSs
      for key_name in get_places(person.lang):
        if key_name.lower() in sms.lower():
          (lon,lat) = self.loc_data[key_name]
    # if we found something, mark it 
    if lon:
      self.mark_gps_answer(person, lon, lat, time)
    person.current_question+=1
    next_q = self.next_q_from_catagory(person)
    return next_q


  def mark_answer(self, sms, person):
    reask_q = None
    current_q = self.get_json(person.lang)[person.current_catagory][person.current_question]
    poss_answers = current_q[ANSWERS]
    if len(poss_answers) == 0:
      person.xml.create_valued_node(current_q[SMRT_KEY],
                                  sms,
                                  current_q[SMRT_KEY_TYPE])
    else:
      try:
        self.mark_option_answer(sms, person, poss_answers,current_q)
      except ValueError as err:
        # loggit and reask the question
        log_response(person.phonenumber, sms)
        reask_q = current_q[QUESTION]
    return reask_q

  def mark_option_answer(self, sms, person, poss_answers,current_q):
    resp_val = int(sms)
    if resp_val < len(poss_answers):
      marked = False
      for answer in poss_answers:
        if resp_val == answer[ANSWER_NUM]:
          marked = True
          person.xml.create_valued_node(current_q[SMRT_KEY],
                                      answer[SMRT_VAL_KEY],
                                      current_q[SMRT_KEY_TYPE])
      # within bounds but not found
      if not marked:
          ValueError()
    else:
      ValueError()

  def next_q_from_catagory(self, person):
    question = None
    try:
      curr_q = self.get_json(person.lang)[person.current_catagory][person.current_question]
      question = curr_q[QUESTION]
      for answer in curr_q[ANSWERS]:
        question = question + SEPARATOR + str(answer[ANSWER_NUM])+ ") " +\
                  answer[ANSWER_VAL]
    except IndexError as err:
      try:
        # get the next catagory
        person.current_question = 0
        debug_print(person.catagories_matched)
        person.current_catagory = person.catagories_matched.pop()
        question = self.next_q_from_catagory(person)
        debug_print(person.catagories_matched)
      except IndexError as err:
        question = self.last_q(person)
    except KeyError as err:
      question = self.last_q(person)
    # return the question found
    return question

  def last_q(self, person):
    person.generateXML()
    return self.get_json(person.lang)[FINALE][0][QUESTION]
