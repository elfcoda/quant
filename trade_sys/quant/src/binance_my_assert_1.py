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
ASSERT_IDX_MACD_INC = 2
ASSERT_IDX_MACD_DEC = 3
myAsserts = {
            "BTC": [100, [31511.0], True, False],
            "OCEAN": [100, [1.42], False, False],
            "PEPE": [200, [0.00000830], False, False]
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

    # TODO
    # callMe(subject, content)
    notifyDict[nkey] = currentTime



def shouldNotify(symbolBase, notifyType, currentTime, nkey, notifyInterval = 1 * 60):
    global notifyDict

    previousNotify = 0
    # previous notify seconds
    if nkey in notifyDict:
        previousNotify = notifyDict[nkey]
    return currentTime - previousNotify > notifyInterval

def symbolMACD(symbolBase, price):
    symbol = symbolBase + "USDT"
    KLine1H = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1h&limit=100"

    response1h = requests.get(KLine1H)
    kline1h = eval(response1h.text)

    tss1h = np.array(loadTS(kline1h))
    opens1h = np.array(loadOpenPrice(kline1h))
    highs1h = np.array(loadHighPrice(kline1h))
    lows1h = np.array(loadLowPrice(kline1h))
    closes1h = np.array(loadClosePrice(kline1h))

    latestPrice = 1000000
    try:
        latestPrice = getLatestPrice(symbolBase)
    except requests.RequestException as e:
        print("请求异常:", e)


    mac, macdsignal, macdhist = talib.MACD(closes1h, fastperiod=12, slowperiod=26, signalperiod=9)
    # MACD down
    if macdhist[-1] <= macdhist[-2] and latestPrice > price:
        currentTime = int(time.time())
        nkey = getNotifyKey(symbolBase, NOTIFY_TYPE_MACD_DOWN_ABOVE_PRICE)
        if shouldNotify(symbolBase, NOTIFY_TYPE_MACD_DOWN_ABOVE_PRICE, currentTime, nkey):
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
            if shouldNotify(symbolBase, NOTIFY_TYPE_PRICE, currentTime, nkey):
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
        o3m = kline3m[-1][1]
        h3m = kline3m[-1][2]
        l3m = kline3m[-1][3]
        c3m = kline3m[-1][4]
        o15m = kline15m[-1][1]
        h15m = kline15m[-1][2]
        l15m = kline15m[-1][3]
        c15m = kline15m[-1][4]

        nkey = getNotifyKey(symbolBase, NOTIFY_TYPE_BIG_FALL_3M)
        if shouldNotify(symbolBase, NOTIFY_TYPE_BIG_FALL_3M, currentTime, nkey):
            amb = abs(h3m - l3m) / l3m * 100
            direction = "上涨" if c3m > o3m else "下跌"
            if amb > 1.2:
                subject = symbolBase + "3m " + direction + "异常, 波动率" + amb + "%"
                content = symbolBase + "3m " + direction + "异常, 波动率" + amb + "%"
                notifyAndSetup(nkey, currentTime, subject, content)

        nkey15 = getNotifyKey(symbolBase, NOTIFY_TYPE_BIG_FALL_15M)
        if shouldNotify(symbolBase, NOTIFY_TYPE_BIG_FALL_15M, currentTime, nkey15):
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
    for symbolBase in myAsserts:
        priceList = myAsserts[symbolBase][ASSERT_IDX_NOFITY_PRICES]
        buyPrice = myAsserts[symbolBase][ASSERT_IDX_BUY_PRICE]
        for price in priceList:
            monitorPrice(symbolBase, price, buyPrice)

        monitorMACD(symbolBase, price)

        # monitorNeedle(symbolBase)

        monitorMinutesAmp(symbolBase)


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

