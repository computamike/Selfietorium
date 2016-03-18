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


WIDTH = 640
HEIGHT = 480

def bgra_rgba(surface):
        img = PIL.Image.frombuffer('RGBA',(surface.get_width(),surface.get_height()),surface.get_data(),'raw','RGBA',0,1)
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
def AttractScreen():
    IMG = load_svg("../Attract.svg")
    screen.blit(background,(0,0))
    screen.blit(IMG,(0,0))
    pygame.display.flip()


def PicamGetPhoto(cam):
#    picamImage = pygame.image.load("../Photo1.bmp")
#    picamImage = pygame.transform.scale(picamImage,(width,height))
#    return picamImage
    img = cam.get_image()
    return img
    #import pygame.image
    #pygame.image.save(img, "photo.bmp")
    #pygame.camera.quit()




def PreenScreen(photoshoot):
    svg_data = open('../Instructions2.svg').read()
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

    #promptFontsize = promptfont.attrib['font-size']

    print promptfont

    promptx = int(math.floor(float(prompt.attrib['x'])*scaleWidth))
    prompty = int(math.floor(float(prompt.attrib['y'])*scaleHeight))
    promptWidth = int(math.ceil(float(prompt.attrib['width'])*scaleWidth))
    promptHeight =int(math.ceil(float(prompt.attrib['height'])*scaleHeight))
    promptBackground = prompt.attrib['style']

    print promptBackground

    for shot in photoshoot:
        photo = PicamGetPhoto(cam)
        my_font = pygame.font.SysFont("My Underwood", 30)

        my_string = str(shot.title)
        my_rect = pygame.Rect((promptx, prompty ,promptWidth, promptHeight))
        prompt = pygameTextRectangle.render_textrect(my_string, my_font, my_rect, (0, 0, 128), (0, 0, 0,0), 1)


        start = datetime.datetime.now()
        end = datetime.datetime.now()
        Preentime = 5
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

            screen.blit(prompt,(promptx,prompty))
            pygame.display.flip()
            pygame.time.delay(25)# this needs to be more realistic - this would only update after .5 seconds.  Instead we need a routine that refreshes the screen and works out how long has elapsed.
        sounda.play()
        pygame.time.delay(500)
        screen.blit(background,(0,0))
        screen.blit(pygame.transform.scale(photo,(WIDTH,HEIGHT)),(0,0))
        pygame.display.flip()
        pygame.time.delay(2000)

    return "ATTRACT"

def debugPrintConfiguration(config,photoshoot):
    """Prints configuration to console."""
    print "Starting selfietorium..."
    print "------------------------"
    print
    print "Configuration :"
    print
    print " Template :" + config.layout
    print
    print
    for shoot in photoshoot:
            print shoot

if __name__ == '__main__':
    config = configuration.ConfigFile("boothsettings.json")
    config.Load()
    photoshoot = template.LoadPhotoShoot(config.layout)
    debugPrintConfiguration(config,photoshoot)


    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    cam.start()



    state = "ATTRACT"
    pygame.init()
    pygame.mixer.init(48000,-16,1,1024)
    sounda = pygame.mixer.Sound("62491__benboncan__dslr-click.wav")
    print pygame.display.list_modes(16,pygame.FULLSCREEN)
    pygame.display.set_mode((WIDTH,HEIGHT),0,16)
    #print 	BestMode
    #\WIDTH = BestMode[0]
    #HEIGHT = BestMode[1]
    background = pygame.Surface((WIDTH,HEIGHT))
    background = background.convert()
    background.fill((0,0,0))
    screen = pygame.display.set_mode((WIDTH,HEIGHT),0,16)
    c=pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                 if event.key == pygame.K_p:
                     print "RUN PRINT"
                     if state == "ATTRACT":
                         state = "PREEN"

            if state == "ATTRACT":
              AttractScreen()
            if state == "PREEN":
              state = PreenScreen(photoshoot)
    # c.tick(1)
