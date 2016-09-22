#!/usr/bin/python
from lxml import etree as ET
from lxml.etree import QName
import array
import math
import cairo
import pygame
import pygame.display
import pygame.camera
import rsvg
import PIL.Image
import sys
import template
import configuration
import pygameTextRectangle
import datetime
import base64
import StringIO
import os

# Constants
WIDTH = 640                     # Width of the window
HEIGHT = 480                    # Height of the window
SHOOTDIRECTORY = None           # Name of directory to store photographs taken
PHOTOSOUNDEFFECT = None         # Sound effect to play when taking photo
SCREEN_ATTRACT = None           # Attract Screen SVG XML data


def bgra_rgba(surface):
        img = PIL.Image.frombuffer('RGBA',(surface.get_width(),surface.get_height()),surface.get_data(),'raw','BGRA',0,1)
        return img.tostring('raw','RGBA',0,1)

def load_svg_string(svg_data):
    svg = rsvg.Handle(data=svg_data)
    img_w,img_h = svg.props.width,svg.props.height
    ScaleFactorx = float(WIDTH) / float(img_w)
    ScaleFactory = float(HEIGHT) / float(img_h)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,WIDTH,HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(ScaleFactorx,ScaleFactory)
    svg.render_cairo(ctx)
    return pygame.image.frombuffer(bgra_rgba(surface),(WIDTH,HEIGHT),'RGBA')

def load_svg(filename):
    """Render SVG as Pygame image"""
    svg = rsvg.Handle(filename)
    img_w,img_h = svg.props.width,svg.props.height
    ScaleFactorx = float(WIDTH) / float(img_w)
    ScaleFactory = float(HEIGHT) / float(img_h)


    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,WIDTH,HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(ScaleFactorx,ScaleFactory)

    svg.render_cairo(ctx)
    return pygame.image.frombuffer(bgra_rgba(surface),(WIDTH,HEIGHT),'RGBA')


# This is a poor state implementation - a better implementation will be
#worked out in due course
#Valid States are :
#
# ATTRACT
# PREEN
# PHOTO
# COMPOSITE
# PRINT
#



def PicamGetPhoto(cam):
#    picamImage = pygame.image.load("../Photo1.bmp")
#    picamImage = pygame.transform.scale(picamImage,(width,height))
#    return picamImage
    img = cam.get_image()
    return img
    #import pygame.image
    #pygame.image.save(img, "photo.bmp")
    #pygame.camera.quit()

def ConvertSurefaceToImage(surface):
    pil=pygame.image.tostring(surface,"RGBA",False)
    img = PIL.Image.fromstring("RGBA",(640,480),pil)
    return img


def SavePhoto(mydir,imgPhoto, filename):
    """Saves a photo as filename in the folder specified"""

    try:
        os.makedirs(mydir)
    except OSError, e:
        if e.errno != 17:
            raise # This was not a "directory exist" error..
    imgPhoto=ConvertSurefaceToImage(imgPhoto)
    imgPhoto.save(os.path.join(mydir, filename), format="PNG")




def layout(tplate,photos,outputDir):
    """Layout template and save to Directory"""
    updateNode = tplate
    for shot in photos:
        imgPhoto=ConvertSurefaceToImage(shot.photo)
        output = StringIO.StringIO()
        imgPhoto.save(output, format="PNG")
        contents = output.getvalue()
        output.close()
        photoB64 = pygame.image.tostring(shot.photo,"RGB")
        photoB64 = contents
        base64data = base64.b64encode(contents)
        strB64 = "data:image/png;base64,"+base64data
        updateNode = template.updateNodeAttrib(updateNode,shot.imageID,"{http://www.w3.org/1999/xlink}href",strB64)
    text_file = open(os.path.join(outputDir,"Output.svg"), "w")
    text_file.write(updateNode)
    text_file.close()
    SaveSVGToIMG(updateNode,outputDir,"Composite.png")


# Screen methods

def SaveSVGToIMG(svg,outputDir,Filename):
    IMG = load_svg_string(svg)
    screen.blit(cbackground,(0,0))
    screen.blit(IMG,(0,0))
    pygame.display.flip()
    pygame.time.delay(5000)
    SavePhoto(outputDir,IMG,Filename)

