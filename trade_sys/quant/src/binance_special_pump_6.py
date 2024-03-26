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
    notifyInterval = 15 * 60
    # previous notify seconds
    if symbol in notifyDict:
        previousNotify = notifyDict[symbol]
    currentTime = int(time.time())
    if currentTime - previousNotify > notifyInterval:
        callSomeone(subject, content, PID_WENJIE)
        callSomeone(subject, content, PID_ZIYAN)
        notifyDict[symbol] = currentTime
        serialize.dump(notifyDict, serialNotifyFile)


def handleRspStrategy(symbol, kline15m, kline1h, kline4h, kline1d):
    symbolBase = symbol[:-4]

    latest = kline15m[-1]

    closes15m = np.array(loadClosePrice(kline15m))
    closes1h = np.array(loadClosePrice(kline1h))
    closes4h = np.array(loadClosePrice(kline4h))
    closes1d = np.array(loadClosePrice(kline1d))

    # 或者1小时ma25
    ma7_4h = talib.MA(closes4h, timeperiod=7, matype=0)
    ma5_4h = talib.MA(closes4h, timeperiod=5, matype=0)
    ma25 = talib.MA(closes1d, timeperiod=25, matype=0)
    ma99 = talib.MA(closes1d, timeperiod=99, matype=0)
    latestPrice = float(latest[HISTORY_CANDLES_CLOSE])
    diff7_4h = abs(latestPrice - ma7_4h[-1])
    diff5_4h = abs(latestPrice - ma5_4h[-1])
    diff25 = abs(latestPrice - ma25[-1])
    diff99 = abs(latestPrice - ma99[-1])
    diffPercentage7_4h = (float(diff7_4h) / float(latestPrice)) * 100
    diffPercentage5_4h = (float(diff5_4h) / float(latestPrice)) * 100
    diffPercentage25 = (float(diff25) / float(latestPrice)) * 100
    diffPercentage99 = (float(diff99) / float(latestPrice)) * 100
    diffThreshold = 5.0
    diffThreshold4h = 0.3

    global cnt

    coins_average_up = ["MATIC", "MEME", "NEXO", "OP", "RVN", "STORJ", "SUSHI", "TWT", "YFI", "ZEC", "MANTA", "MAGIC", "XTZ"]
    coins_acc_up = [""]
    coins_others = [""]
    COINS_UP_AVE = 0
    COINS_UP_ACC = 1
    COINS_UP_OTHERS = 2
    coins_up_type = COINS_UP_OTHERS
    if symbolBase in coins_average_up:
        coins_up_type = COINS_UP_AVE
    mac, macdsignal, macdhist = talib.MACD(closes1d, fastperiod=12, slowperiod=26, signalperiod=9)
    # 要观察突破4小时下跌趋势线
    if macdhist[-1] > macdhist[-2] and (abs(macdhist[-2]) / abs(macdhist[-1])) > 1.06 and (diffPercentage7_4h < diffThreshold4h): # or diffPercentage5_4h < diffThreshold4h):
        subject = symbolBase
        if coins_up_type == COINS_UP_AVE:
            subject += "(匀速币)"

        if diffPercentage25 < diffThreshold:
            subject += " 接近 MA25"
            content = symbolBase + " 接近 MA25, 乖离率" + format(diffPercentage25, ".2f") + "%"
            if coins_up_type == COINS_UP_AVE:
                notify(symbol, subject, content)
            formatPrint3(3, content)
            cnt += 1
        elif diffPercentage99 < diffThreshold:
            subject += " 接近 MA99"
            content = symbolBase + " 接近 MA99, 乖离率" + format(diffPercentage99, ".2f") + "%"
            if coins_up_type == COINS_UP_AVE:
                notify(symbol, subject, content)
            formatPrint3(2, content)
            cnt += 1
        elif diffPercentage99 > diffThreshold and latestPrice < ma99[-1]:
            subject += " 远离 MA99"
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
    interval = 10 * 60
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


















