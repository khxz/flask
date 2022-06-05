import os
import sqlite3
from unicodedata import name
from warnings import catch_warnings
from numpy import datetime_data
import pytz
import tweepy
import pandas as pd
import pytz
import datetime
from textblob import TextBlob
import re





class Listener(tweepy.Stream):
    tweets = []
    
    def on_status(self, status):
        self.tweets.append(status)
        analysis = TextBlob(status.text)
        if analysis.polarity < 0:
            analysis 
            print(status.id)
            self.tweets.append(analysis)
            print(analysis)
            
            


api_key = 'gUHn0tg6rroVfRpddz0Dt9r3w'
api_key_secret = 'HQJKsuP7fs27VIvPMLV6r10XED45TCShpwCiWfJ1wslfoUVIu4'

access_token = '703740762710609920-WlBlY29OUSplpiRQlo86hvgBMMX22Rc'

access_token_secret = 'x9oiMT7LGGG1uYEnBLc6qXuYOJnT7FC3jTIuljrGoRPOK'



    # authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

stream_tweets = Listener(api_key,api_key_secret,access_token,access_token_secret)


keywords = ['bobo','gago','ulol','putang ina','puta','tanga','siraulo','putangina','putangina ka']


language = ['''tl''']



stream_tweets.filter(track=keywords, languages=language)
foulwords = [keywords]
data = []
username = []
date = []
link = []
for tweet in stream_tweets.tweets:
    if not tweet.truncated:
        data.append([tweet.text])
        username.append([tweet.user.screen_name])
        date.append([tweet.created_at.astimezone(pytz.timezone('Asia/Manila')).replace(tzinfo=None,microsecond=0)])
        link.append([tweet.id])
        foulwords.append
    else:
        data.append([tweet.extended_tweet['full_text']])
        username.append([tweet.user.screen_name])
        date.append([tweet.created_at.astimezone(pytz.timezone('Asia/Manila')).replace(tzinfo=None,microsecond=0)])
        link.append([tweet.id])
        foulwords.append


        