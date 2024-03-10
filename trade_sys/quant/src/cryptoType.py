#!/usr/bin/env python
# encoding: utf-8

import okx.PublicData as PublicData
import okx.MarketData as MarketData
from config import ConfigSingleton
import talib
import numpy as np
import utils.utils as utils
# Download the helper library from https://www.twilio.com/docs/python/install
import os
import subprocess

HISTORY_CANDLES_TS = 0
HISTORY_CANDLES_OPEN = 1
HISTORY_CANDLES_HIGH = 2
HISTORY_CANDLES_LOW = 3
HISTORY_CANDLES_CLOSE = 4
HISTORY_CANDLES_VOL = 5
def loadColumn(li, idx):
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


def callMe():
    subject = "推送比特币"
    content = "最新价格趋势"

    command = "osascript email.applescript '" + subject + "' '" + content + "'"
    output = subprocess.check_output(command, shell=True)
    print(output.decode('utf-8'))


result = {}
def getInstDays():
    count = 0

    conf = ConfigSingleton()
    publicDataAPI = PublicData.PublicAPI(flag = conf.simu_mode)
    marketDataAPI = MarketData.MarketAPI(flag = conf.simu_mode)
    result = publicDataAPI.get_instruments(
        instType="SPOT"
        # instType="MARGIN"
    )
    data = result["data"]

    klineList = []
    for entry in data:
        print("instId: ", entry.instId)
        count += 1

        rsp = marketDataAPI.get_candlesticks(
            instId  = entry.instId,
            bar     = "1Dutc",
            # bar     = "5m",
            before  = ConfigSingleton.getDayTS("2023", "12", "12"),
            # after   = ConfigSingleton.getNow(),
            limit = "300",
        )
        dayline = rsp["data"]

        # alert latest
        alert = dayline[0]
        amplitude = ((float(alert[2]) / float(alert[3])) - 1) * 100
        if amplitude > 80.0:
            print("\033[31mamplitude: ", format(amplitude, ".2f"), "%\033[0m")

        # reverse to calculate talib
        dayline.reverse()

        for item in dayline:
            time = utils.formatTS(item[0])

            openPrice = item[1]
            highestPrice = item[2]
            lowestPrice = item[3]
            closePrice = item[4]

            ###
            # multiply = 100000
            # if float(openPrice) < 1.0:
            #     item[1] = str(float(item[1]) * multiply)
            #     item[2] = str(float(item[2]) * multiply)
            #     item[3] = str(float(item[3]) * multiply)
            #     item[4] = str(float(item[4]) * multiply)
            ###

            # 张
            volume = item[5]
            # 币
            volumeCcy = item[6]
            # USDT
            volumeCcyQuote = item[7]
            confirm = item[8]

            item.append(time)

            print(item)

        # dayline is for current dist
        closes = np.array(loadClosePrice(dayline))
        opens = np.array(loadOpenPrice(dayline))
        highs = np.array(loadHighPrice(dayline))
        lows = np.array(loadLowPrice(dayline))

        ma = talib.MA(closes, timeperiod=30, matype=0)
        print("MA: ", ma)

        klineList.append([dayline, 0, 0])

        break

    print("all inst cnt: ", data.__len__())
    print("watching count: ", count)
    return klineList

if __name__ == "__main__":
    getInstDays()
    # callMe()


