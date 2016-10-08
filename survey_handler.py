#!/usr/bin/env python3
import csv
import json

NONMATCH_RESP="out/log.csv"
BEGIN="start"
FINALE="end"
QUESTION="question"
ANSWERS="answers"
ANSWER_NUM="answer_number"
SMRT_KEY="smart_key"
SMRT_KEY_TYPE="smart_key_type"
SMRT_VAL_KEY="smart_value_key"

class SurveyHandler:
  catagories = None
  json_data = None

  def __init__(self, words_loc, json_data):
    self.load_words(words_loc)
    self.json_data = json_data

  def load_words(self, loc):
    print(loc)
    self.catagories={}
    f = open(loc,'r')
    csv_f = csv.reader(f)
    for row in csv_f:
      self.catagories[row[0]] = row[1:]

  def getQuestionCatagories(self, matched_catagories):
    matched_question_cats = []
    for catagory in matched_catagories:
      trimmed_catagory = catagory
      if catagory.endswith("."):
        trimmed_catagory = catagory[:-1]
      if trimmed_catagory in self.json_data:
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
    current_q = self.json_data[person.current_catagory][person.current_question]
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
    try:
      question = self.json_data[catagory][person.current_question][QUESTION]
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
    return self.json_data[FINALE][0][QUESTION]

def log_response(number, sms):
  with open(NONMATCH_RESP, "a") as responses_file:
    responses_file.write("{0}, {1}".format(number, sms))
