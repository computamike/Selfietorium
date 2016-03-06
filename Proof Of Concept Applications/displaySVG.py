#!/usr/bin/python

import array
import math

import cairo
import pygame
import rsvg
import PIL.Image

WIDTH = 640
HEIGHT = 480

def load_svg(filename):
    def bgra_rgba(surface):
        img = PIL.Image.frombuffer('RGBA',(surface.get_width(),surface.get_height()),surface.get_data(),'raw','RGBA',0,1)
        return img.tostring('raw','RGBA',0,1)
    svg = rsvg.Handle(filename)

    img_w,img_h = svg.props.width,svg.props.height

    ScaleFactorx = float(WIDTH) / float(img_w)
    ScaleFactory = float(HEIGHT) / float(img_h)


    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,WIDTH,HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(ScaleFactorx,ScaleFactory)

    svg.render_cairo(ctx)
    return pygame.image.frombuffer(bgra_rgba(surface),(WIDTH,HEIGHT),'RGBA')
                                   







pygame.init()
pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.Surface((WIDTH,HEIGHT))
background = background.convert()
background.fill((0,0,0))


screen = pygame.display.set_mode((WIDTH,HEIGHT))
c=pygame.time.Clock()
while True:
    IMG = load_svg("../Attract.svg")
    screen.blit(background,(0,0))
    screen.blit(IMG,(0,0))
    pygame.display.flip()
    c.tick(1)

##data = array.array('c', chr(0) * WIDTH * HEIGHT * 4)
##surface = cairo.ImageSurface.create_for_data(
##    data, cairo.FORMAT_ARGB32, WIDTH, HEIGHT, WIDTH * 4)
##
##pygame.init()
##window = pygame.display.set_mode((WIDTH, HEIGHT))
##svg = rsvg.Handle(file="../Attract.svg")
##ctx = cairo.Context(surface)
##svg.render_cairo(ctx)
##
##screen = pygame.display.get_surface()
##image = pygame.image.frombuffer(data.tostring(), (WIDTH, HEIGHT),"ARGB")
##screen.blit(image, (0, 0)) 
##pygame.display.flip() 
##
##clock = pygame.time.Clock()
##while True:
##    clock.tick(15)
##    for event in pygame.event.get():
##        if event.type == pygame.QUIT:
##            raise SystemExit
