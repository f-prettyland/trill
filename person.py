FILE_LOC = "out/"

class Person:
  phonenumber = None
  catagories_matched = []
  current_catagory = None
  current_question = None
  last_time_of_contact = None
  xml = None
  finished = False

  def __init__(self, phonenumber, catagories_matched,
              date_time, xml):
    self.phonenumber = phonenumber
    self.catagories_matched = catagories_matched
    if len(catagories_matched) >= 1 :
      self.current_catagory = catagories_matched.pop()
    self.current_question = 0
    self.last_time_of_contact = date_time
    self.xml = xml

  def generateXML(self):
    finished = True
    if self.xml:
      # TODO WRITE A LOG
      self.xml.write_XML(FILE_LOC+self.phonenumber)
    else:
      raise Exception('No XML')
