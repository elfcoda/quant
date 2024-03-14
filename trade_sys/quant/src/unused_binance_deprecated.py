#!/usr/bin/env python
# encoding: utf-8

# 新加坡的IP可以用

import requests
import talib
import numpy as np
import utils.utils as utils
import sched
import time
from binance_comm import *
from binance_util import callMe

aboveCnt = 0
belowCnt = 0

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


def notify(symbol, subject, content):
    global notifyDict

    previousNotify = 0
    notifyInterval = 15 * 60
    # previous notify seconds
    if symbol in notifyDict:
        previousNotify = notifyDict[symbol]
    currentTime = int(time.time())
    if currentTime - previousNotify > notifyInterval:
        callMe(subject, content)
        notifyDict[symbol] = currentTime

def calcAmplitude(o, h, l, c):
    # if c > o:
    #     return (h - l) / l * 100
    # else:
    #     return (h - l) / h * 100
    return (o - l) / o

def calcAmplitudeList(os, hs, ls, cs, symbolBase, tss):
    total = 0
    cnt = os.__len__()
    for idx in range(0, cnt):
        amp = calcAmplitude(os[idx], hs[idx], ls[idx], cs[idx])
        if amp > 3.0:
            total += 1
            timeStr = utils.formatTS(tss[idx])
            print(symbolBase, " big amp ", format(amp, ".2f"), "% in ", timeStr)

    if total != 0:
        print("total big amp: ", total)

def handleRsp(symbol, response, response1h):
    global aboveCnt
    global belowCnt

    symbolBase = symbol[:-4]

    kline = eval(response.text)
    kline1h = eval(response1h.text)

    # kline[-1] is the latest one
    # alert latest

    latest = kline[-1]
    amplitude = ((float(latest[HISTORY_CANDLES_HIGH]) / float(latest[HISTORY_CANDLES_LOW])) - 1) * 100
    if amplitude > 80.0:
        print("\033[31mamplitude: ", format(amplitude, ".2f"), "%\033[0m")

    for item in kline:
        time = utils.formatTS(item[0])
        item.append(time)
        # print(item)

    opens = np.array(loadOpenPrice(kline))
    highs = np.array(loadHighPrice(kline))
    lows = np.array(loadLowPrice(kline))
    closes = np.array(loadClosePrice(kline))

    # timeperiod=30 by default
    ma7 = talib.MA(closes, timeperiod=7, matype=0)
    # print("latest MA7: ", ma7[-1])
    ma25 = talib.MA(closes, timeperiod=25, matype=0)
    # print("latest MA25: ", ma25[-1])
    ma99 = talib.MA(closes, timeperiod=99, matype=0)
    # print("latest MA99: ", ma99[-1])

    # latest price
    latestPrice = float(latest[HISTORY_CANDLES_CLOSE])
    diff = abs(latestPrice - ma7[-1])
    # print("latest price for ", symbol, ": ", latestPrice, ", diff: ", diff)

    diffPercentage = (float(diff) / float(latestPrice)) * 100
    # 宽容度会大点
    diffThreshold = 2


    tss1h = np.array(loadTS(kline1h))
    opens1h = np.array(loadOpenPrice(kline1h))
    highs1h = np.array(loadHighPrice(kline1h))
    lows1h = np.array(loadLowPrice(kline1h))
    closes1h = np.array(loadClosePrice(kline1h))

    # mac, macdsignal, macdhist = talib.MACD(closes1h, fastperiod=12, slowperiod=26, signalperiod=9)
    # print("symbol: ", symbolBase)
    # print(closes1h[-2], " and ", closes1h[-1])
    # MACD up
    # if macdhist[-1] > macdhist[-2]:

    # calcAmplitudeList(opens1h, highs1h, lows1h, closes1h, symbolBase, tss1h)

    # 需要在小时初判断
    # if lows1h[-2] > lows1h[-3]:
    # 需要在小时结尾判断
    if lows1h[-1] > lows1h[-2]:
        # 可以挂插针单对这些币
        if diffPercentage < diffThreshold:
            # 优先做
            aboveCnt += 1
            subject = symbolBase + " 接近MA7"
            content = symbolBase + " 接近MA7"
            # notify(symbol, subject, content)
            formatPrint(MATypeAbove, symbolBase, subject)
        elif diff <= 0:
            # 次优先做
            belowCnt += 1
            subject = symbolBase + " 低于MA7"
            content = symbolBase + " 低于MA7"
            # notify(symbol, subject, content)
            formatPrint(MATypeBelow, symbolBase, subject)

def getFocus1HLines():
    print("TEST888")

def getFocus1HLines1():
    targetKLines = []

    print("TEST9")
    focusSet = getFocusSet()

    print("TEST1")
    for symbolBase in focusSet:
        symbol = symbolBase + "USDT"

        print("symbol is: ", symbol)
        url = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1d&limit=100"
        url1h = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1h&limit=100"
        # url4h = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=4h&limit=100"
        response = requests.get(url)
        response1h = requests.get(url1h)

        kline = eval(response.text)
        kline1h = eval(response1h.text)
        latest = kline[-1]

        opens = np.array(loadOpenPrice(kline))
        highs = np.array(loadHighPrice(kline))
        lows = np.array(loadLowPrice(kline))
        closes = np.array(loadClosePrice(kline))
        ma7 = talib.MA(closes, timeperiod=7, matype=0)

        opens1h = np.array(loadOpenPrice(kline1h))
        highs1h = np.array(loadHighPrice(kline1h))
        lows1h = np.array(loadLowPrice(kline1h))
        closes1h = np.array(loadClosePrice(kline1h))

        # latest price
        latestPrice = float(latest[HISTORY_CANDLES_CLOSE])
        diff = abs(latestPrice - ma7[-1])
        # print("latest price for ", symbol, ": ", latestPrice, ", diff: ", diff)

        diffPercentage = (float(diff) / float(latestPrice)) * 100
        # 宽容度会大点
        diffThreshold = 2

        # 可以挂插针单对这些币
        # 查看是否是在上升趋势
        if diffPercentage < diffThreshold:
            targetKLines.append([kline1h, 0, 0])
        elif diff <= 0:
            targetKLines.append([kline1h, 0, 0])

    return targetKLines


def getKlines():
    cnt = 0

    global symbolList
    global aboveCnt
    global belowCnt
    aboveCnt = 0
    belowCnt = 0

    focusSet = getFocusSet()

    for symbolBase in focusSet:
        symbol = symbolBase + "USDT"

        if symbolBase in nonSpotSet:
            continue

        cnt += 1
        if cnt == 500:
            return

        # print("symbol is: ", symbol)
        url = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1d&limit=100"
        url1h = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1h&limit=100"
        # url4h = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=4h&limit=100"
        response = requests.get(url)
        response1h = requests.get(url1h)

        handleRsp(symbol, response, response1h)

    print("aboveCnt: ", aboveCnt, ", belowCnt: ", belowCnt)


def func():
    print("called per min")

# timer, execute func() every interval seconds
def schedule_func(scheduler):
    getKlines()
    interval = 30 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

if __name__ == "__main__":
    getSpotSymbols()

    # getFocus1HLines()

    # for symbol in symbolList:
    #     print(symbol)

    print("all: ", symbolList.__len__())

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()


