#!/usr/bin/env python

import RPi.GPIO as GPIO
import pygame
from pygame.locals import *

def keyPressed(inputkey):
    keysPressed = key.get_pressed()
    if keysPressed[inputkey]:
        return True
    else:
        return False



GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT) 
# 7 is the for LED1. You need to do this for each LED, or use lists, etc
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
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
        if GPIO.input(21):
            GPIO.output(7,1)
        else:
            GPIO.output(7,0)
        windowSurface.blit(img, (0, 0)) #Replace (0, 0) with desired coordinates
        pygame.display.flip()
pygame.quit()
