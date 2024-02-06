#!/usr/bin/env python
# encoding: utf-8

import utils.serialize as serialize
import utils.utils as utils
import numpy as np
import talib
from marketData import genBars, instSet, barDict
from config import ConfigSingleton
conf = ConfigSingleton()

# checkSet = { "APE", "AVAX", "BCH", "BTC", "ENS", "EOS", "ETC", "ETH", "GMT", "LTC", "LUNA", "MATIC", "NEAR", "OKB", "OP", "ORDI", "SATS", "SOL", "TRB", "XRP" }
checkSet = { "ETC" }

margin = 15

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

def loadTS(li):
    return loadColumn(li, HISTORY_CANDLES_TS)

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

ACTION_SIDELINES = 0
ACTION_LONG = 1
ACTION_SHORT = 2
ACTION_CLOSE_LONG = 3
ACTION_CLOSE_SHORT = 4
ACTION_CLOSE_LONG_AND_SHORT = 5
ACTION_CLOSE_SHORT_AND_LONG = 6
STATE_SIDELINES = 0
STATE_LONG = 1
STATE_SHORT = 2
###
ACTION_LONG_ADD_POS = 100
ACTION_LONG_REDUCE_POS = 101
ACTION_SHORT_ADD_POS = 102
ACTION_SHORT_REDUCE_POS = 103

unstableCnt = 0
def strategy(li, opens, highs, lows, closes, previousState):
    global unstableCnt

    if not hasattr(strategy, "fstCall"):
        strategy.fstCall = True
    else:
        strategy.fstCall = False

    macd, macdsignal, macdhist = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
    # print("DIFF: ", macd)
    # print("DEA: ", macdsignal)
    # print("STICK_MACD: ", macdhist)
    if macdhist[-1] > macdhist[-2]:
        if STATE_SIDELINES == previousState:
            return ACTION_LONG
        elif STATE_LONG == previousState:
            return ACTION_SIDELINES
        elif STATE_SHORT == previousState:
            return ACTION_CLOSE_SHORT
    elif macdhist[-1] < macdhist[-2]:
        if STATE_SIDELINES == previousState:
            return ACTION_SHORT
        elif STATE_LONG == previousState:
            return ACTION_CLOSE_LONG
        elif STATE_SHORT == previousState:
            return ACTION_SIDELINES
    else:
        return ACTION_SIDELINES


    # stream_SMA, check dir(talib)
    # sma = talib.SMA(closes)

    return ACTION_SIDELINES

def genList(li, start, end):
    m = start - margin
    l = 0 if m < 0 else m
    r = end + margin + 1
    markIdx = start if start <= margin else margin
    return [li[l : r], markIdx, markIdx + (end - start)]


def summary():
    pass

