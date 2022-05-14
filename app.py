import os
from unicodedata import name
from warnings import catch_warnings
import tweepy
import configparser
import pandas as pd
import datetime
import csv
from flask import Flask,redirect,url_for,render_template
from requests import request

app = Flask(__name__)




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
@app.route('/')
def home():



    class Listener(tweepy.Stream):
        tweets = []
        limit = 10
        def on_status(self, status):
            self.tweets.append(status)
            # print(status.user.screen_name + ": " + status.text)

            if len(self.tweets) == self.limit:
                self.disconnect()



    stream_tweets = Listener(api_key,api_key_secret,access_token,access_token_secret)

    

    keywords = [ 
        {'bobo, tanga, kupal, gago, tangina, pota, leche, ampota, fuck, stupid, bitch, btch'}
        #,         {'-hahahaha, -haha, -emoji, -RT'}
        ]
    language = ['''tl''']


    stream_tweets.filter(track=keywords, languages=language)

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
    
@app.route('/tweet', methods=["POST","GET"])
def tweet():
    from flask import Flask,redirect,url_for,render_template, request
    tweet = request.form["tweet"]
    api.update_status(tweet)
    return redirect(url_for("home"))
    
@app.route("/product/<user>/<name>")
def user(name,user):
    try:
        api.update_status("Sample Reply111", in_reply_to_status_id = name , auto_populate_reply_metadata=True)
        return render_template('warning.html',sucess="success") 

    except Exception as e :
        print(e)
        return render_template('warning.html',error=e, users = user,tweets=name)  
    
@app.route("/report/<username>/<name>")
def username(name,username):
    try:
        api.report_spam(screen_name = username, perform_block = False)
        return render_template('report_warning.html',sucess="success")  
    except Exception as e :
        print(e)
        return render_template('report_warning.html',error=e, users = username,tweets=name) 
    with open("datafile.csv", 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow("name,report")
@app.route('/refresh')
def refresh():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug = True)