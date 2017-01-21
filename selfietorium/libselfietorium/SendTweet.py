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

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, hashtag):
        self.verified = False
        self.latesttweet = None
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)
        if (self.api.verify_credentials()!=False):
            self.verified = True
            self.background_thread = Thread(target=self.startListening(hashtag))
            self.background_thread.start()

    @property
    def latest_Tweet(self):
        return self.latesttweet

    def on_status(self, data):
        self.latesttweet = data
        #print "STATUS RECIEVED : " + data.text +"\n"
        #for thing in dir(data):
        #    print ":" + thing + "\n"
    #def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        #decoded = json.loads(data)
     #   self.latesttweet = data
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        #print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))

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

    def startListening(self, hashtag):
        self.stream = tweepy.Stream(self.auth,self)
        if (hashtag):
            self.stream.filter(track=[hashtag])
        self.stream.userstream()


if __name__ == '__main__':
    import time
    c = selfie_Tweet('jEI4POVjkHU9IUzwdVRJjAfin','4e2hbGM4LwE8k8AxUmY9JUR5E3nazJUgxwOusycJXXL1PjvlCW','709132628339859456-fArUMiQGqurO5hRkqvBWPeHyOaeKXAU','R4L9WiAdcRhj848QBGLuGwtMCInos9n0axawPsInn0rSS','#selfietorium_test')
    print "Starting Polling the Twitter Layer..."
    #c.startListening();
    var = 1
    while var == 1 :  # This constructs an infinite loop
        if (c.latest_Tweet != None):
            print (time.strftime("%H:%M:%S") + c.latest_Tweet.text +"\n")
            if 'media' in c.latest_Tweet.entities:
                for image in  c.latest_Tweet.entities['media']:
                    print("Photo found @ : " + image['media_url'])
                    #(do smthing with image['media_url'])
            time.sleep(10)

    print "PROGRAM TERMINATED: "
    #res = c.search()
    #print res
    #dir(res)
    #print res
    #print "Screen Name : "+the_dict['user']['name']
    #print "Handle      : "+the_dict['user']['screen_name']
    #print "Avatar URL  : "+the_dict['user']['profile_image_url']
    #print "Tweet Text  : "+the_dict['text']
    #print the_dict['text']


