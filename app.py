
from flask import Flask,redirect,url_for,render_template

app = Flask(__name__)


@app.route('/')
def home():
    import os
    import tweepy
    import configparser
    import pandas as pd
    import datetime


    # read configs
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']

    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']

    # authentication
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    class Listener(tweepy.Stream):
        tweets = []
        limit = 10
        def on_status(self, status):
            self.tweets.append(status)
            # print(status.user.screen_name + ": " + status.text)

            if len(self.tweets) == self.limit:
                self.disconnect()



    stream_tweets = Listener(api_key,api_key_secret,access_token,access_token_secret)

    keywords = ['leni, bbm, ping, kiko'],
    ['-hahahaha, -haha, -lenlen, -filter:retweets']
    languange = ['''tl''']

    
    stream_tweets.filter(track=keywords,languages=languange)

    #Data Fram

    foulwords = [keywords]
    data = []
    username = []
    date = []
    link = []
    for tweet in stream_tweets.tweets:
        if not tweet.truncated:
            data.append([tweet.text])
            username.append([tweet.user.screen_name])
            date.append([tweet.created_at])
            link.append([tweet.id])
            foulwords.append
        else:
            data.append([tweet.extended_tweet['full_text']])
            username.append([tweet.user.screen_name])
            date.append([tweet.created_at])
            link.append([tweet.id])
            foulwords.append
        

    return render_template("index.html", users=username,tweet=data,date=date,link=link,foulwords=foulwords)
    
    

if __name__ == "__main__":
    app.run()