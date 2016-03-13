#!/usr/bin/python
from lxml import etree as ET
from lxml.etree import QName
import array
import math
import cairo
import pygame
import pygame.display
import rsvg
import PIL.Image
import sys
import template
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
    

def PicamGetPhoto(width,height):
    picamImage = pygame.image.load("../Photo1.bmp")
    picamImage = pygame.transform.scale(picamImage,(width,height))
    return picamImage

def PreenScreen():
    svg_data = open('../Instructions2.svg').read()
    screenGeometry = template.findGeometry(svg_data)
    scaleWidth = float(float(WIDTH) / float(screenGeometry[0]))
    scaleHeight = float(float(HEIGHT) / float(screenGeometry[1]))
    picam = template.findNode(svg_data,'//svg:rect[@id="picam"]')
    pcamWidth = int(math.ceil(float(picam.attrib['width'])*scaleWidth))
    pcamHeight =int(math.ceil(float(picam.attrib['height'])*scaleHeight))
    picamx= int(math.floor(float(picam.attrib['x'])*scaleWidth))
    picamy= int(math.floor(float(picam.attrib['y'])*scaleHeight))
  
    photo = PicamGetPhoto(int(pcamWidth),int(pcamHeight))

    for i in range(5,0,-1):
        svg_data = template.updateNode(svg_data,'countDown',str(i))
        IMG = load_svg_string(svg_data)
        screen.blit(background,(0,0))
        
        screen.blit(IMG,(0,0))
        screen.blit(photo,(picamx,picamy))
        pygame.display.flip()

        pygame.time.delay(1000)
    sounda.play()
    return "ATTRACT"

    
state = "ATTRACT"

pygame.init()
pygame.mixer.init(48000,-16,1,1024)
sounda = pygame.mixer.Sound("62491__benboncan__dslr-click.wav")

pygame.display.set_mode((WIDTH,HEIGHT),0,16)
 

background = pygame.Surface((WIDTH,HEIGHT))
background = background.convert()
background.fill((0,0,0))


screen = pygame.display.set_mode((WIDTH,HEIGHT))
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
        state = PreenScreen()

    # c.tick(1)

