import json
from multiprocessing import connection
import os
from select import select
import sqlite3
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
from datetime import datetime,date
from textblob import TextBlob


# connection = sqlite3.connect("keywords.db")
# cursor = connection.cursor()



# questions = """CREATE TABLE IF NOT EXISTS keywords1(q_id INTEGER PRIMARY KEY AUTOINCREMENT, keyword_text text) """
# cursor.execute(questions)



connection2 = sqlite3.connect("logs.db")
cursor2 = connection2.cursor()

# cursor2.execute("""CREATE TABLE IF NOT EXISTS tweet_counter (id INTEGER PRIMARY KEY AUTOINCREMENT, count_date text, no_oftweet INTEGER) """)




# CHECKING IF TODAY's DATE ALREADY EXIST ON THE COUNTER 
today = date.today()
date_only = today.strftime("%Y-%m-%d")

cursor2.execute("Select * from tweet_counter where count_date = ?",[date_only])
result = cursor2.fetchall()

if(len(result) == 0):
    print("no data")
    cursor2.execute("INSERT INTO tweet_counter(count_date,no_oftweet) values(?,?)", (date_only,0))
    connection2.commit()
else:
    print("data found")




# sql1 = """DROP TABLE tweets """
# sql1 = """CREATE TABLE IF NOT EXISTS tweets(id INTEGER PRIMARY KEY AUTOINCREMENT, tweet_text text,user_id text,tweet_date text, tweet_id text,date_only text) """
# sql1 = ALTER TABLE tweets ADD column tweet_hour integer """
# sql1 = """DELETE FROM tweets where id < 137  """
# sql1 = """ UPDATE tweets set tweet_hour = 9 """
# cursor2.execute(sql1)

# connection2.commit()



# sql2 = """CREATE TABLE IF NOT EXISTS warning(warn_id INTEGER PRIMARY KEY AUTOINCREMENT, tweet_text text,user_id text,tweet_date text,tweet_id text,tweet_status text,date_only text) """
# sql2 = """ Update warning set date_only = ? """
# sql2 = """ ALTER TABLE warning add column tweet_hour integer """
# cursor2.execute(sql2)
# connection2.commit()






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

@app.route('/')
def home1():
    if "password" in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/readTweet',methods=["POST","GET"])
def readTweet():
    date = request.form["date"]
    connection2 = sqlite3.connect("logs.db")
    cursor2 = connection2.cursor()
    cursor2.execute("Select * from tweets where date_only = ?",[date])
    results = cursor2.fetchall()
    tweet = []
    id = []
    link = []
    date = []
    for x in range(0,len(results)):
        tweet.append(results[x][1])
        id.append(results[x][2])
        link.append(results[x][4])
        date.append(results[x][3])
    return jsonify({'tweet':tweet,'id':id,'link':link,'date':date})



@app.route('/newTweet',methods=["POST","GET"])
def newTweet():

    class Listener(tweepy.Stream):
    
        def on_status(self, status):

            #UPDATING THE COUNTER
            newConnection = sqlite3.connect("logs.db")
            newCursor = newConnection.cursor()



            today = date.today()
            date_only = today.strftime("%Y-%m-%d")

            newCursor.execute("UPDATE tweet_counter set no_oftweet = no_oftweet + 1 where count_date = ?",[date_only])
            newConnection.commit()


            #CHECKING POLARITY
            analysis = TextBlob(status.text)
            if analysis.polarity < 0:

                tweet_id = ""
                user_id = ""
                analysis = ""
                tweet_date = ""
                tweet_text = ""
                
                if hasattr(status, "retweeted_status"):  # Check if Retweet
                    try:
                        tweet_text= status.retweeted_status.extended_tweet["full_text"]
                    except AttributeError:
                        tweet_text = status.retweeted_status.text
                else:
                    try:
                        tweet_text = status.extended_tweet["full_text"]
                    except AttributeError:
                        tweet_text = status.text 

                #ASSIGNING VALUE TO VARIABLES
                tweet_date = status.created_at.astimezone(pytz.timezone('Asia/Manila')).replace(tzinfo=None,microsecond=0)
                tweet_id = status.id
                user_id =  status.user.screen_name
                today = date.today()
                date_only = today.strftime("%Y-%m-%d")
                month_only = today.strftime("%m")
                day_only = today.strftime("%d")
                year_only = today.strftime("%Y")
                hour_only = datetime.now().hour
                print(user_id)
                print(tweet_text)


                #INSERTING VALUES TO DATABASE

                connection2 = sqlite3.connect("logs.db")
                cursor2 = connection2.cursor()
                cursor2.execute("INSERT INTO tweets(tweet_text,user_id,tweet_date,tweet_id,date_only,tweet_month,tweet_day,tweet_year,tweet_hour) VALUES(?,?,?,?,?,?,?,?,?)",(tweet_text,user_id,tweet_date,tweet_id,date_only,month_only,day_only,year_only,hour_only))
                connection2.commit()

                    
                self.disconnect();    
        


    
    stream_tweets = Listener(api_key,api_key_secret,access_token,access_token_secret)
    
    
    connection = sqlite3.connect("keywords.db")
    cursor = connection.cursor()
    keywords = []
    cursor.execute("Select * from keywords1")
    results = cursor.fetchall()
    for x in range(0,len(results)):
        keywords.append(results[x][1])

    language = ['''tl''']




    stream_tweets.filter(track=keywords, languages=language)

    
    return ''


