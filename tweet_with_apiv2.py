from requests_oauthlib import OAuth1Session
import os
import json
import tweepy
from dotenv import load_dotenv, find_dotenv
# from get_exclude_reply_user_ids import *
import datetime

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

def tweet_with_apiv2(tweet_message, media):
    
    # first using tweepy to upload media to twitter
    auth = tweepy.OAuth1UserHandler(
       consumer_key,
       consumer_secret,
       access_token,
       access_token_secret
    )

    api = tweepy.API(auth)
    media = api.media_upload(filename=media)

    media_id = media.media_id_string

    # exclude_reply_user_ids = get_exclude_reply_user_ids(scraped_tweet)
    payload = {"text": tweet_message, "media": {"media_ids": [media_id]}}

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    print("Response code: {}".format(response.status_code))

    # Saving the response as JSON
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    media = "assets/blank_belly_dark_mode/1.jpg"
    tweet_with_apiv2("test "+str(int(datetime.datetime.now().timestamp())), media)