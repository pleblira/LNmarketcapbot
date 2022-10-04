from amboss_get_LN_capacity import *
from coinmarketcap_get_btc_usd import *
from coinmarketcap_get_shitcoin_mcap import *
from tweepy_send_tweet import *
import random
import urllib.request
import text_on_images
import subprocess
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def manual_tweet():
    while True:
        option = input("What kind of tweet would you like to send (LN_flippening/LN_cap/quit)? ")
        if option.lower() == "quit":
            quit()
        if option.lower() == "ln_flippening":
            LN_flippening_tracker()
        if option.lower() == "ln_cap":
            LN_cap()
        else:
            continue

# @sched.scheduled_job("cron", hour=15, minute=0, timezone="America/Denver")
def LN_flippening_tracker():
    # fetching LN capacity in BTC
    LN_capacity_in_BTC = amboss_get_LN_capacity()
    LN_capacity_text = "LN channel capacity: " + str(LN_capacity_in_BTC) + "BTC"

    # fetching BTC price in USD
    btc_usd = coinmarketcap_get_btc_usd()
    btc_usd_text ="BTC price: ${:,.0f}".format(btc_usd)

    # Calculating current amount allocated in the LN
    LN_mcap_text = "$ allocated in the LN: ${:,.0f}".format(LN_capacity_in_BTC*btc_usd)

    # fetching shitcoin mcap
    shitcoin = input("What shitcoin would you like to compare LN to? ").upper()
    coinmarketcap_get_shitcoin_mcap(shitcoin)
    shitcoin_mcap = coinmarketcap_get_shitcoin_mcap(shitcoin=shitcoin)[1]
    shitcoin_mcap_text = shitcoin.upper() + " market cap: ${:,.0f}".format(shitcoin_mcap)
    
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
    random_image_or_pick = input("Pick and image or choose at random (pick/random)? ")
    if random_image_or_pick == "pick":
        image_url_or_path = input("insert image full URL or path here: ")
        if image_url_or_path.find("http")>-1 and image_url_or_path.find("//")>0:
            urllib.request.urlretrieve(image_url_or_path, "assets/00000001.jpg")
            tweet_image = "assets/00000001.jpg"
        else:
            tweet_image = image_url_or_path
    elif random_image_or_pick == "random":
        random_image_picker = random.randint(1,5)
        tweet_image = "assets/full_belly/" + str(random_image_picker) + ".png"
    else:
        print("Wrong option detected")
        quit()
    subprocess.call(('open', tweet_image))

    custom_text_yes_or_no = input("Would you like to add custom text to the tweet (y/n)? ")
    if custom_text_yes_or_no == "y":
        custom_text = input("Type text (single line): ")

    # LIGHTNING NETWORK FLIPPENING TRACKER TWEET
    tweet_message = (
    "LIGHTNING NETWORK FLIPPENING TRACKER - LN vs $" + shitcoin + "\n\n" + 
    LN_capacity_text + "\n" + 
    btc_usd_text + "\n" + 
    LN_mcap_text + "\n\n" + 
    shitcoin_mcap_text + "\n\n" + 
    flippening_progress_text
    )
    if custom_text_yes_or_no == "y":
        tweet_message = tweet_message + "\n\n" + custom_text
    print(tweet_message)
    confirm_send_tweet = input("Send tweet (y/n)? ")
    if confirm_send_tweet == "y":
        tweepy_send_tweet(tweet_message,tweet_image)
        print("Tweet sent")
        if random_image_or_pick == "pick" and image_url_or_path.find("http")>-1 and image_url_or_path.find("//")>0:
            os.remove("assets/00000001.jpg")
        quit()
    else:
        return
    # tweepy_send_tweet has been disabled for testing


def LN_cap():
    # fetching LN capacity in BTC
    LN_capacity_in_BTC = amboss_get_LN_capacity()
    LN_capacity_text = "Current LN channel capacity: " + str(LN_capacity_in_BTC) + " BTC"

    # picking random image
    random_image_picker = random.randint(1,6)
    tweet_image = "assets/blank_belly_dark_mode/" + str(random_image_picker) + ".jpg"

    # typing LN capacity on mascot
    # tweet_image = text_on_images.image_draw_angled(LN_capacity_in_BTC, tweet_image)
    tweet_image = text_on_images.image_draw_angled(LN_capacity_in_BTC, tweet_image)
    subprocess.call(('open', "assets/tweet_image.jpg"))

    custom_text_yes_or_no = input("Would you like to add custom text to the tweet (y/n)? ")
    if custom_text_yes_or_no == "y":
        custom_text = input("Type text (single line): ")

    # LIGHTNING NETWORK CAPACITY TWEET
    tweet_message = (
    "LIGHTNING NETWORK CAPACITY UPDATE" + "\n\n" + 
    LN_capacity_text
        )
    if custom_text_yes_or_no == "y":
        tweet_message = tweet_message + "\n\n" + custom_text
    print(tweet_message)
    confirm_send_tweet = input("Send tweet (y/n)? ")
    if confirm_send_tweet == "y":
        tweepy_send_tweet(tweet_message,"assets/tweet_image.jpg")
        print("Tweet sent")
        os.remove("assets/tweet_image.jpg")
        quit()
    else:
        return

# if __name__ == "__main__":
#     main()

# script initialization: It auto-starts the daily LN_cap tweet at 12 pm ET. User can press Ctrl+C or Ctrl+Break to start manual tweeting functionality

def LN_cap_automated():
    # fetching LN capacity in BTC
    LN_capacity_in_BTC = amboss_get_LN_capacity()
    LN_capacity_text = "Current LN channel capacity: " + str(LN_capacity_in_BTC) + " BTC"

    # picking random image
    random_image_picker = random.randint(1,6)
    tweet_image = "assets/blank_belly_dark_mode/" + str(random_image_picker) + ".jpg"

    # typing LN capacity on mascot
    tweet_image = text_on_images.image_draw_angled(LN_capacity_in_BTC, tweet_image)

    # LIGHTNING NETWORK CAPACITY TWEET
    tweet_message = (
    "LIGHTNING NETWORK CAPACITY UPDATE" + "\n\n" + 
    LN_capacity_text
        )
    print(tweet_message)
    tweepy_send_tweet(tweet_message,"assets/tweet_image.jpg")
    print("Tweet sent")
    os.remove("assets/tweet_image.jpg")

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(LN_cap_automated, 'cron', hour=12, minute=00, timezone="America/New_York")
    print('Press Ctrl+{0} to stop scheduler and switch to manual tweet.'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nScheduler stopped. Starting manual tweet functionality.\n\n")
        manual_tweet()


