from xml.dom.minidom import Document
from xml.sax.saxutils import unescape
WYPNT_ATTR = {
  'xmlns':"http://www.smartconservationsoftware.org/xml/1.0/independentincident",
  'id':"1"
}

class IncidentXMLWriter:
  def __init__(self, sms, item_arr, in_x, in_y, date_time):
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
                          withAttribs = way_p_full_attr)
    # CREATE COMMENTS
    comment_node = self.createNode("comment", way_node)
    true_val = self.doc.createTextNode("AUTO-GENERATED FROM SMS:\"" + sms +"\"")
    comment_node.appendChild(true_val)

    # FIGURE OUT ARRAY INPUTTED
    for item in item_arr:
      cata = self.createNode("observations", way_node,
                            withAttribs={"categoryKey":item})
      active = self.createNode("attributes",cata,
                              withAttribs = {'attributeKey':"isactive"})
      bValue = self.createNode("bValue", active)
      true_val = self.doc.createTextNode("true")
      bValue.appendChild(true_val)

  def createNode(self, nodeName, parentNode = '', withAttribs = {}):
    node = self.doc.createElement(nodeName)
    if parentNode == '':
      createdNode = self.doc.appendChild(node)
    else:
      createdNode = parentNode.appendChild(node)

    if withAttribs != {}:
      for key, value in withAttribs.items():
        self.setAttribute(createdNode, key, value)

    return createdNode

  def setAttribute(self, node, key, value):
    node.setAttribute(key, value)

  def printXML(self):
    print (self.doc.toprettyxml(indent="  "))

  def writeXML(self, out_file):
    f = open(out_file, 'w')
    f.write(self.doc.toprettyxml(indent="  "))
