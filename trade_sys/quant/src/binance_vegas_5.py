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
from high_value import getHighValueCoinsList, getAllCoinsList
from wenjie import trendCoinHour_WENJIE
from ziyan import trendCoinHour_ZIYAN


# 不同的币种有不同的特性，有些币持续不断地涨，有些币经常横盘，有些币爆拉后暴跌，有些币喜欢插针

cnt = 0
firstRun = True
serialNotifyFile = "binance_vegas_5"
tmpList = []

symbolList = []
notifyDict = {}
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

# [BTCUSDT] -> [BTC]
def symbolList2symbolBaseList(sl):
    return list(map(lambda symbol: symbol[:-4], sl))

def notify2(symbol, subject, content):
    global notifyDict

    previousNotify = 0
    notifyInterval = 6 * 60 * 60
    # previous notify seconds
    if symbol in notifyDict:
        previousNotify = notifyDict[symbol]
    currentTime = int(time.time())
    if currentTime - previousNotify > notifyInterval:
        callSomeone(subject, content, PID_WENJIE)
        callSomeone(subject, content, PID_YOLANDA)
        notifyDict[symbol] = currentTime
        serialize.dump(notifyDict, serialNotifyFile)

def notify(symbol, subject, content):
    global notifyDict

    previousNotify = 0
    notifyInterval = 6 * 60 * 60
    # previous notify seconds
    if symbol in notifyDict:
        previousNotify = notifyDict[symbol]
    currentTime = int(time.time())
    if currentTime - previousNotify > notifyInterval:
        # callSomeone(subject, content, PID_WENJIE)
        # callSomeone(subject, content, PID_ZIYAN)
        # callSomeone(subject, content, PID_YOLANDA)
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

nLi = []
nLiLow = []
def addFor(symbolBase, tp, content):
    global nLi
    global nLiLow
    if symbolBase in lowValuesCoins:
        nLiLow.append([1, content, symbolBase])
    else:
        nLi.append([tp, content, symbolBase])

def prtFot():
    global nLi
    global nLiLow
    for item in nLi:
        formatPrint3(item[0], item[1])

    dumpTmp = []
    for item in nLiLow:
        formatPrint3(item[0], item[1])
        dumpTmp.append(item[2])

    serialize.dump(dumpTmp, "dumpTmp_UI")

def handleRspStrategy1(symbol, kline3m, kline15m, kline1h, kline4h, kline1d):
    symbolBase = symbol[:-4]

    latest = kline15m[-1]

    closes3m = np.array(loadClosePrice(kline3m))
    closes15m = np.array(loadClosePrice(kline15m))
    closes1h = np.array(loadClosePrice(kline1h))
    closes4h = np.array(loadClosePrice(kline4h))
    closes1d = np.array(loadClosePrice(kline1d))

    ema15m144 = talib.EMA(closes15m, timeperiod = 144)
    ema15m169 = talib.EMA(closes15m, timeperiod = 169)

    ema1h_30 = talib.EMA(closes1h, timeperiod = 30)
    ema144 = talib.EMA(closes1h, timeperiod = 144)
    ema169 = talib.EMA(closes1h, timeperiod = 169)
    ema576 = talib.EMA(closes1h, timeperiod = 576)
    ema676 = talib.EMA(closes1h, timeperiod = 676)
    ma7 = talib.MA(closes1d, timeperiod=7, matype=0)
    # print("latest EMA144: ", ema144[-1])

    # latest price
    latestPrice = float(latest[HISTORY_CANDLES_CLOSE])

    diff = abs(latestPrice - ema144[-1])

    ema576List = ["OP", "SKL", "ACA"]
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
    diffThreshold = 2.8
    diffThreshold1dNormal = 20
    diffThreshold1dGood = 30

    vegasSymbolList = filterVegasCoins(trendCoinHour_WENJIE)
    vegasSymbolList2 = filterVegasCoins(trendCoinHour_ZIYAN)
    vegasSymbolList.extend(vegasSymbolList2)

    mac4h, macdsignal4h, macdhist4h = talib.MACD(closes4h, fastperiod=12, slowperiod=26, signalperiod=9)
    mac1h, macdsignal1h, macdhist1h = talib.MACD(closes1h, fastperiod=12, slowperiod=26, signalperiod=9)
    mac15m, macdsignal15m, macdhist15m = talib.MACD(closes15m, fastperiod=12, slowperiod=26, signalperiod=9)

    #######TODO VegasInlowValuesCoins = []

    global cnt
    global tmpList
    # 刚跌完，去除此条件
    # and ema144[-2] > ema576[-2]
    # 观察是否突破趋势
    if diffPercentageVegas < diffThreshold:
        tmpList.append(symbolBase)
        subject = symbolBase + " 接近1H EMA144 偏离" + format(diffPercentageVegas, ".2f") + "%"
        content = symbolBase + " 接近1H EMA144 偏离" + format(diffPercentageVegas, ".2f") + "%。"
        # if macdhist15m[-1] > macdhist15m[-2] or macdhist15m[-1] > 0:
        #     content += "15m 线已止跌或启动。"
        if macdhist1h[-1] > macdhist1h[-2] or macdhist1h[-1] > 0:
            content += "1h 线已止跌或启动。"
        # if isInTrendUp(ema1h_30):
        #     content += "(趋势向上)"

        # special PEPE
        if symbolBase == "PEPE":
            s = "PEPE 接近1H EMA144, Vegas偏离" + format(diffPercentageVegas, ".2f") + "%"
            notify2(symbol, s, s)

        elif symbolBase in vegasSymbolList and diffPercentage1d < diffThreshold1dGood and (macdhist1h[-1] > macdhist1h[-2] or macdhist1h[-1] > 0):
            # 接近日线的优质币
            subject = "精选Vegas币: " + subject
            # if not inSleepMode():
            notify(symbol, subject, content)
            addFor(symbolBase, 2, content)
        elif diffPercentage1d < diffThreshold1dNormal and (macdhist1h[-1] > macdhist1h[-2] or macdhist1h[-1] > 0): # and macdhist1h[-1] > macdhist1h[-2] and (abs(macdhist1h[-2]) / abs(macdhist1h[-1])) > 1.067:
            # 接近日线
            subject = "普通Vegas币(接近日线): " + subject
            # if not inSleepMode():
            notify(symbol, subject, content)
            addFor(symbolBase, 3, content)
        else:
            subject = "普通Vegas币: " + subject
            notify(symbol, subject, content)
            addFor(symbolBase, 4, content)

        cnt += 1


