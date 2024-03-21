#!/usr/bin/env python
# encoding: utf-8

# 新加坡的IP可以用

from binance_comm import *
import requests
import talib
import numpy as np
import utils.utils as utils
from binance_util import callMe
import sched
import time
from network_binance import request_urls_batch

# 大波动，需要在接近日线下方

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

def monitorMinutesAmp():
    global symbolList

    urls3m = []
    urls15m = []
    urls1d = []
    for symbol in symbolList:
        symbolBase = symbol[:-4]

        # print("symbol is: ", symbol)
        url3m = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=3m&limit=3"
        urls3m.append(url3m)
        url15m = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=15m&limit=3"
        urls15m.append(url15m)
        url1d = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1d&limit=10"
        urls1d.append(url1d)
        # url4h = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=4h&limit=100"

    # symbolList
    # batch request, rsp is ordered
    rsp3m = asyncio.run(request_urls_batch(urls3m))
    rsp15m = asyncio.run(request_urls_batch(urls15m))
    rsp1d = asyncio.run(request_urls_batch(urls1d))



    for i in range(0, len(symbolList)):
        symbol = symbolList[i]
        kline = eval(rsp3m[i][1])
        kline15m = eval(rsp15m[i][1])
        kline1d = eval(rsp1d[i][1])

        currentTime = int(time.time())

        index = -1
        # 3m
        open3 = np.array(loadOpenPrice(kline))[index]
        high3 = np.array(loadHighPrice(kline))[index]
        low3 = np.array(loadLowPrice(kline))[index]
        close3 = np.array(loadClosePrice(kline))[index]

        # 15m
        open15m = np.array(loadOpenPrice(kline15m))[index]
        high15m = np.array(loadHighPrice(kline15m))[index]
        low15m = np.array(loadLowPrice(kline15m))[index]
        close15m = np.array(loadClosePrice(kline15m))[index]

        # 1d
        closes1d = np.array(loadClosePrice(kline1d))
        ma7 = talib.MA(closes1d, timeperiod=7, matype=0)

        latestPrice = float(kline[-1][HISTORY_CANDLES_CLOSE])
        diff = abs(latestPrice - ma7[-1])
        diffPercentage = (float(diff) / float(latestPrice)) * 100
        diffThreshold = 2


        # 波动率异常仅在接近MA7时有效, 乖离率过高的瀑布可能是正常回调下跌
        if diffPercentage < diffThreshold:
            nkey = symbolBase + "3m"
            if shouldNotifyComm(symbolBase, currentTime, nkey):
                amb = abs(high3 - low3) / low3 * 100
                direction = "上涨" if close3 > open3 else "下跌"
                if amb > 1.2:
                    subject = symbolBase + " 3m " + direction + "异常, 波动率" + str(amb) + "%"
                    content = symbolBase + " 3m " + direction + "异常, 波动率" + str(amb) + "%"
                    notifyAndSetupComm(nkey, currentTime, subject, content)

            nkey15 = symbolBase + "15m"
            if shouldNotifyComm(symbolBase, currentTime, nkey15):
                amb15 = abs(high15m - low15m) / low15m * 100
                direction15m = "上涨" if close15m > open15m else "下跌"
                if amb15 > 3:
                    subject = symbolBase + " 15m " + direction15m + "异常, 波动率" + str(amb15) + "%"
                    content = symbolBase + " 15m " + direction15m + "异常, 波动率" + str(amb15) + "%"
                    notifyAndSetupComm(nkey15, currentTime, subject, content)

def schedule_func(scheduler):
    monitorMinutesAmp()
    interval = 30 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

if __name__ == "__main__":
    getSpotSymbols()

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()