def PreenScreen(photoshoot,svg_data,Preentime=10):
    screenGeometry = template.findGeometry(svg_data)
    scaleWidth = float(float(WIDTH) / float(screenGeometry[0]))
    scaleHeight = float(float(HEIGHT) / float(screenGeometry[1]))
    picam = template.findNode(svg_data,'//svg:rect[@id="picam"]')
    pcamWidth = int(math.ceil(float(picam.attrib['width'])*scaleWidth))
    pcamHeight =int(math.ceil(float(picam.attrib['height'])*scaleHeight))
    picamx= int(math.floor(float(picam.attrib['x'])*scaleWidth))
    picamy= int(math.floor(float(picam.attrib['y'])*scaleHeight))

    prompt = template.findNode(svg_data,'//svg:rect[@id="prompt"]')
    svg_data=template.deleteNode(svg_data,'//svg:rect[@id="prompt"]')

    promptfont = template.findNode(svg_data,'//svg:text[@id="promptfont"]')
    svg_data=template.deleteNode(svg_data,'//svg:text[@id="promptfont"]')

    promptx = int(math.floor(float(prompt.attrib['x'])*scaleWidth))
    prompty = int(math.floor(float(prompt.attrib['y'])*scaleHeight))
    promptWidth = int(math.ceil(float(prompt.attrib['width'])*scaleWidth))
    promptHeight =int(math.ceil(float(prompt.attrib['height'])*scaleHeight))
    promptBackground = prompt.attrib['style']
    print "1"
    print photoshoot
    for shot in photoshoot:
        photo = PicamGetPhoto(cam)
        my_font = pygame.font.SysFont("My Underwood", 30)
        my_string = str(shot.title) or config.prePhotoPhrase
        my_rect = pygame.Rect((promptx, prompty ,promptWidth, promptHeight))
        prompt = pygameTextRectangle.render_textrect(my_string, my_font, my_rect, (0, 0, 128), (0, 0, 0,0), 1)
        start = datetime.datetime.now()
        end = datetime.datetime.now()

        preentimeSpent =(end-start).seconds
        while Preentime-preentimeSpent >0:
            photo = PicamGetPhoto(cam)
            end =  datetime.datetime.now()
            preentimeSpent =(end-start).seconds
            if Preentime-preentimeSpent ==0 :
                break
            svg_data = template.updateNode(svg_data,'countDown',str(Preentime-preentimeSpent))
            IMG = load_svg_string(svg_data)
            screen.blit(background,(0,0))
            screen.blit(IMG,(0,0))
            screen.blit(pygame.transform.scale(photo,(pcamWidth,pcamHeight)),(picamx,picamy))
            shot.image = photo
            screen.blit(prompt,(promptx,prompty))
            pygame.display.flip()
            pygame.time.delay(25)# this needs to be more realistic - this would only update after .5 seconds.  Instead we need a routine that refreshes the screen and works out how long has elapsed.
        sounda.play()
        shot.photo = photo
        print SHOOTDIRECTORY
        print photo
        print shot.imageID+".png"
        SavePhoto(SHOOTDIRECTORY,photo,shot.imageID+".png")
        pygame.time.delay(500)
        screen.blit(background,(0,0))
        screen.blit(pygame.transform.scale(photo,(WIDTH,HEIGHT)),(0,0))
        pygame.display.flip()
        pygame.time.delay(2000)

    # Cache this...
    print "here ok"
    tphotoshoot = svg_data = open(config.layout).read()
    print "cp2"
    layout(tphotoshoot,photoshoot,SHOOTDIRECTORY )

    return "ATTRACT"

def AttractScreen(AttractSVGdata):
    IMG = load_svg_string(AttractSVGdata)
    screen.blit(background,(0,0))
    screen.blit(IMG,(0,0))
    pygame.display.flip()

def debugPrintConfiguration(config,photoshoot):
    """Prints configuration to console."""
    print "Starting selfietorium..."
    print "------------------------"
    print
    print "Configuration :"
    print
    print "Template        : " + config.layout
    print "Pre-PhotoPhrase : " + config.prePhotoPhrase
    print "Preen Time      : " + str(config.preenTime) + " seconds."
    print "Shutter Sound   : " + config.shutterSound
    print "Photo store     : " + config.photostore
    print "Pre-PhotoPhrase : " + config.prePhotoPhrase
    print "Pre-PhotoPhrase : " + config.prePhotoPhrase
    print "Pre-PhotoPhrase : " + config.prePhotoPhrase
    print "Pre-PhotoPhrase : " + config.prePhotoPhrase

    print
    print
    # for shoot in photoshoot:
    #         print shoot

if __name__ == '__main__':
    #Set up configuration
    config = configuration.ConfigFile("boothsettings.json")
    config.Load()
    debugPrintConfiguration(config,None)
    #Set up variables
    SHOOTPHOTOSTORE = config.photostore
    SHOOTDIRECTORY = os.path.join(SHOOTPHOTOSTORE, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

    PHOTOSOUNDEFFECT = config.shutterSound
    photoshoot = template.LoadPhotoShoot(config.layout)
    debugPrintConfiguration(config,photoshoot)

    #Set Up Screens
    SCREEN_ATTRACT = open('../Attract.svg').read()
    SCREEN_PREEN =   open('../Instructions2.svg').read()

    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    cam.start()



    state = "ATTRACT"
    pygame.init()
    pygame.mixer.init(48000,-16,1,1024)
    sounda = pygame.mixer.Sound(PHOTOSOUNDEFFECT)
    print pygame.display.list_modes(16,pygame.FULLSCREEN)
    pygame.display.set_mode((WIDTH,HEIGHT),0,16)
    #print 	BestMode
    #\WIDTH = BestMode[0]
    #HEIGHT = BestMode[1]
    background = pygame.Surface((WIDTH,HEIGHT))
    background = background.convert()
    background.fill((0,0,0))

    cbackground = pygame.Surface((WIDTH,HEIGHT))
    cbackground = cbackground.convert()
    cbackground.fill((200,255,255))



    screen = pygame.display.set_mode((WIDTH,HEIGHT),0,16)
    c=pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                 if event.key == pygame.K_p:
                     if state == "ATTRACT":
                         state = "PREEN"

            if state == "ATTRACT":
              AttractScreen(SCREEN_ATTRACT)
            if state == "PREEN":
              state = PreenScreen(photoshoot,SCREEN_PREEN,config.preenTime)
    # c.tick(1)
