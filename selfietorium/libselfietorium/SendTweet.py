#!/usr/bin/python
import twitter


class selfie_Tweet:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.verified = False
        self.api = twitter.Api(
            consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token,
        access_token_secret=access_token_secret)
        self.twitteruser = self.api.VerifyCredentials()
        self.verified = (self.twitteruser is not None)

    def tweet(self, status):
        if (self.verified):
            self.api.PostUpdate(status)
        else:
            print "posting to twitter " + status


    def tweetPhoto(self, status, media):
        self.api.PostMedia(status,media)

# This is how you post a simple status update - like..Selfietorium booting up..
#api.PostUpdate('This is an eagle.')
#api.PostMedia('This is an Eagle','../Photo1.jpg')
