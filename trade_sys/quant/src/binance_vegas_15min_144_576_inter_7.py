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

serialNotifyFile = "binance_vegas_15min_144_576_inter_7"
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
    ema144 = talib.EMA(closes15m, timeperiod = 144)
    ema576 = talib.EMA(closes15m, timeperiod = 576)

    latestPrice = float(latest[HISTORY_CANDLES_CLOSE])

    diff144 = abs(latestPrice - ema144[-1])
    diff576 = abs(latestPrice - ema576[-1])
    diffPercentage1 = (float(diff144) / float(latestPrice)) * 100
    diffPercentage5 = (float(diff576) / float(latestPrice)) * 100

    if diffPercentage1 < 3 and diffPercentage5 < 3:
        # subject = symbolBase + " 接近 MA99"
        # content = symbolBase + " 接近 MA99, 乖离率" + format(diffPercentage99, ".2f") + "%"
        # notify(symbol, subject, content)
        formatPrint3(2, "find " + symbolBase)

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


















