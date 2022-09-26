import os
from apscheduler.schedulers.blocking import BlockingScheduler
from python_graphql_client import GraphqlClient
import requests
from requests import Session
from dotenv import load_dotenv, find_dotenv
import json
import pprint

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

BASE_CMC_URL = "https://pro-api.coinmarketcap.com"
COINMARKETCAP_API_KEY = os.environ.get("COINMARKETCAP_API_KEY")

global shitcoin
shitcoin = "shitcoin"
shitcoin = input("What shitcoin would you like to compare LN to? ").upper()

def coinmarketcap_get_shitcoin_mcap(shitcoin):
    if shitcoin == "123":
        return
    if not COINMARKETCAP_API_KEY:
        print("MISSING COINMARKETCAP API KEY. SET COINMARKETCAP_API_KEY in .env")
        exit()
    
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY}
    # resp = requests.get(f"{BASE_CMC_URL}/v1/global-metrics/quotes/latest", headers=headers)
    # print("${:,.2f}".format(resp.json()['data']['quote']['USD']['altcoin_market_cap']))
    # resp = requests.get("[{BASE_CMC_URL}/v1/cryptocurrency/quotes/latest", headers=headers)
    # print("${:,.2f}".format(resp.json()['data']))
    # print("SHITCOIN MARKET CAP:")

    session = Session()
    session.headers.update(headers)
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = { 'symbol': shitcoin, 'convert': 'USD' } # API parameters to pass in for retrieving specific cryptocurrency data

    global shitcoin_mcap
    response = session.get(url, params=parameters)
    shitcoin_mcap = json.loads(response.text)['data'][shitcoin]['quote']['USD']['market_cap']
    # print(shitcoin_mcap)
    # shitcoin = shitcoin
    return shitcoin
    return shitcoin_mcap

coinmarketcap_get_shitcoin_mcap(shitcoin=shitcoin.upper())