#!/usr/bin/env python3
import csv
import json
from os import listdir
from os.path import isdir, join

CATAGORIES_FILE="catagories.csv"
JAAAASON="temp.json"

NONMATCH_RESP="out/log.csv"
BEGIN="start"
FINALE="end"
QUESTION="question"
ANSWERS="answers"
ANSWER_NUM="answer_number"
ANSWER_VAL="answer_text"
SMRT_KEY="smart_key"
SMRT_KEY_TYPE="smart_key_type"
SMRT_VAL_KEY="smart_value_key"
SEPARATOR="  "

LANG="LANGUAGE NOT DETECTED"

class SurveyHandler:
  catagories = None
  json_data = None
  json_data_lang = None
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

  def load_words(self):
    self.catagories = {}
    onlyfolders = [f for f in listdir(self.input_fold) if isdir(join(self.input_fold, f))]
    for lang_folder in onlyfolders:
      print("FOLDER ",lang_folder)
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
      person.last_time_of_contact=time
      poss_reask = self.mark_answer(sms, person)
      if poss_reask:
        return poss_reask
      # next question
      person.current_question+=1
    next_q = self.next_q_from_catagory(person.current_catagory, person)
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

  def next_q_from_catagory(self, catagory, person):
    question = None
    if person.lang is None:
      person.finished = True
      return LANG
    try:
      curr_q = self.get_json(person.lang)[catagory][person.current_question]
      question = curr_q[QUESTION]
      for answer in curr_q[ANSWERS]:
        print(answer[ANSWER_VAL])
        question = question + SEPARATOR + str(answer[ANSWER_NUM])+ ") " +\
                  answer[ANSWER_VAL]
    except IndexError as err:
      try:
        # get the next catagory
        person.current_question = 0
        question = self.next_q_from_catagory(person.catagories_matched.pop(),
                            person)
      except IndexError as err:
        question = self.last_q(person)
    except KeyError as err:
      question = self.last_q(person)
    # return the question found
    return question

  def last_q(self, person):
    person.generateXML()
    return self.get_json(person.lang)[FINALE][0][QUESTION]

def log_response(number, sms):
  with open(NONMATCH_RESP, "a") as responses_file:
    responses_file.write("{0}, {1}".format(number, sms))
