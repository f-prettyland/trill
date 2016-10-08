from xml.dom.minidom import Document
from xml.sax.saxutils import unescape
WYPNT_ATTR = {
  'xmlns':"http://www.smartconservationsoftware.org/xml/1.0/independentincident",
  'id':"1"
}

class IncidentXMLWriter:
  def __init__(self, sms, bool_arr_to_true, in_x, in_y, date_time):
    self.doc = Document()
    # CREATE WAYPOINT
    extra_deets = {
      'x':in_x,
      'y':in_y,
      'dateTime':date_time
    }
    way_p_full_attr = dict(WYPNT_ATTR)
    way_p_full_attr.update(extra_deets)
    way_node = self.createNode("Waypoint",
                          attribs = way_p_full_attr)
    # CREATE COMMENTS
    comment_node = self.createNode("comment", way_node)
    true_val = self.doc.createTextNode("AUTO-GENERATED FROM SMS:\"" + sms +"\"")
    comment_node.appendChild(true_val)

    # FIGURE OUT ARRAY INPUTTED
    for item in bool_arr_to_true:
      cata = self.createNode("observations", way_node,
                            attribs={"categoryKey":item})
      active = self.createNode("attributes",cata,
                              attribs = {'attributeKey':"isactive"})
      bValue = self.createNode("bValue", active)
      true_val = self.doc.createTextNode("true")
      bValue.appendChild(true_val)

  def createNode(self, node_name, parent_node = '', attribs = {}):
    node = self.doc.createElement(node_name)
    if parent_node == '':
      createdNode = self.doc.appendChild(node)
    else:
      createdNode = parent_node.appendChild(node)

    if attribs != {}:
      for key, value in attribs.items():
        self.setAttribute(createdNode, key, value)

    return createdNode

  # def createValuedNode(self, node_name, nodeValue):
  #   node = self.doc.createElement(node_name)
  #   if parent_node == '':
  #     createdNode = self.doc.appendChild(node)
  #   else:
  #     createdNode = parent_node.appendChild(node)
  #
  #   if attribs != {}:
  #     for key, value in attribs.items():
  #       self.setAttribute(createdNode, key, value)
  #
  #   return createdNode

  def setAttribute(self, node, key, value):
    node.setAttribute(key, value)

  def printXML(self):
    print (self.doc.toprettyxml(indent="  "))

  def writeXML(self, out_file):
    f = open(out_file, 'w')
    f.write(self.doc.toprettyxml(indent="  "))
