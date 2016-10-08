from xml.dom.minidom import Document
from xml.sax.saxutils import unescape

class IncidentXMLWriter:
  def __init__(self, item_arr):
    self.doc = Document()
    way = self.createNode("Waypoint")
    for item in item_arr:
      cata = self.createNode(item, way)
      active = self.createNode("attributes",cata,withAttribs = {'attributeKey':"isactive"})
      bValue = self.createNode("bValue", active)

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
