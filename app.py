import os
from unicodedata import name
from warnings import catch_warnings
from numpy import datetime_data
import pytz
import tweepy
import pandas as pd
import pytz
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
api_key = 'gUHn0tg6rroVfRpddz0Dt9r3w'
api_key_secret = 'HQJKsuP7fs27VIvPMLV6r10XED45TCShpwCiWfJ1wslfoUVIu4'

access_token = '703740762710609920-WlBlY29OUSplpiRQlo86hvgBMMX22Rc'

access_token_secret = 'x9oiMT7LGGG1uYEnBLc6qXuYOJnT7FC3jTIuljrGoRPOK'



    # authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

@app.route('/logs')
def logs():
    filename = "data/datafile.csv"

    # initializing the titles and rows list
    fields = []
    user = []
    tweet_id = []
    date = []
    type_log = []

    # reading csv file
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            user.append(row[0])
            tweet_id.append(row[1])
            date.append(row[2])
            type_log.append(row[3])

    return render_template("logfiles.html", users=user,tweet_id=tweet_id,date=date,type=type_log)





@app.route('/')
def home1():
    if "password" in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/newTweet',methods=["POST","GET"])
def newTweet():
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
            date.append([tweet.created_at.astimezone(pytz.timezone('Asia/Manila')).replace(tzinfo=None,microsecond=0)])
            link.append([tweet.id])
            foulwords.append
        else:
            data.append([tweet.extended_tweet['full_text']])
            username.append([tweet.user.screen_name])
            date.append([tweet.created_at.astimezone(pytz.timezone('Asia/Manila')).replace(tzinfo=None,microsecond=0)])
            link.append([tweet.id])
            foulwords.append

    
    return jsonify('',render_template("model.html",users=username,tweet=data,date=date,link=link))


@app.route('/index', methods=["POST","GET"])
def home():


    if "password" in session:
        if request.method == "POST":
            old_pass = request.form["old_pass"]
            new_pass = request.form["new_pass"]
            confirm_pass = request.form["confirm_pass"]
            found_user = users.query.filter_by(user_password=old_pass).first()
            if new_pass != confirm_pass:
                flash("Unmatched Password")
                return redirect(url_for("home"))
            else:
                if found_user:
                    found_user.user_password = new_pass
                    db.session.commit()
                    session.pop("password", None)
                    flash("Password was Changed")
                    return redirect(url_for("login"))
                else:
                    flash("Current Password is incorrect")
                    return redirect(url_for("home"))
        else:
            
            keywords = [ 
                {'bobo, tanga, kupal, gago, tangina, pota, leche, ampota, fuck, stupid, bitch, btch'}
                ,         {'-hahahaha, -haha, -emoji, -RT'}
                ]
            language = ['''tl''']
            foulwords = [keywords]
            return render_template("index.html", foulwords=foulwords)
    else:
        flash("You need to Login First")
        return redirect(url_for("login"))




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
        api.update_status("sample reply. sorry for the inconvenience this is for my thesis project only.", in_reply_to_status_id = name , auto_populate_reply_metadata=True)
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




@app.route('/register', methods=["POST","GET"])
def register():
    if request.method == "POST":
        password = request.form["password"]
        found_user = users.query.filter_by(user_password=password).first()
        if found_user:
            found_user.user_password = password
            db.session.commit()
        else:
            addusr = users(password)
            db.session.add(addusr)
            db.session.commit()


        return redirect(url_for("login"))
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST","GET"])
def login():
    if "password" in session:
        return redirect(url_for("home"))
    else:
        if request.method == "POST":
            password = request.form["password"]
            found_user = users.query.filter_by(user_password=password).first()
            if found_user:
                session["password"] = password
                return redirect(url_for("home"))
            else:
                flash("Incorrect Password")
                return render_template("login.html")
        else:
            return render_template("login.html")


@app.route('/log')
def log():
    return render_template("logfiles.html")

@app.route("/logout")
def logout():
    session.pop("password", None)
    flash("Log out sucessfully")
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)