def vegas():
    global cnt
    cnt = 0

    symbolBaseList = getAllCoinsList()
    print("total coins: ", len(symbolBaseList))

    # 临时改成做所有币种
    global symbolList

    urls3m = []
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
        url3m = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=3m&limit=200"
        urls3m.append(url3m)
        url15m = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=15m&limit=700"
        urls15m.append(url15m)
        # 1小时有700可以算EMA576和EMA676(最大1000)
        url1h = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1h&limit=700"
        urls1h.append(url1h)
        url4h = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=4h&limit=300"
        urls4h.append(url4h)
        url1d = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1d&limit=100"
        urls1d.append(url1d)

    print("downloading...")
    # KLineList
    # batch request, rsp is ordered
    rsp3m = asyncio.run(request_urls_batch(urls3m))
    rsp15m = asyncio.run(request_urls_batch(urls15m))
    rsp1h = asyncio.run(request_urls_batch(urls1h))
    rsp4h = asyncio.run(request_urls_batch(urls4h))
    rsp1d = asyncio.run(request_urls_batch(urls1d))
    print("downloaded")

    # side write for other strategies
    KLinesSideWriteFileName = "klines_side_write"
    serialize.dump([KLineList, rsp3m, rsp15m, rsp1h, rsp4h, rsp1d], KLinesSideWriteFileName)

    for i in range(0, len(KLineList)):
        symbolBase = KLineList[i]
        if symbolBase in vegas_excluded_list:
            continue

        kline3m = eval(rsp3m[i][1])
        kline15m = eval(rsp15m[i][1])
        kline1h = eval(rsp1h[i][1])
        kline4h = eval(rsp4h[i][1])
        kline1d = eval(rsp1d[i][1])
        handleRspStrategy1(symbolBase + "USDT", kline3m, kline15m, kline1h, kline4h, kline1d)

    prtFot()
    print("total: ", cnt)
    serialize.dump(tmpList, "vegas_UI")
    print("all crypto finished.")


# timer, execute func() every interval seconds
def schedule_func(scheduler):
    global tmpList
    global nLi
    global nLiLow
    tmpList = []
    nLi = []
    nLiLow = []
    vegas()
    interval = 10 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

def initDict():
    # serialize.dump({}, serialNotifyFile)

    global notifyDict
    notifyDict = serialize.load(serialNotifyFile)


if __name__ == "__main__":
    initDict()

    getSpotSymbols()

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()


