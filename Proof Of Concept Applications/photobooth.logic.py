import time
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree

class PhotoPicture ():
    def __init__(self,a,b,c,d,e = None):
        self.With = a
        self.height = b
        self.x = c 
        self.y = d 
        self.image = e
        

def timeStamp ():
    seperator = "-"
    timedata = time.gmtime()
    return str(timedata.tm_year) + seperator + str(timedata.tm_mon) + str(timedata.tm_mday) + str(timedata.tm_hour)+ seperator + str(timedata.tm_min)


def takePhoto(index, folderName ,initsettings):
    print "CLR"
    print "5"
    time.sleep(1)
    print "5"
    time.sleep(1)
    print "4"
    time.sleep(1)
    print "3"
    time.sleep(1)
    print "2"
    time.sleep(1)
    print "1"
    time.sleep(1)
    print initsettings.PrePhotoPhrase
    time.sleep(1)
    print "TAKING PICTURE " , index + 1 
    print "picture saved as PICTURE",index + 1 ,"in location:", folderName
    

def PhotoLoop (initsettings):
    #this is a psuedo code loop to take X pictures
    #cleare the output wundow
    print "BUTTON Pressed"
    os.system("cls") or os.system("clear")    
    folderName = timeStamp()
    print "Folder created :" , folderName
    for i in range (0,initsettings.PhotoCount - 1):
        takePhoto( i, folderName,initsettings)
    print "photos Taken, arranging..."
    print "call a function to replace the references in layout SVG with the photos we just took and save to same location."
    time.sleep(2)
    print "show user photos"
    print "send final image to printer"
    print "if threading is working than second thread handles images, if not there might be a pause here..."
    time.sleep (5)
    initsettings.photosTaken += 1
    print "***DONE***"
    print initsettings.photosTaken,"/",initsettings.sheetspercartridge

def mainLoop (initsettings):
    while True:
        entered = raw_input("simulate different Button presses :\n P to take photos\n X to exit ")

        if not entered: 
            writeIni(initsettings)
            break
        
        if entered == "p":
            PhotoLoop(initsettings)
            
        if entered =="x":
            writeIni(initsettings)
            break


def setBoothSettings (obj,child_of_root):
    print"booth settings"
    obj.PrePhotoPhrase = child_of_root.attrib['PrePhotoPhrase']
    obj.sheetspercartridge = int(child_of_root.attrib['sheetspercartidge'])
    obj.photosTaken = int(child_of_root.attrib['photosTaken'])
    obj.LayoutUsed = child_of_root.attrib['Layout']


def ErrorSettings (obj,child_of_root):
    print"Error settings"


def GetPicturecount (obj):
    tree = ElementTree()
    tree.parse(obj.LayoutUsed)     
    picCount = 0                    
    for node in tree.iter():
        if node.tag.split("}")[1] == 'image':
            picCount +=1
    obj.PhotoCount = picCount


case = {
      'PhotoSettings': setBoothSettings,
      'ErrorMessages': ErrorSettings,
      }
def writeIni (obj):
    root = etree.Element("Boothsettings")
    elemtn1 = etree.SubElement(root, "PhotoSettings")
    elemtn1.attrib['sheetspercartidge']= str(obj.sheetspercartridge)
    elemtn1.attrib['photosTaken']=str(obj.photosTaken)
    elemtn1.attrib['PrePhotoPhrase']= obj.PrePhotoPhrase
    elemtn1.attrib['Layout']= obj.LayoutUsed
    elemtn2 = etree.SubElement(root, "ErrorMessages", NoWifi="ERROR1", NoPaper="ERROR2" ,General="ERRO3")
    elemtn2.attrib['NoWifi']= str(obj.error1)
    elemtn2.attrib['NoPaper']= str(obj.error2)
    elemtn2.attrib['General']= str(obj.error3)
    tree = etree.ElementTree(root)
    tree.write(inifile)


class initVals ():
    def __init__ (self):
        self.PrePhotoPhrase = None
        self.sheetspercartridge = None
        self.photosTaken = None
        self.LayoutUsed = None
        self.error1 = None
        self.error2 = None
        self.error3 = None
        self.PhotoCount = 0
        

initsettings = initVals()
inifile = "boothsettings.xml"
tree = etree.ElementTree(file=inifile)
root = tree.getroot()
#set all the global settings
for child_of_root in root:
    print "CHECKING",child_of_root.tag
    case[child_of_root.tag](initsettings,child_of_root)
GetPicturecount(initsettings)

#Fire up toe booth
mainLoop(initsettings)


