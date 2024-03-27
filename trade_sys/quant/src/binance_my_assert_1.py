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

ASSERT_IDX_BUY_PRICE = 0
ASSERT_IDX_NOFITY_PRICES = 1
ASSERT_IDX_MACD_DOWN = 2
ASSERT_IDX_VEGAS_15 = 3
myAsserts = {
            # "FTM": [1.035, [1.11], False],
            # "MKR": [3090, [3233], False],
            # "SUI": [2.6, [], False],
            # "PEPE": [0.00000750, [0.0000076], False],
            # "FLOW": [1.433, [], True],
            # "XTZ": [1.363, [], True],
        }

NOTIFY_TYPE_PRICE = 0
NOTIFY_TYPE_MACD_DOWN_BELOW_PRICE = 1
NOTIFY_TYPE_MACD_DOWN_ABOVE_PRICE = 2
NOTIFY_TYPE_MACD_UP_BELOW_PRICE = 3
NOTIFY_TYPE_MACD_UP_ABOVE_PRICE = 4
NOTIFY_TYPE_BIG_FALL_3M = 5
NOTIFY_TYPE_BIG_FALL_15M = 6
notifyDict = {}
# notify for each coin for each notifyType
def getNotifyKey(symbolBase, notifyType):
    return symbolBase + "-" + str(notifyType)

def notifyAndSetup(nkey, currentTime, subject, content):
    global notifyDict

    print(content)

    callMe(subject, content)
    notifyDict[nkey] = currentTime



def shouldNotify(currentTime, nkey, notifyInterval = 10 * 60):
    global notifyDict

    previousNotify = 0
    # previous notify seconds
    if nkey in notifyDict:
        previousNotify = notifyDict[nkey]
    return currentTime - previousNotify > notifyInterval

def symbolMACD(symbolBase, monitorPrice):
    # monitorPrice不想监控就写0
    symbol = symbolBase + "USDT"
    KLineUrl = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=15m&limit=100"

    response = requests.get(KLineUrl)
    kline = eval(response.text)

    tss1h = np.array(loadTS(kline))
    closes = np.array(loadClosePrice(kline))

    latestPrice = 1000000
    try:
        latestPrice = getLatestPrice(symbolBase)
    except requests.RequestException as e:
        print("请求异常:", e)


    mac, macdsignal, macdhist = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
    # MACD down
    if macdhist[-1] <= macdhist[-2] and latestPrice > monitorPrice:
        currentTime = int(time.time())
        nkey = getNotifyKey(symbolBase, NOTIFY_TYPE_MACD_DOWN_ABOVE_PRICE)
        if shouldNotify(currentTime, nkey):
            subject = symbolBase + "MACD提示"
            content = symbolBase + "小时线MACD下降，并且最新价格在监控价格之上"
            notifyAndSetup(nkey, currentTime, subject, content)


def monitorPrice(symbolBase, price, buyPrice):
    try:
        latestPrice = getLatestPrice(symbolBase)

        diffPrice = abs(latestPrice - price)
        percentage = (diffPrice / price) * 100

        if percentage < 0.5:
            currentTime = int(time.time())
            nkey = getNotifyKey(symbolBase, NOTIFY_TYPE_PRICE)
            if shouldNotify(currentTime, nkey):
                subject = symbolBase + "监控点位提示"
                # 低于  高于 成本价
                content = symbolBase + "最新价格: " + str(latestPrice) + ", 已接近监控点位: " + str(price)
                if latestPrice > buyPrice:
                    content += ("。高于买入价格: " + str(buyPrice) + ", 请记得止盈。")
                else:
                    content += ("。低于买入价格: " + str(buyPrice) + ", 请记得止损或加仓。")
                notifyAndSetup(nkey, currentTime, subject, content)
    except requests.RequestException as e:
        print("请求异常:", e)


def monitorMACD(symbolBase, price):
    symbolMACD(symbolBase, price)

def monitorNeedle(symbolBase):
    pass

