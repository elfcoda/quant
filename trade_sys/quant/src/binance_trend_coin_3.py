#!/usr/bin/env python
# encoding: utf-8

# 新加坡的IP可以用

from binance_comm import *
from binance_util import *
import utils.serialize as serialize
import requests
import talib
import numpy as np
import utils.utils as utils
import sched
import time
import config
from network_binance import request_urls_batch
from ziyan import *
from wenjie import *

oneHour = 60 * 60
notifyDict = {}
notifySerialFile = "binance_trend_coin"

# hourLi: [2024, 3, 21, 0]
def fromHourList2TS(hourLi):
    return int(config.ConfigSingleton.getHourTS(hourLi[0], hourLi[1], hourLi[2], hourLi[3]) / 1000)

# def calcIncPerHour(price1, price2, pastHours):

def shouldNotify(symbolBase, currentTime):
    global notifyDict

    previousNotify = 0
    notifyInterval = 30 * 60
    # previous notify seconds
    if symbolBase in notifyDict:
        previousNotify = notifyDict[symbolBase]
    return currentTime - previousNotify > notifyInterval

def notifyAndSetup(symbolBase, currentTime, subject, content):
    global notifyDict

    print("点位提示: ", content)

    callSomeone(subject, content, PID_WENJIE)
    # callSomeone(subject, content, PID_ZIYAN)
    notifyDict[symbolBase] = currentTime
    serialize.dump(notifyDict, notifySerialFile)

def monitorTrends(trendCoins):
    for symbolBaseSuffix in trendCoins:
        symbolBase = symbolBaseSuffix[:-2]
        currentTime = int(time.time())
        p = trendCoins[symbolBaseSuffix]

        strategy_type = p[0]
        if strategy_type != STRATEGY_TREND:
            continue

        # In Seconds
        TS1 = fromHourList2TS(p[2])
        TS2 = fromHourList2TS(p[4])
        pastHours = int((TS2 - TS1) / oneHour )
        inc = (p[3] - p[1]) / pastHours

        pastHours2Now = int((currentTime - TS2) / oneHour )
        targetPrice = pastHours2Now * inc + p[3]

        try:
            latestPrice = getLatestPrice(symbolBase)
            print("latestPrice for ", symbolBase, ": ", latestPrice)
            diffPrice = abs(latestPrice - targetPrice)

            percentage = (diffPrice / targetPrice) * 100

            config_tp = p[5]
            prefix = "重要: " if config_tp == CFG_TYPE_GOOD else ""
            # print("target: ", targetPrice, ", latestPrice: ", latestPrice, ", pastHours2: ", pastHours2Now, ", currentTime: ", currentTime, ", inc: ", inc * 10000)
            if percentage < 0.5:
                if shouldNotify(symbolBase, currentTime):
                    subject = prefix + symbolBase + "已达趋势价格附近"
                    content = symbolBase + "最新价格: " + str(latestPrice)
                    notifyAndSetup(symbolBase, currentTime, subject, content)
        except requests.RequestException as e:
            print("请求异常:", e)

def schedule_func(scheduler):
    monitorTrends(trendCoinHour_WENJIE)
    monitorTrends(trendCoinHour_ZIYAN)
    interval = 5 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

def initDict():
    global notifyDict
    notifyDict = serialize.load(notifySerialFile)


if __name__ == "__main__":
    initDict()

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()




