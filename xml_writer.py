import os.path
from xml.dom.minidom import Document
from xml.sax.saxutils import unescape
WYPNT_ATTR = {
  'xmlns':"http://www.smartconservationsoftware.org/xml/1.0/independentincident",
  'id':"1"
}
FILE_TYPE = ".xml"

class IncidentXMLWriter:
  way_node = None

  def __init__(self, sms, bool_arr_to_true, date_time):
    self.doc = Document()
    # CREATE WAYPOINT
    extra_deets = {
      'x':'0',
      'y':'0',
      'dateTime':date_time
    }
    way_p_full_attr = dict(WYPNT_ATTR)
    way_p_full_attr.update(extra_deets)
    self.way_node = self.create_node("Waypoint",
                          attribs = way_p_full_attr)
    # CREATE COMMENTS
    comment_node = self.create_node("comment", self.way_node)
    trueVal = self.doc.createTextNode("AUTO-GENERATED FROM SMS:\"" + sms +"\"")
    comment_node.appendChild(trueVal)

    # FIGURE OUT ARRAY INPUTTED
    for item in bool_arr_to_true:
      self.create_valued_node(item+"isactive",
                      "true",
                      "bValue")

  def create_node(self, node_name, parent_node = '', attribs = {}):
    node = self.doc.createElement(node_name)
    if parent_node == '':
      createdNode = self.doc.appendChild(node)
    else:
      createdNode = parent_node.appendChild(node)

    if attribs != {}:
      for key, value in attribs.items():
        self.set_attribute(createdNode, key, value)

    return createdNode

  def create_valued_node(self, node_name, node_value, value_type):
    # get the final thing as the attributeKey
    # eg.ge.example => "eg.ge." and "example"
    splitUp = node_name.rsplit('.',1)
    attributeKey = splitUp[1]
    categoryKey = splitUp[0]

    observation = self.create_node("observations", self.way_node,
                          attribs={"categoryKey":categoryKey})
    active = self.create_node("attributes",observation,
                            attribs = {'attributeKey':attributeKey})
    typeVal = self.create_node(value_type, active)
    trueVal = self.doc.createTextNode(node_value)
    typeVal.appendChild(trueVal)
    return observation

  def set_location(self, x_loc, y_loc):
    self.way_node.setAttribute("x", x_loc)
    self.way_node.setAttribute("y", y_loc)

  def set_attribute(self, node, key, value):
    node.setAttribute(key, value)

  def print_XML(self):
    print (self.doc.toprettyxml(indent="  "))

  def write_XML(self, out_file):
    file_name = out_file + FILE_TYPE
    i = 1
    while(os.path.isfile(file_name)):
      file_name = out_file + "-" + str(i) + FILE_TYPE
      i+=1
    f = open(file_name, 'w')
    f.write(self.doc.toprettyxml(indent="  "))
