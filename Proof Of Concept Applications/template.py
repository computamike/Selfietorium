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
# +------------+----------------------------------------------------------+---------+
# |Photo number| Shooting instruction                                     |ImageID  |
# +------------+----------------------------------------------------------+---------+
# | 1          | Ok.  Big smiles everyone                                 |image3085|
# | 2          | That looked amazing.Ok - now everyone wave at the camera.|image3087|
# | 3          | Wow - and you guys aren't professional Models?  Smile!   |image3045|
# | 4          | Great... last one now..  Got nuts everyone!              |image3085|
# +------------+----------------------------------------------------------+---------+
#
# this allows the photo program the ability to prompt the subjects appropriately, and makes updating the template easier (straight XPath update)

from lxml import etree as ET
from lxml.etree import QName

tree = ET.parse('../6x4.Template1.-.Linked.Files.svg')
root = tree.getroot()


# First - lets set up some SVG namespaces

ns = {
    'dc'    : 'http://purl.org/dc/elements/1.1/',
	'cc'    : 'http://creativecommons.org/ns#',
	'rdf'   : 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'svg'   : 'http://www.w3.org/2000/svg',
    'xlink' : 'http://www.w3.org/1999/xlink',
    'sodipodi':'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
    'inkscape' : 'http://www.inkscape.org/namespaces/inkscape'
    }

p = tree.xpath('/svg:svg/svg:g/svg:image',namespaces=ns)

for child in p:
    imageID = child.attrib['id']
    title = tree.xpath('/svg:svg/svg:g/svg:image[@id=\''+ imageID + '\']/svg:title',namespaces=ns)
    print "Image ID : = " + imageID
    if (len(title) > 0):
        print title[0].text
    print '----------'
    
 