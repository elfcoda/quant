#!/usr/bin/env python
# encoding: utf-8

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

serialNotifyFile = "binance_ema12_hour"
cnt = 0

notifyDict = {}
def notify(symbol, subject, content):
    global notifyDict

    previousNotify = 0
    notifyInterval = 30 * 60
    # previous notify seconds
    if symbol in notifyDict:
        previousNotify = notifyDict[symbol]
    currentTime = int(time.time())
    if currentTime - previousNotify > notifyInterval:
        # callSomeone(subject, content, PID_WENJIE)
        # callSomeone(subject, content, PID_ZIYAN)
        notifyDict[symbol] = currentTime
        serialize.dump(notifyDict, serialNotifyFile)

li1 = []
li2 = []
li3 = []
li4 = []
def addPrt(symbolBase, content):
    if symbolBase in lv1:
        li1.append("优先级1: " + content)
    elif symbolBase in lv2:
        li2.append("优先级2: " + content)
    elif symbolBase in lv3:
        li3.append("优先级3: " + content)
    else:
        li4.append("低优先级: " + content)

def forPrt():
    for it in li4:
        formatPrint3(0, it)
    for it in li3:
        formatPrint3(4, it)
    for it in li2:
        formatPrint3(3, it)
    for it in li1:
        formatPrint3(2, it)

def handleRspStrategy(symbol, kline15m, kline1h, kline4h, kline1d):
    symbolBase = symbol[:-4]

    latest = kline15m[-1]

    closes15m = np.array(loadClosePrice(kline15m))
    closes1h = np.array(loadClosePrice(kline1h))
    closes4h = np.array(loadClosePrice(kline4h))
    closes1d = np.array(loadClosePrice(kline1d))

    ema12 = talib.EMA(closes1h, timeperiod = 12)
    ema144 = talib.EMA(closes1h, timeperiod = 144)
    ma7 = talib.MA(closes1d, timeperiod=7, matype=0)
    # print("latest EMA144: ", ema144[-1])

    # latest price
    latestPrice = float(latest[HISTORY_CANDLES_CLOSE])

    diff144 = abs(latestPrice - ema144[-1])
    diff12 = abs(latestPrice - ema12[-1])
    diff7 = abs(latestPrice - ma7[-1])
    # print("latest price for ", symbol, ": ", latestPrice, ", diff: ", diff)

    diffPercentageVegas = (float(diff144) / float(latestPrice)) * 100
    diffPercentage12 = (float(diff12) / float(latestPrice)) * 100
    diffPercentage1d = (float(diff7) / float(latestPrice)) * 100
    # 宽容度会大点
    diffThreshold12 = 0.5
    diffThreshold1dGood = 3.5

    vegasSymbolList = getHighValueCoinsList()

    mac, macdsignal, macdhist = talib.MACD(closes15m, fastperiod=12, slowperiod=26, signalperiod=9)

    global cnt
    if macdhist[-1] > macdhist[-2]:   # 在上涨趋势里
        if diffPercentageVegas < 5 and diffPercentage1d < diffThreshold1dGood and latestPrice < ema12[-1]: # (diffPercentage12 < diffThreshold12 or latestPrice < ema12[-1]):
            cnt += 1
            subject = symbolBase + " 接近EMA12"
            content = symbolBase + " 接近EMA12"
            addPrt(symbolBase, content)
        elif diffPercentageVegas < 0.7:
            cnt += 1
            subject = symbolBase + " 接近EMA144"
            content = symbolBase + " 接近EMA144"
            addPrt(symbolBase, content)


def func():
    global cnt
    cnt = 0

    KLinesSideWriteFileName = "klines_side_write"
    [KLineList, rsp3m, rsp15m, rsp1h, rsp4h, rsp1d] = serialize.load(KLinesSideWriteFileName)
    for i in range(0, len(KLineList)):
        symbolBase = KLineList[i]
        kline15m = eval(rsp15m[i][1])
        kline1h = eval(rsp1h[i][1])
        kline4h = eval(rsp4h[i][1])
        kline1d = eval(rsp1d[i][1])
        handleRspStrategy(symbolBase + "USDT", kline15m, kline1h, kline4h, kline1d)

    forPrt()

    print("total: ", cnt)
    print("all crypto finished.")

# timer, execute func() every interval seconds
def schedule_func(scheduler):
    global li1
    global li2
    global li3
    global li4
    li1 = []
    li2 = []
    li3 = []
    li4 = []
    func()
    interval = 5 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

def initDict():
    # serialize.dump({}, serialNotifyFile)

    global notifyDict
    notifyDict = serialize.load(serialNotifyFile)


if __name__ == "__main__":
    initDict()

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()


















