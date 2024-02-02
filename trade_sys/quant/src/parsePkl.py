#!/usr/bin/env python
# encoding: utf-8

import utils.serialize as serialize
import numpy as np
import talib
from marketData import genBars, instSet, barDict
from config import ConfigSingleton
conf = ConfigSingleton()

# checkSet = { "APE", "AVAX", "BCH", "BTC", "ENS", "EOS", "ETC", "ETH", "GMT", "LTC", "LUNA", "MATIC", "NEAR", "OKB", "OP", "ORDI", "SATS", "SOL", "TRB", "XRP" }
checkSet = { "ETC" }

HISTORY_CANDLES_TS = 0
HISTORY_CANDLES_OPEN = 1
HISTORY_CANDLES_HIGH = 2
HISTORY_CANDLES_LOW = 3
HISTORY_CANDLES_CLOSE = 4
HISTORY_CANDLES_VOL = 5

def loadHistory(coin, instID, bar):
    fileName = conf.marketDataFilePrefix + coin + "/" + instID + "-" + bar
    li = serialize.load(fileName)
    # for item in li:
    #     print(item)
    print("total: ", li.__len__())

    return li

# turn [["1.1", "2.2", "3.3"], ["4.4", "5.5", "6.6"]], 2 into [3.3, 6.6]
def loadColumn(li, idx):
    return list(map(lambda item: float(item[idx]), li))

def loadClosePrice(li):
    return loadColumn(li, HISTORY_CANDLES_CLOSE)

def loadOpenPrice(li):
    return loadColumn(li, HISTORY_CANDLES_OPEN)

def loadHighPrice(li):
    return loadColumn(li, HISTORY_CANDLES_HIGH)

def loadLowPrice(li):
    return loadColumn(li, HISTORY_CANDLES_LOW)

def validateOne(li, bar):
    cnt = li.__len__()
    interval = barDict[bar]

    print("cnt: ", cnt)

    result = True

    if cnt == 0:
        print("success, no data")
    elif cnt == 1:
        print("success, only 1 record")
    else:
        # validating logic
        for i in range(1, cnt):
            if int(li[i][HISTORY_CANDLES_TS]) - int(li[i - 1][HISTORY_CANDLES_TS]) != interval:
                print("error when validating for bar ", bar, ", time is ", li[i][HISTORY_CANDLES_TS], ", gap is ", int(li[i][HISTORY_CANDLES_TS]) - int(li[i - 1][HISTORY_CANDLES_TS]))
                result = False

    return result

def remediateHole():
    pass

def appendCandles():
    pass

def validate():
    bars = genBars()

    failCnt = 0
    for coin in checkSet:
        for bar in bars:
            print("validate coin ", coin, " for bar ", bar)
            li = loadHistory(coin, coin + "-USDT", bar)
            result = validateOne(li, bar)
            if result == False:
                failCnt += 1
                print("validate failed for ", coin, " with ", bar)
            else:
                print("validate succeeded for ", coin, " with ", bar)

    print("--------------summary--------------")
    print("failCnt: ", failCnt)
    print("--------------summary--------------")

def strategy1(li, start):
    # [buy, sell]
    return [5, 6]

patternFileName = "pkl/pattern/pattern.dict"

def analysePattern(li, opens, highs, lows, closes):
    getRange = 15
    results = talib.CDLDOJISTAR(opens, highs, lows, closes)
    print("debug pattern: ", results)
    pos = []
    neg = []
    for i in range(0, results.__len__()):
        leftIdx = 0 if (i - getRange < 0) else (i - getRange)
        rightIdx = i + getRange + 1
        if results[i] == 100:
            pos.append(li[leftIdx : rightIdx])
        elif results[i] == -100:
            neg.append(li[leftIdx : rightIdx])

    writeInPattern = { "pos": pos, "neg": neg }

    serialize.dump(writeInPattern, patternFileName)

def loadPattern(fileName = patternFileName):
    patternDict = serialize.load(fileName)
    for k in patternDict:
        print(k, ": ", patternDict[k])

    return patternDict


def ayalyse():
    coin = "BTC"
    latest = 500
    start = 100
    bar = "15m"
    li = loadHistory(coin, coin + "-USDT", bar)

    # handle this one
    li = li[-latest:]
    closes = np.array(loadClosePrice(li))
    opens = np.array(loadOpenPrice(li))
    highs = np.array(loadHighPrice(li))
    lows = np.array(loadLowPrice(li))
    print("closes: ", closes)

    analysePattern(li, opens, highs, lows, closes)

    res = strategy1(li, start)

    # stream_SMA, check dir(talib)
    sma = talib.SMA(closes)
    # MACD and analyse directly
    macd, macdsignal, macdhist = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
    # print("DIFF: ", macd)
    # print("DEA: ", macdsignal)
    ## print("STICK_MACD: ", macdhist)

def test():
    # get list
    return 1111

if __name__ == "__main__":
    # validate()
    ayalyse()


