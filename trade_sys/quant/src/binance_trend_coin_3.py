#!/usr/bin/env python
# encoding: utf-8

# 新加坡的IP可以用

from binance_comm import *
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

def calcIncPerHour(price1, price2, hours):
    return (price2 - price1) / hours

oneHour = 60 * 60
notifyDict = {}

def shouldNotify(symbolBase, currentTime):
    global notifyDict

    previousNotify = 0
    notifyInterval = 60 * 60
    # previous notify seconds
    if symbolBase in notifyDict:
        previousNotify = notifyDict[symbolBase]
    return currentTime - previousNotify > notifyInterval

def notifyAndSetup(symbolBase, currentTime, subject, content):
    global notifyDict

    print("点位提示: ", content)

    # callMe(subject, content)
    notifyDict[symbolBase] = currentTime

# 按分钟计算
def monitorTrends(trendCoins):
    for symbolBaseSuffix in trendCoins:
        symbolBase = symbolBaseSuffix[:-2]
        currentTime = int(time.time())
        p = trendCoins[symbolBaseSuffix]
        inc = calcIncPerHour(p[0], p[1], p[2])

        lastTS = int(config.ConfigSingleton.getHourTS(p[3], p[4], p[5], p[6]) / 1000)
        pastHours = int((currentTime - lastTS) / oneHour )
        targetPrice = pastHours * inc + p[1]

        try:
            latestPrice = getLatestPrice(symbolBase)
            print("latestPrice for ", symbolBase, ": ", latestPrice)
            diffPrice = abs(latestPrice - targetPrice)

            percentage = (diffPrice / targetPrice) * 100

            # print("target: ", targetPrice, ", latestPrice: ", latestPrice, ", pastHours: ", pastHours, ", currentTime: ", currentTime, ", lastTS: ", lastTS, ", inc: ", inc * 10000)
            if percentage < 1.5:
                if shouldNotify(symbolBase, currentTime):
                    subject = symbolBase + "已达趋势价格附近"
                    content = symbolBase + "最新价格: " + str(latestPrice)
                    notifyAndSetup(symbolBase, currentTime, subject, content)
        except requests.RequestException as e:
            print("请求异常:", e)

def schedule_func(scheduler):
    monitorTrends(trendCoinHour_WENJIE)
    monitorTrends(trendCoinHour_ZIYAN)
    interval = 5 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()




