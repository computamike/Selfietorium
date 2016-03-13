#!/usr/bin/python
import cups
import pygame
import pygame.display

conn = cups.Connection()
printers = conn.getPrinters()

PrinterName = 'PDF'
##printer = [p for p in printers if p == 'PDF']
##print printer
for printerd in printers:
    print printerd

conn.printFile(PrinterName,'../Photo1.bmp','Hello',{})

##pygame.init()
##Width=640
##Height=480
##screen = pygame.display.set_mode((Width,Height))
##c = pygame.time.Clock()
##
##while True:
##    image = pygame.image.load('../Photo1.bmp')
##    image =  pygame.transform.scale(image,(Width,Height))
##    screen.blit(image,(0,0))
##    pygame.display.flip()
##    c.tick(3)
