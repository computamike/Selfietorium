#!/usr/bin/env python
import sys
import RPi.GPIO as GPIO
import pygame
import time
from pygame.locals import *



GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT) 
GPIO.setup(15, GPIO.OUT) 
GPIO.setup(12, GPIO.OUT) 
GPIO.setup(18, GPIO.OUT) 


# 7 is the for LED1. You need to do this for each LED, or use lists, etc
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# 21 is the for the Red button. You need to do this for each button, or use lists, etc


pygame.init()
infoObject = pygame.display.Info()


WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN ,32)

img=pygame.image.load("Instructions1.png").convert_alpha()
img = pygame.transform.scale(img,(WIDTH,HEIGHT))




running = True

while running:
    events = pygame.event.get()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            if event.key == K_ESCAPE :
                running = False

    if GPIO.input(24):
        GPIO.output(15,1)
        #pygame.quit()
        #sys.exit()
    else:
        GPIO.output(15,0)
    

    if GPIO.input(26):
        GPIO.output(18,1)
        #pygame.quit()
        #sys.exit()
    else:
        GPIO.output(18,0)


    if GPIO.input(19):
        GPIO.output(12,1)
        #pygame.quit()
        #sys.exit()
    else:
        GPIO.output(12,0)




    if GPIO.input(21):
        GPIO.output(7,1)
    else:
        GPIO.output(7,0)
    windowSurface.blit(img, (0, 0)) #Replace (0, 0) with desired coordinates
    pygame.display.flip()
pygame.quit()
