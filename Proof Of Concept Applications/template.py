#!/usr/bin/env python

# Reading a SVG template file to retrieve all of the required photos.
# When loading a template, we can use the TITLE of a photo to store a "Smile" or some other form of instruction.
# The Title will also have to store the Order of the photo so that we can take photos
# in a specific order
#
# This code takes an SVG, and from that generates a Shot List.  
#
# A shot list consists of the :
#  Image ID associated with the Photo
#  The Order that the photo should be taken
#  The instruction to the subjects
#
# EG:
# +----------------------------------------------------------+---------+
# | Shooting instruction                                     |ImageID  |
# +----------------------------------------------------------+---------+
# | Ok.  Big smiles everyone                                 |image3085|
# | That looked amazing.Ok - now everyone wave at the camera.|image3087|
# | Wow - and you guys aren't professional Models?  Smile!   |image3045|
# | Great... last one now..  Got nuts everyone!              |image3085|
# +----------------------------------------------------------+---------+
#
# this allows the photo program the ability to prompt the subjects appropriately, and makes updating the template easier (straight XPath update)
#
# Note : order is determined from the Image ID.  Creating an image in Inkscape will increment the image.  Therefore if you create your images in the order that you want them to be taken, then the photo ordering should work fine.  
#  the Shoot list is ordered by the ImageID - meaning that you can write your own ID's for photos if you want - however the order of these ID's will determine the shoot order

from lxml import etree as ET
from lxml.etree import QName

class PhotoShoot(object):
    pass
    def __str__(self):
        return '|' + self.imageID + '|' + self.title  +'|'
    

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

def updateNode(svg_data,id,value):
    tree = ET.fromstring(svg_data)
    NodeToUpdate = tree.xpath('/svg:svg/svg:g/svg:text[@id=\''+ id + '\']/svg:tspan',namespaces=ns)
    NodeToUpdate[0].text = value
    xmlstr = ET.tostring(tree)
    return xmlstr

def findNode(svg_data,xpath):
    tree = ET.fromstring(svg_data)
    NodeToUpdate = tree.xpath(xpath,namespaces=ns)
    if len(NodeToUpdate) >0:
        return NodeToUpdate[0]
    return None

def findGeometry(svg_data):
    tree = ET.fromstring(svg_data)
    return (tree.attrib["width"],tree.attrib["height"])



def PrintLists(list):
    for child in list: 
        print child  


def LoadPhotoShoot(templateFile):
    """
    Load a template file, and read the PhotoShoot information (shots and prompts in order)
    """
    tree = ET.parse(templateFile)
    root = tree.getroot()
    # First - lets set up some SVG namespaces
    p = tree.xpath('/svg:svg/svg:g/svg:image',namespaces=ns)
    simpleList = []
    for child in p:
        title = tree.xpath('/svg:svg/svg:g/svg:image[@id=\''+ child.attrib['id'] + '\']/svg:title',namespaces=ns)
        x = PhotoShoot()
        x.imageID = child.attrib['id']
        x.title = title[0].text or ""
        simpleList.append(x)
    return sorted(simpleList, key=lambda x: x.imageID, reverse=False)


#simpleList = LoadPhotoShoot('../6x4.Template1.-.Linked.Files.svg')

svg_data = open('../Instructions2.svg').read()
svg_data2 = findGeometry(svg_data)

#svg_data2 = findNode(svg_data,'//svg:rect[@id="picam"]')[0]
print svg_data2
#print svg_data2.attrib['height']
#print svg_data2.attrib['x']
#print svg_data2.attrib['y']

#print svg_data2
#for l in svg_data2 :
#    print ET.tostring(l)
#PrintLists(simpleList)