@app.route('/index', methods=["POST","GET"])
def home():
    if request.method == "POST":
            old_pass = request.form["old_pass"]

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
            connection = sqlite3.connect("keywords.db")
            cursor = connection.cursor()
            keywords = []
            cursor.execute("Select * from keywords1")
            results = cursor.fetchall()
            for x in range(0,len(results)):
                keywords.append(results[x][1])

            language = ['''tl''']
            foulwords = [keywords]
            return render_template("index.html", foulwords=keywords)
    else:
        flash("You need to Login First")
        return redirect(url_for("login"))





@app.route('/checktweet')
def checktweet():
    try:
        tweet = api.get_status('1526256077842817024')
        print("a")
    except Exception as e :
        print(e)

    return redirect(url_for("login"))   



@app.route('/tweet', methods=["POST"])
def tweet():
    try:
        tweet = request.form["tweetTxt"]
        api.update_status(tweet)
    # report_date = datetime.now()
    # with open('data/datafile.csv', 'a', newline='') as rep:
    #     rwriter = writer(rep)
    #     rwriter.writerow(["Cyberbot", tweet, report_date, "tweet"])
    #     rep.close()
    except Exception as e:
        print(e)

    return redirect(url_for("ourLogs"))


@app.route("/warning", methods=["POST"])
def warning():
    tweetTxt = request.form["tweetTxt"]
    userID = request.form["userID"]
    date = request.form["tweetDate"]
    tweetID = request.form["tweetID"]
    status = "active"


    connection = sqlite3.connect("logs.db")
    cursor = connection.cursor()
    cursor.execute("Select * from tweets where tweet_id = ?",([tweetID]))
    results = cursor.fetchall()

    dateofTweet = str(results[0][5])
    monthofTweet = str(results[0][6])
    dayofTweet = str(results[0][7])
    yearofTweet = str(results[0][8])
    hourofTweet = str(results[0][9])
    try:
        api.update_status("hello, our system noticed that your tweet/reply contains inappropriate languages that may induce or result to cyberbullying. This will serve as a warning and we advice to use proper online etiquette.", in_reply_to_status_id = tweetID , auto_populate_reply_metadata=True)
        connection143 = sqlite3.connect("logs.db")
        cursor123 = connection143.cursor()
        cursor123.execute("INSERT INTO warning(tweet_text, user_id, tweet_date, tweet_id, tweet_status,date_only,tweet_month,tweet_day,tweet_year,tweet_hour) VALUES(?,?,?,?,?,?,?,?,?,?)", (tweetTxt,userID,date,tweetID,status,dateofTweet,monthofTweet,dayofTweet,yearofTweet,hourofTweet))
        connection143.commit()
        cursor123.execute("DELETE FROM tweets where tweet_id = ?", [tweetID])
        connection143.commit()
        return jsonify({'status': "success"})
    except Exception as e :
        error = str(e)
        print (error)
        return jsonify({'status': "failed", 'error': error})
    




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
        return render_template('report_warning.html',sucess="success", users = screenname,tweets=name)
    except Exception as e :
        print(e)
        return render_template('report_warning.html',error=e, users = screenname,tweets=name)



@app.route('/refresh')
def refresh():
    return redirect(url_for("home"))


# LOGS ROUTE

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


@app.route('/log')
def log():
    return render_template("logfiles.html")



# ACCOUNT ROUTE


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

            
@app.route("/forgot", methods=["POST","GET"])
def forgot():
    if request.method == "POST":
                secret = request.form["secretKey"]
                key = "123"
                password = users.query.filter_by(_id="1").first()
                passw = password.user_password
                if secret ==  key:
                    #passw.append
                    print(passw)
                    flash("Your Password is  "+ passw)
                    return redirect(url_for("login"))
                if secret !=  key:
                    flash("wrong key")
                    
                    return redirect(url_for("login"))
                else:
                    flash("error")
                    return redirect(url_for("login"))
                    
    else:
        return render_template("forgot.html")

@app.route("/logout")
def logout():
    session.pop("password", None)
    flash("Log out sucessfully")
    return redirect(url_for("login"))


#KEYWORD ROUTES


@app.route('/insertkey', methods=["POST","GET"])
def insert():
    if request.method == "POST":
        new_keyword = request.form["keyword"]

        connection = sqlite3.connect("keywords.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO keywords1(keyword_text) VALUES(?)",[new_keyword])
        connection.commit()
    else:
        return redirect(url_for("home"))
    return redirect(url_for("home"))


