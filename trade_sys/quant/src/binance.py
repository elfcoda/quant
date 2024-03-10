#!/usr/bin/env python
# encoding: utf-8

# 新加坡的IP可以用

import requests
import talib
import numpy as np
import utils.utils as utils
import subprocess
import sched
import time

HISTORY_CANDLES_TS = 0
HISTORY_CANDLES_OPEN = 1
HISTORY_CANDLES_HIGH = 2
HISTORY_CANDLES_LOW = 3
HISTORY_CANDLES_CLOSE = 4
HISTORY_CANDLES_VOL = 5

symbolList = []
notifyDict = {}

def callMe(subject, content):
    command = "osascript email.applescript '" + subject + "' '" + content + "'"
    output = subprocess.check_output(command, shell=True)
    print(output.decode('utf-8'))

def getSpotSymbols():
    global symbolList
    url = 'https://api.binance.com/api/v3/exchangeInfo'
    response = requests.get(url)
    if response.status_code == 200:
        exchange_info = response.json()
        symbols = exchange_info['symbols']
        for symbol in symbols:
            if symbol["quoteAsset"] == "USDT":
                # BTCUSDT, ETHUSDT
                symbolList.append(symbol["symbol"])


def loadColumn(li, idx):
    # int for timestamp and float for prices
    if idx == HISTORY_CANDLES_TS:
        return list(map(lambda item: int(item[idx]), li))
    else:
        return list(map(lambda item: float(item[idx]), li))

def loadVolume(li):
    return loadColumn(li, HISTORY_CANDLES_VOL)

def loadClosePrice(li):
    return loadColumn(li, HISTORY_CANDLES_CLOSE)

def loadOpenPrice(li):
    return loadColumn(li, HISTORY_CANDLES_OPEN)

def loadHighPrice(li):
    return loadColumn(li, HISTORY_CANDLES_HIGH)

def loadLowPrice(li):
    return loadColumn(li, HISTORY_CANDLES_LOW)

def loadTS(li):
    return loadColumn(li, HISTORY_CANDLES_TS)

def notify(symbol, subject, content):
    global notifyDict

    previousNotify = 0
    notifyInterval = 15 * 60
    # previous notify seconds
    if symbol in notifyDict:
        previousNotify = notifyDict[symbol]
    currentTime = int(time.time()))
    if currentTime - previousNotify > notifyInterval:
        callMe(subject, content):
        notifyDict[symbol] = currentTime


def getKlines():
    cnt = 0

    global symbolList
    for symbol in symbolList:
        cnt += 1
        if cnt == 200:
            return

        # print("symbol is: ", symbol)
        url = "https://data-api.binance.vision/api/v3/klines?symbol=" + symbol + "&interval=1d&limit=100"
        response = requests.get(url)
        kline = eval(response.text)

        # kline[-1] is the latest one
        # alert latest
        latest = kline[-1]
        amplitude = ((float(latest[HISTORY_CANDLES_HIGH]) / float(latest[HISTORY_CANDLES_LOW])) - 1) * 100
        if amplitude > 80.0:
            print("\033[31mamplitude: ", format(amplitude, ".2f"), "%\033[0m")

        for item in kline:
            time = utils.formatTS(item[0])
            item.append(time)
            # print(item)

        closes = np.array(loadClosePrice(kline))
        opens = np.array(loadOpenPrice(kline))
        highs = np.array(loadHighPrice(kline))
        lows = np.array(loadLowPrice(kline))

        # timeperiod=30 by default
        ma7 = talib.MA(closes, timeperiod=7, matype=0)
        # print("latest MA7: ", ma7[-1])
        ma25 = talib.MA(closes, timeperiod=25, matype=0)
        # print("latest MA25: ", ma25[-1])
        ma99 = talib.MA(closes, timeperiod=99, matype=0)
        # print("latest MA99: ", ma99[-1])

        # latest price
        latestPrice = float(latest[HISTORY_CANDLES_CLOSE])
        diff = latestPrice - ma7[-1]
        # print("latest price for ", symbol, ": ", latestPrice, ", diff: ", diff)

        diffPercentage = (float(diff) / float(latestPrice)) * 100
        diffThreshold = 0.1
        if diff > 0 and diffPercentage < diffThreshold:
            subject = symbol + " 接近MA7"
            content = symbol + " 接近MA7"
            # notify(symbol, subject, content)
            print(subject)
        elif diff <= 0:
            subject = symbol + " 低于MA7"
            content = symbol + " 低于MA7"
            # notify(symbol, subject, content)
            print(subject)

        # TODO: MACD
        # TODO: Exclude Insts

def func():
    print("called per min")

# timer, execute func() every interval seconds
def schedule_func(scheduler):
    getKlines()
    interval = 5 * 60
    scheduler.enter(interval, 1, schedule_func, (scheduler,))

if __name__ == "__main__":
    getSpotSymbols()

    # for symbol in symbolList:
    #     print(symbol)

    print("all: ", symbolList.__len__())

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, schedule_func, (scheduler,))
    scheduler.run()