analyseFileName = "pkl/analyse/analyse.dict"
def trade(li, opens, highs, lows, closes, start):
    # analysePattern(li, opens, highs, lows, closes)

    total = 0
    win = 0
    totalEarn = 0
    # x100
    multiple = 100
    # base 100$
    base = 100

    writeInLong = []
    writeInShort = []

    idx = li.__len__() - 1
    curr = start

    sli = li[: curr + 1]
    sopens = opens[: curr + 1]
    shighs = highs[: curr + 1]
    slows = lows[: curr + 1]
    scloses = closes[: curr + 1]

    previousState = STATE_SIDELINES
    previousPrice = 0
    previousPos = 0
    while (curr <= idx):
        action = strategy(sli, sopens, shighs, slows, scloses, previousState)
        print("action: ", action, " in position ", curr, ", price ", closes[curr], ", sticks size: ", scloses.size, ", time: ", utils.formatTS(li[curr][HISTORY_CANDLES_TS]))

        if ACTION_SIDELINES == action:
            print("do nothing!")

        elif ACTION_LONG == action and STATE_SIDELINES == previousState:
            previousState = STATE_LONG

            previousPrice = closes[curr]
            previousPos = curr

        elif ACTION_SHORT == action and STATE_SIDELINES == previousState:
            previousState = STATE_SHORT

            previousPrice = closes[curr]
            previousPos = curr

        elif ACTION_CLOSE_LONG == action and STATE_LONG == previousState:
            previousState = STATE_SIDELINES

            diff = closes[curr] - previousPrice
            percentage = diff / previousPrice * 100
            earn = base * percentage / 100 * multiple
            print("buy ", previousPos, " with price ", previousPrice, " and sell ", curr, " with price ", closes[curr])
            print("diff ", diff, "$, percentage ", percentage, "%, using ", base, "$, earn ", earn, "$")

            total += 1
            win = win + 1 if diff > 0 else win
            totalEarn += earn
            writeInLong.append(genList(li, previousPos, curr))

        elif ACTION_CLOSE_SHORT == action and STATE_SHORT == previousState:
            previousState = STATE_SIDELINES

            diff = previousPrice - closes[curr]
            percentage = diff / previousPrice * 100
            earn = base * percentage / 100 * multiple
            print("sell ", previousPos, " with price ", previousPrice, " and buy ", curr, " with price ", closes[curr])
            print("diff ", diff, "$, percentage ", percentage, "%, using ", base, "$, earn ", earn, "$")

            total += 1
            win = win + 1 if diff > 0 else win
            totalEarn += earn
            writeInShort.append(genList(li, previousPos, curr))

        elif ACTION_CLOSE_LONG_AND_SHORT == action and STATE_LONG == previousState:
            previousState = STATE_SHORT

            diff = closes[curr] - previousPrice
            percentage = diff / previousPrice * 100
            earn = base * percentage / 100 * multiple
            print("buy ", previousPos, " with price ", previousPrice, " and sell ", curr, " with price ", closes[curr])
            print("diff ", diff, "$, percentage ", percentage, "%, using ", base, "$, earn ", earn, "$")

            total += 1
            win = win + 1 if diff > 0 else win
            totalEarn += earn
            writeInLong.append(genList(li, previousPos, curr))

            previousPrice = closes[curr]
            previousPos = curr

        elif ACTION_CLOSE_SHORT_AND_LONG == action and STATE_SHORT == previousState:
            previousState = STATE_LONG

            diff = previousPrice - closes[curr]
            percentage = diff / previousPrice * 100
            earn = base * percentage / 100 * multiple
            print("sell ", previousPos, " with price ", previousPrice, " and buy ", curr, " with price ", closes[curr])
            print("diff ", diff, "$, percentage ", percentage, "%, using ", base, "$, earn ", earn, "$")

            total += 1
            win = win + 1 if diff > 0 else win
            totalEarn += earn
            writeInShort.append(genList(li, previousPos, curr))

            previousPrice = closes[curr]
            previousPos = curr

        else:
            print("error, action: ", action, ", state: ", previousState)
            exit(-1)

        curr += 1
        if curr <= idx:
            sli = np.append(sli, li[curr])
            sopens = np.append(sopens, opens[curr])
            shighs = np.append(shighs, highs[curr])
            slows = np.append(slows, lows[curr])
            scloses = np.append(scloses, closes[curr])

    print("total: ", total, ", win: ", win, ", percentage: ", win / total * 100, "%", ", total earn: ", totalEarn)

    writeIn = { "long": writeInLong, "short": writeInShort }

    serialize.dump(writeIn, analyseFileName)


patternFileName = "pkl/pattern/pattern.dict"

def analysePattern(li, opens, highs, lows, closes):
    results = talib.CDLDOJISTAR(opens, highs, lows, closes)
    print("debug pattern: ", results)
    long = []
    short = []
    for i in range(0, results.__len__()):
        leftIdx = 0 if (i - margin < 0) else (i - margin)
        rightIdx = i + margin + 1
        markIdx = i if i <= margin else margin
        if results[i] == 100:
            long.append([li[leftIdx : rightIdx], markIdx, markIdx])
        elif results[i] == -100:
            short.append([li[leftIdx : rightIdx], markIdx, markIdx])

    writeInPattern = { "long": long, "short": short }

    serialize.dump(writeInPattern, patternFileName)

def loadPattern(fileName = patternFileName):
    patternDict = serialize.load(fileName)
    for k in patternDict:
        print(k, ": ", patternDict[k])

    return patternDict

def loadAnalyse(fileName = analyseFileName):
    analyseDict = serialize.load(fileName)
    for k in analyseDict:
        print(k, ": ", analyseDict[k])

    return analyseDict

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

    trade(li, opens, highs, lows, closes, start)
    # if direction == 1:
    #     print("buy ", fst, " with price ", opens[fst], " and sell ", snd, " with price ", opens[snd])
    #     diff = opens[snd] - opens[fst]
    #     print("diff ", diff, "$, percentage ", diff / opens[fst] * 100, "%, using 100$, earn ", diff / opens[fst] * 100, "$")
    # elif direction == -1:
    #     print("sell ", fst, " with price ", opens[fst], " and buy ", snd, " with price ", opens[snd])
    #     diff = opens[fst] - opens[snd]
    #     print("diff ", diff, "$, percentage ", diff / opens[fst] * 100, "%, using 100$, earn ", diff / opens[fst] * 100, "$")

def test():
    # get list
    return 1111

if __name__ == "__main__":
    # validate()
    ayalyse()


