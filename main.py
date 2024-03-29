from amboss_get_LN_capacity import *
from coinmarketcap_get_btc_usd import *
from coinmarketcap_get_shitcoin_mcap import *
from tweet_with_apiv2 import *
import random
import urllib.request
import text_on_images
import subprocess
import os
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from sparkle_gif_create_frames import *
from s3_update_LN_capacity_and_compare import *
import time
from post_note import *
from upload_to_voidcat_and_return_url import *

def timer(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        func(*args, **kwargs)
        print("Function took:", time.time() - before, "seconds")
    
    return wrapper

def manual_tweet():
    while True:
        option = input("What kind of tweet would you like to send (LN_flippening/LN_cap/autotest/quit)? ")
        if option.lower() == "quit":
            quit()
        if option.lower() == "ln_flippening":
            LN_flippening_tracker()
        if option.lower() == "ln_cap":
            LN_cap(automated=False)
        if option.lower() == "autotest":
            LN_cap(automated=True)
        else:
            continue

def LN_flippening_tracker():
    # fetching LN capacity in BTC
    LN_capacity_in_BTC = amboss_get_LN_capacity()
    LN_capacity_text = f"LN channel capacity: {str(LN_capacity_in_BTC)} BTC"

    # fetching BTC price in USD
    btc_usd = coinmarketcap_get_btc_usd()
    btc_usd_text =f"BTC price: ${btc_usd:,.0f}"

    # Calculating current amount allocated in the LN
    LN_mcap_text = f"$ allocated in the LN: ${LN_capacity_in_BTC*btc_usd:,.0f}"

    # fetching shitcoin mcap
    shitcoin = input("What shitcoin would you like to compare LN to? ").upper()
    coinmarketcap_get_shitcoin_mcap(shitcoin)
    shitcoin_mcap = coinmarketcap_get_shitcoin_mcap(shitcoin=shitcoin)[1]
    shitcoin_mcap_text = f"{shitcoin.upper()} market cap: ${shitcoin_mcap:,.0f}"
    
    # Comparing LN network with shitcoin
    percentage_bar = int(LN_capacity_in_BTC*btc_usd/shitcoin_mcap*100/5)
    if percentage_bar > 20:
        percentage_bar = 20
    percentage_calculation = str(f"{LN_capacity_in_BTC*btc_usd/shitcoin_mcap*100:.2f}")
    if float(percentage_calculation) > 100:
        percentage_calculation = f"FLIPPED (LN market cap = {float(percentage_calculation)/100:.2f}X {shitcoin.upper()}'s market cap)"

    flippening_progress_text = (
        "Progress (LN flippening " + shitcoin + ")\n" + 
        "▓" * percentage_bar + "░" * (20 - percentage_bar) + " " +
        percentage_calculation + "%"
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
        tweet_image = "assets/full_belly_dark_mode/" + str(random_image_picker) + ".png"
    else:
        print("Wrong option detected")
        quit()

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
        # tweepy_send_tweet(tweet_message,tweet_image)
        tweet_with_apiv2(tweet_message,tweet_image)
        print("Tweet sent")
        if random_image_or_pick == "pick" and image_url_or_path.find("http")>-1 and image_url_or_path.find("//")>0:
            os.remove("assets/00000001.jpg")
        quit()
    else:
        return

# script initialization: It auto-starts the daily LN_cap tweet at 12 pm ET. User can press Ctrl+C or Ctrl+Break to start manual tweeting functionality

@timer
def LN_cap(automated):
    # fetching LN capacity in BTC
    LN_capacity_in_BTC = amboss_get_LN_capacity()
    LN_capacity_text = f"Current LN capacity: {LN_capacity_in_BTC} BTC"

    # fetching BTC price in USD
    btc_usd = coinmarketcap_get_btc_usd()
    btc_usd_text =f"BTC price: ${btc_usd:,.0f}"

    # Calculating current amount allocated in the LN
    LN_mcap_text = f"$ allocated in the LN: ${LN_capacity_in_BTC*btc_usd:,.0f}"

    # picking random image
    random_image_picker = random.randint(1,6)
    # when it picks image 4, switch to image 2 (removing image 4 from circulation for now)
    if random_image_picker == 4:
        random_image_picker = 2
    with open("previously_selected_images.txt","r") as file:
        lines = file.readlines()
        if len(lines) == 0:
            last_two_random_picks = "-1"
            last_random_pick = "-1"
        else:
            last_random_pick = lines[len(lines)-1].strip()
            last_two_random_picks = lines[len(lines)-1].strip() + lines[len(lines)-2].strip()
    while str(last_two_random_picks).find(str(random_image_picker)) > -1:
        random_image_picker = random.randint(1,6)
    with open("previously_selected_images.txt","a") as file:
        file.write(str(random_image_picker) + "\n")

    # typing LN capacity on mascot
    tweet_image = f"assets/blank_belly_dark_mode/{str(random_image_picker)}.jpg"
    tweet_image = text_on_images.image_draw_angled(LN_capacity_in_BTC, tweet_image)

    # making tweet image a gif with sparkle
    sparkle_gif_create_frames("assets/tweet_image.jpg", random_image_picker)

    # running S3_update_LN_capacity_and_compare function
    info_from_s3 = s3_update_LN_capacity_and_compare(LN_capacity_in_BTC, automated)

    # Getting the weekly increase based on the bot's history
    LN_capacity_period_change_text = info_from_s3[0]

    # LN Capacity ATH announcement
    LN_capacity_ATH_text = ""
    if info_from_s3[1] == True:
        LN_capacity_ATH_text = "\n\nLN Capacity ATH!!"

    # LIGHTNING NETWORK CAPACITY TWEET
    tweet_message = (
    "LIGHTNING NETWORK CAPACITY UPDATE" + "\n\n" + 
    LN_capacity_text + "\n" + 
    btc_usd_text + "\n" +
    LN_mcap_text
     + "\n" + "\n"
    + LN_capacity_period_change_text
     + LN_capacity_ATH_text
        )
    print(tweet_message)
    if automated == True: 
        url_of_note_on_snort_social = post_note(tweet_message + " " + upload_to_voidcat_and_return_url("assets/tweet_image_sparkled.gif", "gif"))
        tweet_with_apiv2(tweet_message+"\n\nNOSTR: "+url_of_note_on_snort_social,"assets/tweet_image_sparkled.gif")
        print("Tweet sent")
    else:
        confirm_send_tweet = input("Send tweet (y/n)? ")
        if confirm_send_tweet == "y":
            url_of_note_on_snort_social = post_note(tweet_message + " " + upload_to_voidcat_and_return_url("assets/tweet_image_sparkled.gif", "gif"))
            tweet_with_apiv2(tweet_message+"\n\nNOSTR: "+url_of_note_on_snort_social,"assets/tweet_image_sparkled.gif")
            print("Tweet sent")
            quit()
        else:
            return

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(lambda: LN_cap(automated=True), 'cron', hour=12, minute=00, timezone="America/New_York")
    print('Press Ctrl+{0} to stop scheduler and switch to manual tweet.'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nScheduler stopped. Starting manual tweet functionality.\n\n")
        manual_tweet()