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
from high_value import getHighValueCoinsList, getAllCoinsList
from wenjie import trendCoinHour_WENJIE
from ziyan import trendCoinHour_ZIYAN

serialNotifyFile = "binance_high_amp_among_all"
cnt = 0
dumpList = []
oldPrice = {}

notifyDict = {}
def notify(symbol, subject, content):
    global notifyDict

    previousNotify = 0
    notifyInterval = 5 * 60
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

def handleRspStrategy(symbol, kline3m, kline15m, kline1h, kline4h, kline1d):
    symbolBase = symbol[:-4]

    open1h = np.array(loadOpenPrice(kline1h))[-1]
    close1h = np.array(loadClosePrice(kline1h))[-1]
    open1h2 = np.array(loadOpenPrice(kline1h))[-2]
    close1h2 = np.array(loadClosePrice(kline1h))[-2]
    open1h3 = np.array(loadOpenPrice(kline1h))[-3]
    close1h3 = np.array(loadClosePrice(kline1h))[-3]

    amp = (float(close1h) - float(open1h)) / open1h * 100
    amp2 = (float(close1h2) - float(open1h2)) / open1h2 * 100
    amp3 = (float(close1h3) - float(open1h3)) / open1h3 * 100

    # 对比前n个小时跌幅
    n = 3
    open1h_n = np.array(loadOpenPrice(kline1h))[-n]
    global oldPrice
    oldPrice[symbolBase] = open1h_n


def initPrice():
    global cnt
    cnt = 0

    KLinesSideWriteFileName = "klines_side_write"
    [KLineList, rsp3m, rsp15m, rsp1h, rsp4h, rsp1d] = serialize.load(KLinesSideWriteFileName)
    for i in range(0, len(KLineList)):
        symbolBase = KLineList[i]
        kline3m = eval(rsp3m[i][1])
        kline15m = eval(rsp15m[i][1])
        kline1h = eval(rsp1h[i][1])
        kline4h = eval(rsp4h[i][1])
        kline1d = eval(rsp1d[i][1])
        handleRspStrategy(symbolBase + "USDT", kline3m, kline15m, kline1h, kline4h, kline1d)

ampDict = {}
def func():
    global oldPrice
    global ampDict
    ampDict = {}
    for symbolBase in oldPrice:
        price = oldPrice[symbolBase]
        latestPrice = getLatestPrice(symbolBase)
        amp_n = (float(latestPrice) - float(price)) / price * 100
        ampDict[amp_n] = symbolBase

    allCoinsLi = getAllCoinsList()
    ampList = sorted(ampDict.items())

    excludedCoins = ["REI", "RAD"]
    cnt = 0
    for pa in ampList:
        pa_amp = pa[0]
        pa_symbol_base = pa[1]

        if pa_symbol_base in excludedCoins:
            continue

        if pa_symbol_base in allCoinsLi:
            cnt += 1
            if cnt > 30:
                print("scan completed.")
                return

            formatPrint3(2, pa_symbol_base + "跌幅: " + format(pa_amp, ".2f"))



# timer, execute func() every interval seconds
def schedule_func(scheduler):
    global li1
    global li2
    global li3
    global li4
    global dumpList
    li1 = []
    li2 = []
    li3 = []
    li4 = []
    dumpList = []
    func()
    interval = 5 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

def initDict():
    # serialize.dump({}, serialNotifyFile)

    global notifyDict
    notifyDict = serialize.load(serialNotifyFile)


if __name__ == "__main__":
    initDict()

    initPrice()

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()




