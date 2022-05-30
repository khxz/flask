import os
from unicodedata import name
from warnings import catch_warnings
from numpy import datetime_data

import tweepy
import configparser
import pandas as pd
import datetime
import csv
from flask import Flask,redirect,url_for,render_template,request,session,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from csv import writer
from datetime import datetime


app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'users.sqlite3.db')
#Setting up DATABASE
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    user_password = db.Column(db.String(100))

    def __init__(self,user_password):
        self.user_password = user_password



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


@app.route('/', methods=["POST","GET"])
def index():
    return render_template('samp.html')

texxt = ""
@app.route('/newTweet', methods=["POST","GET"])
def home():
    class Listener(tweepy.Stream):
        tweets = []
        
        def on_status(self, status):
            self.tweets.append(status)
            texxt = status.text
            print(status.user.screen_name + ": " + status.text)
            
            self.disconnect()
        def on_error(self, status_code):
            if status_code == 420:
                self.disconnect()
                return False

    
    stream_tweets = Listener(api_key,api_key_secret,access_token,access_token_secret)
    
    

    keywords = [ 
        {'bobo, tanga, kupal, gago, tangina, pota, leche, ampota, fuck, stupid, bitch, btch'}
        ,         {'-hahahaha, -haha, -emoji, -RT'}
        ]
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
            date.append([tweet.created_at])
            link.append([tweet.id])
            foulwords.append
        else:
            data.append([tweet.extended_tweet['full_text']])
            username.append([tweet.user.screen_name])
            date.append([tweet.created_at])
            link.append([tweet.id])
            foulwords.append

    
    return jsonify('',render_template("model.html",users=username,tweet=data,date=date,link=link))
    
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)