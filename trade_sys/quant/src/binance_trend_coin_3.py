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

def calcIncPerDay(price1, price2, days):
    return (price2 - price1) / days

oneday = 24 * 60 * 60
notifyDict = {}

def shouldNotify(symbolBase, currentTime):
    global notifyDict

    previousNotify = 0
    notifyInterval = 1 * 60
    # previous notify seconds
    if symbolBase in notifyDict:
        previousNotify = notifyDict[symbolBase]
    return currentTime - previousNotify > notifyInterval

def notifyAndSetup(symbolBase, currentTime, subject, content):
    global notifyDict

    print(content)

    # TODO
    # callMe(subject, content)
    notifyDict[symbolBase] = currentTime

def monitorTrends():
    for symbolBase in neddleCoin:
        currentTime = int(time.time())
        p = neddleCoin[symbolBase]
        inc = calcIncPerDay(p[0], p[1], p[2])

        lastTS = int(config.ConfigSingleton.getDayTS(p[3], p[4], p[5]) / 1000)
        pastDays = int((currentTime - lastTS) / oneday )
        targetPrice = pastDays * inc + p[1]

        try:
            latestPrice = getLatestPrice(symbolBase)
            print("latestPrice for ", symbolBase, ": ", latestPrice)
            diffPrice = abs(latestPrice - targetPrice)

            percentage = (diffPrice / targetPrice) * 100

            if percentage < 0.5:
                if shouldNotify(symbolBase, currentTime):
                    subject = symbolBase + "已达趋势价格附近"
                    content = symbolBase + "最新价格: " + str(latestPrice)
                    notifyAndSetup(symbolBase, currentTime, subject, content)
        except requests.RequestException as e:
            print("请求异常:", e)

def schedule_func(scheduler):
    monitorTrends()
    interval = 30 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()




