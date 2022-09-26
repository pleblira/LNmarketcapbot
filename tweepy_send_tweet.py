import tweepy
from amboss_get_LN_capacity import *
import os

from dotenv import load_dotenv, find_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# consumer_key = os.environ.get("CONSUMER_KEY")
# consumer_secret = os.environ.get("CONSUMER_SECRET")
# access_token = os.environ.get("ACCESS_TOKEN")
# access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

def tweepy_send_tweet(tweet_message,tweet_image):
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
    
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)

    api = tweepy.API(auth)
    # get_capacity()

    # Define the tweet text
    # tweet="Current LN channel capacity: " + str(capacity_btc) + "BTC"
    # tweet_message="Current LN channel capacity: " + str(capacity_btc) + "BTC"

    # For text only tweets
    # api.update_status(tweet)

    # tweet_image ='LNmarketcapbotLIGHTNING.png'

    # Generate text tweet with media (image)
    api.update_status_with_media(tweet_message, tweet_image)