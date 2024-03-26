#!/usr/bin/env python
# encoding: utf-8

# 新加坡的IP可以用

import requests
import talib
import utils.serialize as serialize
import numpy as np
import utils.utils as utils
import sched
import time
from datetime import datetime
from binance_comm import *
from binance_util import *
from network_binance import request_urls_batch
from all_coins import coins_wenjie, coins_ziyan
from high_value import getHighValueCoinsList
from wenjie import trendCoinHour_WENJIE
from ziyan import trendCoinHour_ZIYAN


# 不同的币种有不同的特性，有些币持续不断地涨，有些币经常横盘，有些币爆拉后暴跌，有些币喜欢插针

cnt = 0
firstRun = True
serialNotifyFile = "binance_vegas_5"

symbolList = []
notifyDict = {}

def notify(symbol, subject, content):
    global notifyDict

    previousNotify = 0
    notifyInterval = 6 * 60 * 60
    # previous notify seconds
    if symbol in notifyDict:
        previousNotify = notifyDict[symbol]
    currentTime = int(time.time())
    if currentTime - previousNotify > notifyInterval:
        callSomeone(subject, content, PID_WENJIE)
        callSomeone(subject, content, PID_ZIYAN)
        callSomeone(subject, content, PID_YOLANDA)
        notifyDict[symbol] = currentTime
        serialize.dump(notifyDict, serialNotifyFile)

def filterVegasCoins(configCoins):
    vegasSymbolBaseList = []

    for symbolIndex in configCoins:
        symbolBase = symbolIndex[:-2]
        p = configCoins[symbolIndex]
        if p[0] != STRATEGY_VEGAS:
            continue

        if len(p) >= 2 and p[1] == CFG_TYPE_GOOD:
            vegasSymbolBaseList.append(symbolBase)

    return vegasSymbolBaseList


def handleRspStrategy1(symbol, kline15m, kline1h, kline4h, kline1d):
    symbolBase = symbol[:-4]

    latest = kline15m[-1]

    closes15m = np.array(loadClosePrice(kline15m))
    closes1h = np.array(loadClosePrice(kline1h))
    closes4h = np.array(loadClosePrice(kline4h))
    closes1d = np.array(loadClosePrice(kline1d))

    ema15m144 = talib.EMA(closes15m, timeperiod = 144)
    ema15m169 = talib.EMA(closes15m, timeperiod = 169)

    ema144 = talib.EMA(closes1h, timeperiod = 144)
    ema169 = talib.EMA(closes1h, timeperiod = 169)
    ema576 = talib.EMA(closes1h, timeperiod = 576)
    ema676 = talib.EMA(closes1h, timeperiod = 676)
    ma7 = talib.MA(closes1d, timeperiod=7, matype=0)
    # print("latest EMA144: ", ema144[-1])

    # latest price
    latestPrice = float(latest[HISTORY_CANDLES_CLOSE])

    diff = abs(latestPrice - ema144[-1])

    ema576List = ["OP", "SKL"]
    ema15m144List = ["ETHFI"]
    if symbolBase in ema576List:
        diff = abs(latestPrice - ema576[-1])
    elif symbolBase in ema15m144List:
        diff = abs(latestPrice - ema15m144[-1])

    diff1d = abs(latestPrice - ma7[-1])
    # print("latest price for ", symbol, ": ", latestPrice, ", diff: ", diff)

    diffPercentageVegas = (float(diff) / float(latestPrice)) * 100
    diffPercentage1d = (float(diff1d) / float(latestPrice)) * 100
    # 宽容度会大点
    diffThreshold = 2.1
    diffThreshold1dNormal = 1.5
    diffThreshold1dGood = 3

    vegasSymbolList = filterVegasCoins(trendCoinHour_WENJIE)
    vegasSymbolList2 = filterVegasCoins(trendCoinHour_ZIYAN)
    vegasSymbolList.extend(vegasSymbolList2)

    mac, macdsignal, macdhist4h = talib.MACD(closes4h, fastperiod=12, slowperiod=26, signalperiod=9)

    global cnt
    if diffPercentageVegas < diffThreshold and ema144[-24] > ema576[-24]:
        needld_coin_list = ["WAVES", "ZIL"]
        subject = symbolBase + " 接近1H EMA144"
        if symbolBase in needld_coin_list:
            subject += "(插针币)"
        content = symbolBase + " 接近1H EMA144"
        if symbolBase in vegasSymbolList and diffPercentage1d < diffThreshold1dGood:
            # 接近日线的优质币
            subject = "精选Vegas币: " + subject
            # if not inSleepMode():
            notify(symbol, subject, content)
            formatPrint3(2, content)
        elif diffPercentage1d < diffThreshold1dNormal and macdhist4h[-1] > macdhist4h[-2] and (abs(macdhist4h[-2]) / abs(macdhist4h[-1])) > 1.067:
            # 接近日线
            subject = "普通Vegas币(接近日线): " + subject
            if not inSleepMode():
                notify(symbol, subject, content)
            formatPrint3(3, content)
        else:
            subject = "普通Vegas币: " + subject
            # notify(symbol, subject, content)
            formatPrint3(0, content)

        cnt += 1


def vegas():
    global cnt
    cnt = 0

    symbolBaseList = getHighValueCoinsList()

    urls15m = []
    urls1h = []
    urls4h = []
    urls1d = []
    KLineList = []
    for symbolBase in symbolBaseList:
        if symbolBase in nonSpotSet or "UP" in symbolBase or "DOWN" in symbolBase or symbolBase in lowAmountSet or symbolBase in lowValueSet:
            continue

        symbol = symbolBase + "USDT"

        KLineList.append(symbolBase)
        # print("symbol is: ", symbol)
        url15m = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=15m&limit=700"
        urls15m.append(url15m)
        # 1小时有700可以算EMA576和EMA676(最大1000)
        url1h = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1h&limit=700"
        urls1h.append(url1h)
        url4h = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=4h&limit=300"
        urls4h.append(url4h)
        url1d = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1d&limit=100"
        urls1d.append(url1d)

    # KLineList
    # batch request, rsp is ordered
    rsp15m = asyncio.run(request_urls_batch(urls15m))
    rsp1h = asyncio.run(request_urls_batch(urls1h))
    rsp4h = asyncio.run(request_urls_batch(urls4h))
    rsp1d = asyncio.run(request_urls_batch(urls1d))

    # side write for other strategies
    KLinesSideWriteFileName = "klines_side_write"
    serialize.dump([KLineList, rsp15m, rsp1h, rsp4h, rsp1d], KLinesSideWriteFileName)

    for i in range(0, len(KLineList)):
        symbolBase = KLineList[i]
        if symbolBase in vegas_excluded_list:
            continue

        kline15m = eval(rsp15m[i][1])
        kline1h = eval(rsp1h[i][1])
        kline4h = eval(rsp4h[i][1])
        kline1d = eval(rsp1d[i][1])
        handleRspStrategy1(symbolBase + "USDT", kline15m, kline1h, kline4h, kline1d)

    print("total: ", cnt)
    print("all crypto finished.")


# timer, execute func() every interval seconds
def schedule_func(scheduler):
    vegas()
    interval = 10 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

def initDict():
    global notifyDict
    notifyDict = serialize.load(serialNotifyFile)


if __name__ == "__main__":
    initDict()

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()


