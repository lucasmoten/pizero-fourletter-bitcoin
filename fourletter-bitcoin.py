#!/usr/bin/env python

import calendar
import time
import fourletterphat
import urllib
import json
import random
from subprocess import Popen, PIPE
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime

# Variables needed. These are secrets. Don't share
rpc_user = "You should have configured this in your bitcoin.conf"
rpc_password = "You should have configured this in your bitcoin.conf"
rpc_host = "Routeable ip address or hostname to your bitcoin node"
rpc_port = "8332"

# Panels to display. 1 to show it, 0 to skip
show_welcome = 1
show_time = 1
show_temp = 1
show_price = 1
show_pricemsg = 1
show_blockheight = 1
show_mempoolsize = 1
show_minfee = 1
show_feerec = 1

# Timing
minutes_between_api_updates = 5
seconds_for_panel_display = 1
scrolling_speed = 8

# Subroutines - No need to change stuff below this line -----------------------------------

class AppURLopener(urllib.FancyURLopener):
    version = "PiZero-fourletter-bitcoin/1.1"
urllib._urlopener = AppURLopener()

def scroll_message(message):
    m = "    " + message
    fourletterphat.clear()
    while len(m) > 3:
        fourletterphat.print_str(m[:4])
        m = m[1:]
        fourletterphat.show()
        time.sleep(float(1) / scrolling_speed)
    time.sleep(seconds_for_panel_display)

def gettemp():
    temperature = Popen(["vcgencmd", "measure_temp"], stdout=PIPE)
    temperature = temperature.stdout.read().decode('utf-8')
    temperature = temperature[5:7] + "C"
    return temperature

def getbitcoinprice():
    a = ['coindesk','blockchain']
    ra = random.choice(a)
    if ra in ['coindesk']:
        p, pm = btcprice_from_coindesk()
    if ra in ['blockchain']:
        p, pm = btcprice_from_blockchain()
    if p in ['?']:
        p, pm = getbitcoinprice()
    # Grab first 4. TBD: cut at decimal to handle 10K+
    p = p[:4]
    return p, pm

def btcprice_from_coindesk():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'
    priceurl = urllib.urlopen(url)
    if(priceurl.getcode() == 200):
        pricedata = priceurl.read()
        jsonpricedata = json.loads(pricedata)
        bitcoin_price = jsonpricedata["bpi"]["USD"]["rate"]
        bitcoin_price = bitcoin_price.replace(",","")
        bitcoin_price = bitcoin_price[:4]
        m = 'Powered by CoinDesk @ https://coindesk.com/coindesk-api'
        return bitcoin_price, m
    else:
        return "?", "Error getting price from Coindesk"

def btcprice_from_blockchain():
    url = 'https://blockchain.info/ticker'
    priceurl = urllib.urlopen(url)
    if(priceurl.getcode() == 200):
        pricedata = priceurl.read()
        jsonpricedata = json.loads(pricedata)
        bitcoin_price = str(jsonpricedata["USD"]["last"])
        bitcoin_price = bitcoin_price.replace(",","")
        bitcoin_price = bitcoin_price[:4]
        m = 'Price courtesy of Blockchain.info @ https://blockchain.com/api'
        return bitcoin_price, m
    else:
        return "?", "Error getting price from Blockchain"

def rpcinfo_from_node():
    try:
        rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_host, rpc_port), timeout=120)
        mining_info = rpc_connection.getmininginfo()
        mempool_info = rpc_connection.getmempoolinfo()
        blockchain_info = rpc_connection.getblockchaininfo()
        mempool_usage = mempool_info["usage"]
        mempool_minfee = mempool_info["mempoolminfee"]
        mempool_size = str(mempool_usage / (1024*1024))
        satfee = str(int(mempool_minfee * 100000000))
        block_height = str(blockchain_info["blocks"])
    except:
        mempool_usage = "?"
        mempool_minfee = "?"
        mempool_size = "?"
        satfee = "?"
        block_height = "?"
        scroll_message("RPC ERROR")
        scroll_message("CHECK VARIABLES")
    return mempool_usage, mempool_minfee, mempool_size, satfee, block_height

def feerecommendations():
    url = 'https://bitcoinfees.earn.com/api/v1/fees/recommended'
    # special note: we get 403 errors on this url if using default user agent
    respurl = urllib.urlopen(url)
    if(respurl.getcode() == 200):
        respdata = respurl.read()
        jsonrespdata = json.loads(respdata)
        fastest = str(jsonrespdata["fastestFee"])
        halfhour = str(jsonrespdata["halfHourFee"])
        hour = str(jsonrespdata["hourFee"])
        return fastest, halfhour, hour
    else:
        print("CODE" + str(respurl.getcode()))
        print(respurl.read())
        return "RESPONSE CODE " + str(respurl.getcode()), "?", "?"

# Main routine ----------------------------------------------------------------

nextupdate = 0
btcpriceprovidermsg = 'None'

while True:
    # Force clear at beginning of loop
    fourletterphat.clear()

    # Check if time to get updated stats
    if (nextupdate < int(time.time())):
        mempool_usage, mempool_minfee, mempool_size, satfee, block_height = rpcinfo_from_node()
        # and pricing
        bitcoin_price, btcpriceprovidermsg = getbitcoinprice()
        # dont spam the rpc and api calls, this isn't a second by second price display
        if (minutes_between_api_updates < 1):
            minutes_between_api_updates = 10
        nextupdate = int(time.time()) + (60 * minutes_between_api_updates)

    # Panels ----------------------------------------------------------------------------

    # Welcome
    if (show_welcome == 1):
        message = "PI-0"
        scroll_message(message)

    # TIME
    if (show_time == 1):
        now = datetime.utcnow()
        thetime = now.strftime("%H%M")
        message = "TIME " + thetime
        scroll_message(message)

    # TEMP
    if (show_temp == 1):
        temperature = gettemp()
        message = "TEMP " + temperature
        scroll_message(message)

    # BITCOIN PRICE
    if (show_price == 1):
        message = "BITCOIN PRICE " + bitcoin_price
        scroll_message(message)
        if (show_pricemsg == 1):
            scroll_message(btcpriceprovidermsg)

    # BLOCK HEIGHT (bitcoin-cli getmininginfo blocks)
    if (show_blockheight == 1):
        message = "BLOCK HEIGHT " + block_height
        scroll_message(message)

    # MEMPOOL SIZE (bitcoin-cli getmempoolinfo usage)
    if (show_mempoolsize == 1):
        message = "MEMPOOL " + mempool_size + "MB"
        scroll_message(message)

    # MINIMUM FEE (bitcoin-cli getmempoolinfo mempoolminfee)
    if (show_minfee == 1):
        message = "MIN FEE " + satfee
        scroll_message(message)
        
    # RECOMMENDED FEE PER BYTE
    if (show_feerec == 1):
        lowfee = int(float(satfee) / 125)
        message = "SATS PER BYTE FOR NEXT BLOCK " + fee1
        scroll_message(message)
        message = "HALF HOUR " + fee2
        scroll_message(message)
        message = "IN AN HOUR " + fee3
        scroll_message(message)
        message = "MINIMUM FOR MEMPOOL " + str(lowfee)
        scroll_message(message)

    # Rest between iterations
    time.sleep(2)
