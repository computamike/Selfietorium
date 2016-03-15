#!/usr/bin/python
from gpiozero import LED,Button
from time import sleep

def Red():
    print "red"








RedButton = Button(21)
GreenButton  = Button(19)
BlueButton = Button(26)
YellowButton = Button(24)

RedButton.when_pressed = Red

while True:
    pass
