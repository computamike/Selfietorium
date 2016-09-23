#!/usr/bin/python
import twitter
import pygame

api = twitter.Api(
    consumer_key='0KfOMrcL9j89rz9Mo1DJTuKNw',
    consumer_secret='rNoX4d7OE7FzcSh3i2x6JpNwzJDaqVkuqQW0ugug5C0XdXrrwQ',
    access_token_key='709132628339859456-ffOEOiTzIKgFglEHeqTCznr9j4ueP8G',
    access_token_secret='vI63eF1KkG29I8uJ4ZeFxkxzEOT29jVdRzFmHX7NRKXAD')

print api.VerifyCredentials()
file = open('../Photo1.jpg','rb')

# This is how you post a simple status update - like... Selfietorium booting up..
#api.PostUpdate('This is an eagle.')
#api.PostMedia('This is an Eagle','../Photo1.jpg')
