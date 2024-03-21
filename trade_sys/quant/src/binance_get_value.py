#!/usr/bin/env python
# encoding: utf-8

import requests
import talib
import numpy as np
import utils.utils as utils
import sched
import time
from binance_comm import *
from binance_util import callMe
from network_binance import request_urls_batch


symbolList = []
def getSpotSymbols():
    global symbolList
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(url)
    if response.status_code == 200:
        exchange_info = response.json()
        symbols = exchange_info['symbols']
        for symbol in symbols:
            if symbol["quoteAsset"] == "USDT":
                # BTCUSDT, ETHUSDT
                symbolList.append(symbol["symbol"])

def getMarketDealValues():
    global symbolList
    collectList = []
    for symbol in symbolList:
        symbolBase = symbol[:-4]

        if symbolBase in nonSpotSet or symbolBase in lowAmountSet or symbolBase in lowValueSet:
            continue

        if "UP" in symbolBase or "DOWN" in symbolBase:
            continue

        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=" + symbol
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # 日成交
            deal = int(float(data["quoteVolume"]))
            if deal > 50 * 1000 * 1000:
                collectList.append(symbolBase)

    collectList = sorted(collectList)
    print("total: ", len(collectList))

    for item in collectList:
        print(item)


if __name__ == "__main__":
    getSpotSymbols()
    getMarketDealValues()
