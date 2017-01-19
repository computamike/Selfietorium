#!/usr/bin/python
import tweepy
from threading import Thread

# Notes :
# 1. This class works well as an asynchronous class - however the stream only
# shows tweets that have been added while the stream was activated -
#
# What we need to do is in the constructor of this create a thread that will
# establish the stream connection and update the stored latest tweet object
#
# This means that the thing can be left running with its established connection
# to Twitter.  Every time you call the selfie_Tweet.Latest, the shared latest
# tweet object is returned
#
# The only issue could be in the event of a disconnection the inner class should
# attempt to reconnect.  It's not a massive issue - after all the latest tweet
# is stored in memory
#
#

class selfie_Tweet(tweepy.StreamListener):

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.verified = False
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)
        if (self.api.verify_credentials()!=False):
            self.verified = True

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        #decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print data
        #print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        return True
    def on_error(self, status):
        print status

    def tweet(self, status):
        if (self.verified):
            self.api.PostUpdate(status)
        else:
            print "posting to twitter " + status

    def search(self):
        #results = self.api.search(q="selfietorium", count=100)
        return self.api.home_timeline(screen_name = "selfietorium",count=1)

    def tweetPhoto(self, status, media):
        self.api.PostMedia(status,media)

    def startListening(self):
        self.stream = tweepy.Stream(self.auth,self)
        self.stream.userstream()


# This is how you post a simple status update - like..Selfietorium booting up..
#api.PostUpdate('This is an eagle.')
#api.PostMedia('This is an Eagle','../Photo1.jpg')
if __name__ == '__main__':
    # Add sample Code here
    c = selfie_Tweet('jEI4POVjkHU9IUzwdVRJjAfin','4e2hbGM4LwE8k8AxUmY9JUR5E3nazJUgxwOusycJXXL1PjvlCW','709132628339859456-fArUMiQGqurO5hRkqvBWPeHyOaeKXAU','R4L9WiAdcRhj848QBGLuGwtMCInos9n0axawPsInn0rSS')
    c.startListening();
    var = 1
    while var == 1 :  # This constructs an infinite loop

        num = raw_input("Enter a number  :")
    print "You entered: ", num
    #res = c.search()
    #print res
    #dir(res)
    #print res
    #print "Screen Name : "+the_dict['user']['name']
    #print "Handle      : "+the_dict['user']['screen_name']
    #print "Avatar URL  : "+the_dict['user']['profile_image_url']
    #print "Tweet Text  : "+the_dict['text']
    #print the_dict['text']


