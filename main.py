import os
from apscheduler.schedulers.blocking import BlockingScheduler
from python_graphql_client import GraphqlClient
import requests
from dotenv import load_dotenv, find_dotenv
from amboss_get_LN_capacity import *
from coinmarketcap_get_btc_usd import *
from coinmarketcap_get_shitcoin_mcap import *
# import coinmarketcap_get_btc_usd
from tweepy_send_tweet import *
import random
import urllib.request


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

sched = BlockingScheduler()

# BASE_CMC_URL = "https://pro-api.coinmarketcap.com"
# COINMARKETCAP_API_KEY = os.environ.get("COINMARKETCAP_API_KEY")

def main():
    while True:
        option = input("What kind of tweet would you like to send? (flippening/LNcap/quit) ")
        if option.lower() == "quit":
            quit()
        if option.lower() == "flippening":
            LN_flippening_tracker()
        if option.lower() == "lncap":
            LN_cap()
        else:
            continue


# @sched.scheduled_job("cron", hour=15, minute=0, timezone="America/Denver")
def LN_flippening_tracker():
    # fetching LN capacity in BTC
    amboss_get_LN_capacity()
    LN_capacity_text = "LN channel capacity: " + str(LN_capacity_in_BTC) + "BTC"

    # fetching BTC price in USD
    coinmarketcap_get_btc_usd()
    btc_usd_text ="BTC price: ${:,.2f}".format(btc_usd)

    # Calculating current amount allocated in the LN
    LN_mcap_text = "$ allocated in the LN: ${:,.2f}".format(LN_capacity_in_BTC*btc_usd)

    # fetching shitcoin mcap
    coinmarketcap_get_shitcoin_mcap(shitcoin=shitcoin)
    shitcoin_mcap_text = shitcoin.upper() + " market cap: ${:,.2f}".format(shitcoin_mcap)
    
    # Comparing LN network with shitcoin
    percentage_bar = int(LN_capacity_in_BTC*btc_usd/shitcoin_mcap*100/5)
    if percentage_bar > 20:
        percentage_bar = 20
    percentage_calculation = LN_capacity_in_BTC*btc_usd/shitcoin_mcap*100
    if percentage_calculation > 100:
        percentage_calculation = "FLIPPED (LN = %{:,.2f}".format(percentage_calculation) + " " + shitcoin + ")"

    flippening_progress_text = (
        "Progress (LN flippening " + shitcoin + ")\n" + 
        "▓" * percentage_bar + "░" * (20 - percentage_bar) + " " +
        str("{:,.2f}".format(percentage_calculation)) + "%"
    )

    # asking if would like to choose image or pick a random one
    random_image_or_choose = input("Pick and image or choose at random? (pick/random)")
    if random_image_or_choose == "pick":
        image_url = input("insert image full URL or path here: ")
        urllib.request.urlretrieve(image_url, "00000001.jpg")
        tweet_image = "00000001.jpg"
    if random_image_or_choose == "random":
        random_image_picker = random.randint(1,5)
        tweet_image = str(random_image_picker) + ".png"
        

    # LIGHTNING NETWORK FLIPPENING TRACKER TWEET
    tweet_message = (
    "LIGHTNING NETWORK FLIPPENING TRACKER - LN vs " + shitcoin + "\n\n" + 
    LN_capacity_text + "\n" + 
    btc_usd_text + "\n" + 
    LN_mcap_text + "\n\n" + 
    shitcoin_mcap_text + "\n\n" + 
    flippening_progress_text
    )
    print(tweet_message)
    tweepy_send_tweet(tweet_message,tweet_image)
    print("Tweet sent")


def LN_cap():
    # fetching LN capacity in BTC
    amboss_get_LN_capacity()
    LN_capacity_text = "Current LN channel capacity: " + str(LN_capacity_in_BTC) + "BTC"

    # picking random image
    random_image_picker = random.randint(1,5)
    tweet_image = str(random_image_picker) + ".png"

    # LIGHTNING NETWORK CAPACITY TWEET
    tweet_message = (
    "LIGHTNING NETWORK CAPACITY UPDATE" + "\n\n" + 
    LN_capacity_text + "\n"
        )
    tweepy_send_tweet(tweet_message,tweet_image)
    print("Tweet sent")


# just a comment

if __name__ == "__main__":
    main()