def monitorMinutesAmp(symbolBase):
    symbol = symbolBase + "USDT"
    url3m = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=3m&limit=3"
    url15m = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=15m&limit=3"
    try:
        response3m = requests.get(url3m)
        response15m = requests.get(url15m)

        kline3m = eval(response3m.text)
        kline15m = eval(response15m.text)

        currentTime = int(time.time())
        o3m = float(kline3m[-1][1])
        h3m = float(kline3m[-1][2])
        l3m = float(kline3m[-1][3])
        c3m = float(kline3m[-1][4])
        o15m = float(kline15m[-1][1])
        h15m = float(kline15m[-1][2])
        l15m = float(kline15m[-1][3])
        c15m = float(kline15m[-1][4])

        nkey = getNotifyKey(symbolBase, NOTIFY_TYPE_BIG_FALL_3M)
        if shouldNotify(currentTime, nkey):
            amb = abs(h3m - l3m) / l3m * 100
            direction = "上涨" if c3m > o3m else "下跌"
            if amb > 1.2:
                subject = symbolBase + "3m " + direction + "异常, 波动率" + amb + "%"
                content = symbolBase + "3m " + direction + "异常, 波动率" + amb + "%"
                notifyAndSetup(nkey, currentTime, subject, content)

        nkey15 = getNotifyKey(symbolBase, NOTIFY_TYPE_BIG_FALL_15M)
        if shouldNotify(currentTime, nkey15):
            amb15 = abs(h15m - l15m) / l15m * 100
            direction15m = "上涨" if c15m > o15m else "下跌"
            if amb15 > 3:
                subject = symbolBase + "15m " + direction15m + "异常, 波动率" + amb15 + "%"
                content = symbolBase + "15m " + direction15m + "异常, 波动率" + amb15 + "%"
                notifyAndSetup(nkey15, currentTime, subject, content)
    except requests.RequestException as e:
        print("请求异常:", e)

def monitorTrend(symbolBase):
    pass

def monitorAsserts():
    global myAsserts
    for symbolBase in myAsserts:
        buyPrice = myAsserts[symbolBase][ASSERT_IDX_BUY_PRICE]
        priceList = myAsserts[symbolBase][ASSERT_IDX_NOFITY_PRICES]
        for price in priceList:
            monitorPrice(symbolBase, price, buyPrice)

        isMonitorMACDDown = myAsserts[symbolBase][ASSERT_IDX_MACD_DOWN]
        if isMonitorMACDDown:
            monitorMACD(symbolBase, 0)

        # monitorNeedle(symbolBase)

        # monitorMinutesAmp(symbolBase)


    # url_wenjie = "https://raw.githubusercontent.com/elfcoda/conf/main/binance_asserts.py"
    # url_yolanda = "https://raw.githubusercontent.com/yooyolanda/the-big-short/main/conf.py"
    # url_ziyan = ""
    # urls = [url_wenjie, url_yolanda]

    # for url in urls:
    #     try:
    #         rsp = requests.get(url)
    #         conf = eval(rsp.text)
    #         email = conf["info"][0]
    #         phone = conf["info"][1]
    #         myAsserts = conf["sub"]

    #         for symbolBase in myAsserts:
    #             priceList = myAsserts[symbolBase][ASSERT_IDX_NOFITY_PRICES]
    #             buyPrice = myAsserts[symbolBase][ASSERT_IDX_BUY_PRICE]
    #             for price in priceList:
    #                 monitorPrice(symbolBase, price, buyPrice)

    #             # 暂时不需要判断MACD
    #             # monitorMACD(symbolBase, price)

    #             # monitorNeedle(symbolBase)

    #             monitorMinutesAmp(symbolBase)
    #     except Exception as e:
    #         print("发生异常:", e)
    #         callMe("FATAL: config error", "url: " + url + ", error: " + str(e))
    #         continue


def func():
    print("called per min")

# timer, execute func() every interval seconds
def schedule_func(scheduler):
    monitorAsserts()
    interval = 5 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()

