import os
from unicodedata import name
from warnings import catch_warnings
from numpy import datetime_data
import tweepy
import configparser
import pandas as pd
import datetime
import csv
from flask import Flask,redirect,url_for,render_template
from requests import request
from csv import writer
from datetime import datetime

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
        limit = 12
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

    report_date = datetime.now()
    with open('data/datafile.csv', 'a', newline='') as rep:
        rwriter = writer(rep)
        rwriter.writerow(["Cyberbot", tweet, report_date, "tweet"])
        rep.close()
    return redirect(url_for("home"))

    
@app.route("/product/<user>/<name>")
def user(name,user):
    screenname = user
    report_date = datetime.now()
    with open('data/datafile.csv', 'a', newline='') as rep:
        rwriter = writer(rep)
        rwriter.writerow([screenname, "twitter.com/"+screenname+"/status/"+name , report_date, "warning"])
        rep.close()
    try:
        api.update_status("We would like to ask you some questions. It will only take 10 mins of your time. It will be a great help for our team if you can lend us some of your precious time. Thank you and please keep safe, To participate please click the link thanks : https://forms.gle/M15pVFTXGsUb2xAs5", in_reply_to_status_id = name , auto_populate_reply_metadata=True)
        return render_template('warning.html',sucess="success") 

    except Exception as e :
        print(e)
        return render_template('warning.html',error=e, users = user,tweets=name)  
    
@app.route("/report/<username>/<name>")
def username(name,username):
    screenname = username
    report_date = datetime.now()
    with open('data/datafile.csv', 'a', newline='') as rep:
        rwriter = writer(rep)
        rwriter.writerow([screenname, "twitter.com/"+screenname+"/status/"+name , report_date, "report"])
        rep.close()
    try:
        api.report_spam(screen_name = username, perform_block = False)
        return render_template('report_warning.html',sucess="success")  
    except Exception as e :
        print(e)
        return render_template('report_warning.html',error=e, users = username,tweets=name) 
    
@app.route('/refresh')
def refresh():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug = True)