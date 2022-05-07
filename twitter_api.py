import tweepy
from tweepy import API
from tweepy import OAuthHandler



CONSUMER_KEY ='gUHn0tg6rroVfRpddz0Dt9r3w'
CONSUMER_SECRET = 'HQJKsuP7fs27VIvPMLV6r10XED45TCShpwCiWfJ1wslfoUVIu4'   
ACCESS_KEY = '703740762710609920-WlBlY29OUSplpiRQlo86hvgBMMX22Rc'  
ACCESS_SECRET = 'x9oiMT7LGGG1uYEnBLc6qXuYOJnT7FC3jTIuljrGoRPOK'


auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit= True)
api.update_status('Updating using OAuth authentication via Tw11eepy!', in_reply_to_status_id = 1522277485169483777  ,auto_populate_reply_metadata=True)