#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy


class selfie_Tweet(tweepy.StreamListener):

    def __init__(
        self,
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
        hashtag,
        author
        ):
        self.IsTest = True
        self.verified = False
        self.latesttweet = None
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)
        self.author = author.lstrip('@')
        self.hashtag = hashtag.lstrip('#')
        if self.IsTest is False and self.api.verify_credentials() is not False:
            self.verified = True
            self.stream = tweepy.Stream(auth=self.auth, listener=self)
            self.stream.userstream(async=True)
        if self.IsTest is True:
            self.verified = True

    @property
    def Fake_Tweet(self):
        faketweet = tweepy.models.Status()
        faketweet.text = "This is a fake tweet"
        faketweet.user = tweepy.models.User()
        faketweet.user.screen_name = "selfietorium"
        faketweet.entities=        {
            'hashtags': [{u'indices': [18, 36], u'text': u'selfietorium_test'}],
            'urls': [],
            'media'   :[
                {'type':'photo', 'media_url':'https://pbs.twimg.com/media/C1RspMjXEAAQwKJ.png'},
                {'type':'photo', 'media_url':'https://pbs.twimg.com/media/C2zEuKpWEAAj5Pg.jpg'},
                {'type':'photo', 'media_url':'https://pbs.twimg.com/media/C2tpKy7XcAMlcco.jpg'}]
         }

        faketweet.user.name = "selfietorium"
        faketweet.user.profile_image_url ='https://pbs.twimg.com/profile_images/709148441981616128/X4ZMu4ax_bigger.jpg'
        return faketweet

    @property
    def latest_Tweet(self):
        if self.IsTest :
            return self.Fake_Tweet
        return self.latesttweet

    def tweet(self, status):
        if self.verified:
            self.api.PostUpdate(status)
        else:
            print 'posting to twitter ' + status

    def tweetPhoto(self, status, media):
        self.api.PostMedia(status, media)


    def on_status(self, data):
        print data
        if (data.user.name == self.author):
            for x in data.entities.get('hashtags'):
                if x["text"] == self.hashtag:
                    self.latesttweet = data
                    break

    def on_error(self, status):
        print status


if __name__ == '__main__':
    pass