@app.route("/viewWords")
def viewWords():
    connection = sqlite3.connect("keywords.db")
    cursor = connection.cursor()
    key_id = []
    keywords = []
    cursor.execute("Select * from keywords1")
    results = cursor.fetchall()
    for x in range(0,len(results)):
        keywords.append(results[x][1])
        key_id.append(results[x][0])
    return render_template("keywords.html",keywords=keywords,key_id=key_id)


@app.route('/deleteKeyword', methods=["POST"])
def deleteKeyword():
    key_id = request.form["key_id"]
    connection = sqlite3.connect("keywords.db")
    cursor = connection.cursor()
    cursor.execute("Delete from keywords1 where q_id = ?",[key_id])         
    connection.commit()
    
    return jsonify({'name' : key_id})


@app.route('/ourLogs')
def ourLogs():
    return render_template("dashboard.html")

@app.route('/readDatabase', methods=["POST"])
def readDatabase():
    date = request.form["date"]
    connection = sqlite3.connect("logs.db")
    cursor = connection.cursor()
    cursor.execute("select tweet_hour,COUNT(tweet_text)from tweets where date_only = ? GROUP BY tweet_hour",[date])
    result = cursor.fetchall()
    return jsonify({"result":result})



@app.route("/getTweetReport", methods=["POST"])
def getTweetReport():
    date = request.form["date"]
    connection = sqlite3.connect("logs.db")
    cursor = connection.cursor()

    cursor.execute("select no_oftweet from tweet_counter where count_date = ?", [date])
    result = cursor.fetchall()

    cursor2 = connection.cursor()
    cursor2.execute("select COUNT(tweet_text) as No_ofTweet from tweets where date_only = ?", [date])
    result2 = cursor2.fetchall()

    cursor3 = connection.cursor()
    cursor3.execute("select count(tweet_text) as No_Tweets, user_id from warning group by user_id ORDER BY No_Tweets DESC")
    result3 = cursor3.fetchall()

    cursor4 = connection.cursor()
    cursor4.execute("select COUNT(tweet_text) as No_ofwarn from warning where date_only = ?", [date])
    result4 = cursor4.fetchall()
    return jsonify({"raw": result,"filtered":result2,"users":result3,"warn":result4})


@app.route("/checkWarned",methods=["POST"])
def checkWarned():
    connection = sqlite3.connect("logs.db")
    cursor = connection.cursor()

    cursor.execute("select * from warning")
    result = cursor.fetchall()
    for x in range(0,len(result)):
        try:
            tweet = api.get_status(result[x][4])
            
        except Exception as e :
            cursor2 = connection.cursor()
            cursor2.execute("UPDATE warning set tweet_status = 'removed' where tweet_id = ?",[result[x][4]])
            connection.commit()

    return jsonify("","")


@app.route("/reportList")
def reportList():
    return render_template("logsReprt.html")

@app.route("/warnList")
def warnList():
    return render_template("logsWarn.html")


@app.route("/getAllReprt",methods=["POST"])
def getAllReprt():
    connection = sqlite3.connect("logs.db")
    cursor = connection.cursor()
    cursor.execute("select * from report")
    result = cursor.fetchall()
    
    return jsonify({"report":result})


@app.route("/getAllWarned",methods=["POST"])
def getAllWarned():
    connection = sqlite3.connect("logs.db")
    cursor = connection.cursor()
    cursor.execute("select * from warning")
    result = cursor.fetchall()
    
    return jsonify({"tweets":result})

@app.route("/getAvailableWarn",methods=["POST"])
def getAvailableWarn():
    connection = sqlite3.connect("logs.db")
    cursor = connection.cursor()
    cursor.execute("select * from warning where tweet_status = 'active'")
    result = cursor.fetchall()
    
    return jsonify({"tweets":result})


@app.route("/getDeletedWarn",methods=["POST"])
def getDeletedWarn():
    connection = sqlite3.connect("logs.db")
    cursor = connection.cursor()
    cursor.execute("select * from warning where tweet_status = 'removed'")
    result = cursor.fetchall()
    
    return jsonify({"tweets":result})

@app.route("/getWarnDate",methods=["POST"])
def getWarnDate():
    type = request.form["type"]
    date = request.form["date"]
    connection = sqlite3.connect("logs.db")
    cursor = connection.cursor()

    if type == "ALL":
        cursor.execute("select * from warning where date_only = ?",[date])
    elif type == "AVAIL":
        cursor.execute("select * from warning where tweet_status = 'active' AND date_only = ?",[date])
    else:
        cursor.execute("select * from warning where tweet_status = 'removed' AND date_only = ?",[date])
    
    result = cursor.fetchall()
    
    return jsonify({"tweets":result})



@app.route("/getSearchData",methods=["POST"])
def getSearchData():
    text = request.form["text"]
    connection = sqlite3.connect("logs.db")
    cursor = connection.cursor()
    cursor.execute("select * from warning where user_id LIKE ? ",["@%"+text+"%"])
 
    result = cursor.fetchall()
    
    return jsonify({"tweets":result})



if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)