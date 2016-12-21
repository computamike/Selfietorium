#!/usr/bin/env python
"""
A library that provides template functionality for selfietorium project

Tempaltes for selfietorium are stored as SVG graphic files.
This library provides functionality for reading and updating templates.
"""
from lxml import etree as ET
from lxml.etree import QName

class PhotoShoot(object):
    """Class that describes a photoshoot."""
    pass
    def __str__(self):
        return '|' + str(self.imageID) + '|' + str(self.title)  +'|' + str(self.photo)  +'|'


#
# CONSTANTS
#
ns = {
    'dc'    : 'http://purl.org/dc/elements/1.1/',
    'cc'    : 'http://creativecommons.org/ns#',
    'rdf'   : 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'svg'   : 'http://www.w3.org/2000/svg',
    'xlink' : 'http://www.w3.org/1999/xlink',
    'sodipodi':'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
    'inkscape' : 'http://www.inkscape.org/namespaces/inkscape'
    }
"""Namespaces used by SVG files (created by Inkscape)."""


def updateNode(svg_data,id,value):
    """
    Finds a Text Node based on ID, and sets its value.
    Args:
        svg_data : String containing template data
        id       : id of element to find
        value    : value to assign.
    returns :
        Updated SVG string data.
    """
    tree = ET.fromstring(svg_data)
    NodeToUpdate = tree.xpath('/svg:svg/svg:g/svg:text[@id=\''+ id + '\']/svg:tspan',namespaces=ns)
    NodeToUpdate[0].text = value
    xmlstr = ET.tostring(tree)
    return xmlstr

def updateNodeAttrib(svg_data,id,attrib,value):
    """
    Finds a Text Node based on ID, and sets its value.
    Args:
        svg_data : String containing template data
        id       : id of element to find
        value    : value to assign.
    returns :
        Updated SVG string data.
    """


    tree = ET.fromstring(svg_data)
    NodeToUpdate = tree.xpath('//*[@id=\''+id+'\']',namespaces=ns)
    #//*[@id='38']
    NodeToUpdate[0].set(attrib,value)

    #xmlstr = ET.tostring(tree)
    return ET.tostring(tree)


def findNode(svg_data,xpath):
    """
    Finds a node based on an Xpath.
    Args:
        svg_data : String containing template data
        xpath    : XPath of element to find
    Returns:
        XmlElement of required node, or None if node does not exist.
    """
    tree = ET.fromstring(svg_data)
    NodeToUpdate = tree.xpath(xpath,namespaces=ns)
    if len(NodeToUpdate) >0:
        return NodeToUpdate[0]
    return None

def deleteNode(svg_data,xpath):
    """
    Deletes a node based on an Xpath.
    Args:
        svg_data : String containing template data
        xpath    : XPath of element to find
    Returns:
        svg data cleansed of the offending node.
    """
    tree = ET.fromstring(svg_data)
    NodeToUpdate = tree.xpath(xpath,namespaces=ns)
    if len(NodeToUpdate) >0:
        NodeToUpdate[0].getparent().remove(NodeToUpdate[0])
    return  ET.tostring(tree)



def findGeometry(svg_data):
    """
    Determines the Geometry (size) of the template.
    Args:
        svg_data : String containing template data.
    """
    tree = ET.fromstring(svg_data)
    return (tree.attrib["width"],tree.attrib["height"])


def LoadPhotoShoot(templateFile):
    """
    Load a template file, and read the PhotoShoot shotlist.
    Notes:
        A shot list consists of the :
        * Image ID associated with the Photo
        * The prompt to the subjects
        * In the order the photos should be taken.
    EG:
    +----------------------------------------------------------+---------+
    | Shooting instruction                                     |ImageID  |
    +----------------------------------------------------------+---------+
    | Ok.  Big smiles everyone                                 |image3085|
    | That looked amazing.Ok - now everyone wave at the camera.|image3087|
    | Wow - and you guys aren't professional Models?  Smile!   |image3045|
    | Great... last one now..  Got nuts everyone!              |image3085|
    +----------------------------------------------------------+---------+

    This allows the photo program the ability to prompt the subjects
    appropriately, and makes updating the template easier (straight
    XPath update).  Shot order is determined from the Image ID.
    Creating an image in Inkscape will increment the image ID.
    Therefore if you create your images in the order that you want
    them to be taken, then the photo ordering should work fine.

    As the shoot list is ordered by the ImageID, these can be
    renamed - however the order of these ID's will determine the shoot
    order.
    """
    tree = ET.parse(templateFile)
    root = tree.getroot()
    # First - lets set up some SVG namespaces
    p = tree.xpath('/svg:svg/svg:g/svg:image',namespaces=ns)
    simpleList = []
    for child in p:
        Image = tree.xpath('/svg:svg/svg:g/svg:image[@id=\''+ child.attrib['id'] + '\']',namespaces=ns)
        title = tree.xpath('/svg:svg/svg:g/svg:image[@id=\''+ child.attrib['id'] + '\']/svg:title',namespaces=ns)
        x = PhotoShoot()
        x.imageID = child.attrib['id']
        print x.imageID
        print title
        print title == None
        print title == []
        x.title = ""
        if (title != [] ):
            x.title = title[0].text or ""
        x.photo=None
        simpleList.append(x)
    return sorted(simpleList, key=lambda x: x.imageID, reverse=False)

if __name__ == '__main__':
    # Add sample Code here
    pass
