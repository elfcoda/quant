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

serialNotifyFile = "binance_ma99"
cnt = 0

notifyDict = {}
def notify(symbol, subject, content):
    global notifyDict

    previousNotify = 0
    notifyInterval = 30 * 60
    # previous notify seconds
    if symbol in notifyDict:
        previousNotify = notifyDict[symbol]
    currentTime = int(time.time())
    if currentTime - previousNotify > notifyInterval:
        # callSomeone(subject, content, PID_WENJIE)
        # callSomeone(subject, content, PID_ZIYAN)
        notifyDict[symbol] = currentTime
        serialize.dump(notifyDict, serialNotifyFile)

li1 = []
li2 = []
li3 = []
li4 = []
def addPrt(lv1, lv2, lv3, symbolBase, content):
    if symbolBase in lv1:
        li1.append("优先级1: " + content)
    elif symbolBase in lv2:
        li2.append("优先级2: " + content)
    elif symbolBase in lv3:
        li3.append("优先级3: " + content)
    else:
        li4.append("低优先级: " + content)

def forPrt():
    for it in li4:
        formatPrint3(0, it)
    for it in li3:
        formatPrint3(4, it)
    for it in li2:
        formatPrint3(3, it)
    for it in li1:
        formatPrint3(2, it)

def handleRspStrategy(symbol, kline15m, kline1h, kline4h, kline1d):
    symbolBase = symbol[:-4]

    latest = kline15m[-1]

    closes1h = np.array(loadClosePrice(kline1h))
    closes4h = np.array(loadClosePrice(kline4h))
    closes1d = np.array(loadClosePrice(kline1d))
    mac, macdsignal, macdhist4h = talib.MACD(closes4h, fastperiod=12, slowperiod=26, signalperiod=9)

    ma99 = talib.MA(closes1h, timeperiod=99, matype=0)
    # print("latest EMA144: ", ema144[-1])

    # latest price
    latestPrice = float(latest[HISTORY_CANDLES_CLOSE])

    diff99 = abs(latestPrice - ma99[-1])
    # print("latest price for ", symbol, ": ", latestPrice, ", diff: ", diff)

    diffPercentage = (float(diff99) / float(latestPrice)) * 100
    # 宽容度会大点

    # 买过的 绿色
    lv1 = [ "MEME", "ID", "INJ", "SUSHI", "DYM", "TWT", "SC", "GNO", "ARKM", "FTM", "MATIC", "XTZ", "FLOW", "GMX", "CRV", "MANTA", "DOT", "CKB", "SHIB"]
    # 匀速或者加速币 黄色
    lv2 = [ "AAVE", "ALGO", "APE", "ARKM", "ATOM", "AXS", "BAT", "CRV", "DYDX", "ETHFI", "NEXO", "OP", "RVN", "STORJ", "QKC",
           "QTUM", "ROSE", "SAND", "SUN", "LUNC", "MANA", "SHIB", "WIN", "XEM", "YFI", "ZEC"]
    # 其他潜力币 蓝色
    lv3 = [ "1INCH", "AAVE", "AI", "APE", "ATOM", "AXS", "BAT", "BEAMX", "BLUR", "BTC", "BTTC", "CHZ", "COMP", "CRV",
            "DASH", "DCR", "DOT", "DYDX", "EGLD", "ELF", "ENS", "EOS", "ETH", "FIL", "FLOW", "FTT", "FXS", "GAS", "GLM",
            "GLMR", "GNO", "HBAR", "ID", "IMX", "INJ", "IOTA", "JASMY", "JST", "JTO", "KAVA", "KLAY", "LDO", "LINK", "LRC",
            "MAGIC", "MANA", "MANTA", "MATIC", "MINA", "NEO", "ONE", "OP", "ORDI", "PEPE", "POWR", "QKC", "QTUM", "RPL", "SAND",
            "SEI", "SHIB", "STORJ", "STRK", "SUN", "SUSHI", "TFUEL", "THETA", "TRX", "TWT", "UNI", "VET", "WBETH", "WBTC", "WLD", "XAI",
            "XEM", "XLM", "XTZ", "YFI", "ZEC", "ZIL" ]


    global cnt
    if diffPercentage < 2 or latestPrice < ma99[-1]:
        cnt += 1
        subject = symbolBase + " 接近MA99"
        content = symbolBase + " 接近MA99"
        addPrt(lv1, lv2, lv3, symbolBase, content)


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

    forPrt()

    print("total: ", cnt)
    print("all crypto finished.")

# timer, execute func() every interval seconds
def schedule_func(scheduler):
    global li1
    global li2
    global li3
    global li4
    li1 = []
    li2 = []
    li3 = []
    li4 = []
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


















