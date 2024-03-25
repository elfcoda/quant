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

serialNotifyFile = "binance_special_pump"
cnt = 0

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
        # callSomeone(subject, content, PID_WENJIE)
        # callSomeone(subject, content, PID_ZIYAN)
        notifyDict[symbol] = currentTime
        serialize.dump(notifyDict, serialNotifyFile)


def handleRspStrategy(symbol, kline15m, kline1h, kline4h, kline1d):
    symbolBase = symbol[:-4]

    latest = kline15m[-1]

    closes15m = np.array(loadClosePrice(kline15m))
    closes1h = np.array(loadClosePrice(kline1h))
    closes4h = np.array(loadClosePrice(kline4h))
    closes1d = np.array(loadClosePrice(kline1d))

    ma25 = talib.MA(closes1d, timeperiod=25, matype=0)
    ma99 = talib.MA(closes1d, timeperiod=99, matype=0)
    latestPrice = float(latest[HISTORY_CANDLES_CLOSE])
    diff25 = abs(latestPrice - ma25[-1])
    diff99 = abs(latestPrice - ma99[-1])
    diffPercentage25 = (float(diff25) / float(latestPrice)) * 100
    diffPercentage99 = (float(diff99) / float(latestPrice)) * 100
    diffThreshold = 5.0

    global cnt
    mac, macdsignal, macdhist = talib.MACD(closes1d, fastperiod=12, slowperiod=26, signalperiod=9)
    # 要观察突破4小时下跌趋势线
    if macdhist[-1] > macdhist[-2] and (abs(macdhist[-2]) / abs(macdhist[-1])) > 1.06:
        if diffPercentage25 < diffThreshold:
            subject = symbolBase + " 接近 MA25"
            content = symbolBase + " 接近 MA25, 乖离率" + format(diffPercentage25, ".2f") + "%"
            # notify(symbol, subject, content)
            formatPrint3(3, content)
            cnt += 1
        elif diffPercentage99 < diffThreshold:
            subject = symbolBase + " 接近 MA99"
            content = symbolBase + " 接近 MA99, 乖离率" + format(diffPercentage99, ".2f") + "%"
            # notify(symbol, subject, content)
            formatPrint3(2, content)
            cnt += 1
        elif diffPercentage99 > diffThreshold and latestPrice < ma99[-1]:
            subject = symbolBase + " 远离 MA99"
            content = symbolBase + " 远离 MA99, 乖离率" + format(diffPercentage99, ".2f") + "%"
            # notify(symbol, subject, content)
            formatPrint3(1, content)
            cnt += 1


def func():
    global cnt
    cnt = 0

    KLinesSideWriteFileName = "klines_side_write"
    [KLineList, rsp15m, rsp1h, rsp4h, rsp1d] = serialize.load(KLinesSideWriteFileName)
    for i in range(0, len(KLineList)):
        symbolBase = KLineList[i]
        kline15m = eval(rsp15m[i][1])
        kline1h = eval(rsp1h[i][1])
        kline4h = eval(rsp4h[i][1])
        kline1d = eval(rsp1d[i][1])
        handleRspStrategy(symbolBase + "USDT", kline15m, kline1h, kline4h, kline1d)

    print("total: ", cnt)
    print("all crypto finished.")

# timer, execute func() every interval seconds
def schedule_func(scheduler):
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


















