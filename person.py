
class Person:
  phonenumber = None
  catagories_matched = []
  current_catagory = None
  current_question = None
  last_time_of_contact = None
  xml = None

  def __init__(self, phonenumber, catagories_matched, current_catagory,
              date_time, xml):
    self.catagories_matched = catagories_matched
    if len(catagories_matched) >= 1 :
      self.current_catagory = current_catagory[0]
    self.current_question = 0
    self.last_time_of_contact = date_time
    self.xml = xml

  def getNextQuestion():



  def generateXML():
    if xml:
      # WRITE A LOG
      print("xml lol")
    else:
      raise Exception('No XML')
