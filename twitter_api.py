import tweepy
import configparser
import pandas as pd


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

keywords = ['2022']

stream_tweets.filter(track=keywords)


#Data Fram
columns = ['User','Tweet']
data = []


for tweet in stream_tweets.tweets:
    if not tweet.truncated:
        data.append([tweet.user.location,tweet.text])
    else:
        data.append([tweet.user.location,tweet.extended_tweet['full_text']])

    

df = pd.DataFrame(data, columns=columns)
print(df)
