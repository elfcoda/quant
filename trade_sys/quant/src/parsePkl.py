#!/usr/bin/env python
# encoding: utf-8

import utils.serialize as serialize
import utils.utils as utils
import numpy as np
import talib
import matplotlib.pyplot as plt
from marketData import genBars, instSet, barDict
from cryptoType import getInstDays
from config import ConfigSingleton
conf = ConfigSingleton()

# checkSet = { "APE", "AVAX", "BCH", "BTC", "ENS", "EOS", "ETC", "ETH", "GMT", "LTC", "LUNA", "MATIC", "NEAR", "OKB", "OP", "ORDI", "SATS", "SOL", "TRB", "XRP" }
checkSet = { "ETC" }

margin = 40

HISTORY_CANDLES_TS = 0
HISTORY_CANDLES_OPEN = 1
HISTORY_CANDLES_HIGH = 2
HISTORY_CANDLES_LOW = 3
HISTORY_CANDLES_CLOSE = 4
HISTORY_CANDLES_VOL = 5

def loadHistory(coin, instID, bar, pathPre = "./"):
    fileName = pathPre + conf.marketDataFilePrefix + coin + "/" + instID + "-" + bar
    li = serialize.load(fileName)
    # for item in li:
    #     print(item)
    print("total: ", li.__len__())

    return li

# turn [["1.1", "2.2", "3.3"], ["4.4", "5.5", "6.6"]], 2 into [3.3, 6.6]
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

def canIgnore(prev, curr):
    if prev == 0:
        return False
    t = abs(curr - prev) / abs(prev)
    return t < 0.07

def increaseN(li, n):
    while n > 0:
        if li[-n] <= li[-n-1]:
            return False
        n -= 1
    return True

def decreaseN(li, n):
    while n > 0:
        if li[-n] >= li[-n-1]:
            return False
        n -= 1
    return True

# TODO: Pattern, MA line trend
#  FIND SPECIFIC POINT
startMACD = False
curContinue = 1
def strategy(li, opens, highs, lows, closes, previousState):
    global startMACD
    global curContinue

    if not hasattr(strategy, "fstCall"):
        strategy.fstCall = True
    else:
        strategy.fstCall = False

    macd, macdsignal, macdhist = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
    # print("DIFF: ", macd)
    # print("DEA: ", macdsignal)
    # print("STICK_MACD: ", macdhist)

    continueCnt = 6
    threshold = 5
    minContinue = 5

    if not startMACD:
        if STATE_SIDELINES != previousState:
            print("ERROR: should be sidelines")
            exit(0)

        if increaseN(macdhist[-50 : -1], continueCnt):
            if macdhist[-1] < macdhist[-2]:
                startMACD = True
                curContinue = 1
                return ACTION_SHORT
            elif macdhist[-1] < threshold:
                startMACD = True
                curContinue = continueCnt
                return ACTION_LONG
            else:
                return ACTION_SIDELINES

        elif decreaseN(macdhist[-50 : -1], continueCnt):
            if macdhist[-1] > macdhist[-2]:
                startMACD = True
                curContinue = 1
                return ACTION_LONG
            elif macdhist[-1] > -threshold:
                startMACD = True
                curContinue = continueCnt
                return ACTION_SHORT
            else:
                return ACTION_SIDELINES
    else:
        # start MACD
        if STATE_SIDELINES == previousState:
            print("ERROR: should not sidelines")
            exit(0)

        elif STATE_LONG == previousState:
            if macdhist[-1] < macdhist[-2]:
                if curContinue < minContinue:
                    startMACD = False
                    return ACTION_CLOSE_LONG

                curContinue = 1
                return ACTION_CLOSE_LONG_AND_SHORT
            else:
                curContinue += 1
                return ACTION_SIDELINES

        else:
            if macdhist[-1] > macdhist[-2]:
                if curContinue < minContinue:
                    startMACD = False
                    return ACTION_CLOSE_SHORT

                curContinue = 1
                return ACTION_CLOSE_SHORT_AND_LONG
            else:
                curContinue += 1
                return ACTION_SIDELINES


    # stream_SMA, check dir(talib)
    # sma = talib.SMA(closes)

    return ACTION_SIDELINES

def genList(li, start, end, marginV = margin):
    m = start - marginV
    l = 0 if m < 0 else m
    r = end + marginV + 1
    markIdx = start if start <= marginV else marginV
    return [li[l : r], markIdx, markIdx + (end - start)]


def summary():
    pass

### get Quote
# find trend and pattern

def isUp(item):
    return item[HISTORY_CANDLES_CLOSE] > item[HISTORY_CANDLES_OPEN]

def isUpN(li, n):
    for item in li[-n:]:
        if not isUp(item):
            return False

    return True


TestFileName = "pkl/analyse/test.lst"
def analyseTest1(li, opens, highs, lows, closes):
    res = []
    for idx in range(0, li.__len__()):
        w = highs[idx] / lows[idx]
        if w >= 1.0065 and w <= 1.012:
            res.append(genList(li, idx, idx))

    serialize.dump(res, TestFileName)

def analyseTest(li, opens, highs, lows, closes):
    res = []
    n = 5
    idx = n + 3
    while idx < li.__len__():
        if isUpN(li[idx - n - 1 : idx+1], n):
            res.append(genList(li, idx, idx, 70))
            while isUp(li[idx]):
                idx += 1
        idx += 1

    serialize.dump(res, TestFileName)


def loadTest(fileName = TestFileName):
    lst = serialize.load(fileName)
    return lst

HTFileName = "pkl/pattern/HT.lst"
def analyseCycle(li, opens, highs, lows, closes):
    # real = talib.AD(highs, lows, closes, vols)
    # print("real: ", real)

    # serialize.dump(li, HTFileName)
    pass

def loadHT(fileName = HTFileName):
    lst = serialize.load(fileName)
    return lst


analyseFileName = "pkl/analyse/analyse.dict"
def trade(li, opens, highs, lows, closes, start):
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
        if action != ACTION_SIDELINES:
            print("action: ", action, " in position ", curr, ", price ", closes[curr], ", sticks size: ", scloses.size, ", time: ", utils.formatTS(li[curr][HISTORY_CANDLES_TS]))

        if ACTION_SIDELINES == action:
            # print("do nothing!")
            pass

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
            print("diff ", int(diff), "$, percentage ", format(percentage, '.3f'), "%, using ", base, "$, earn ", int(earn), "$")

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
            print("diff ", int(diff), "$, percentage ", format(percentage, '.3f'), "%, using ", base, "$, earn ", int(earn), "$")

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
            print("diff ", int(diff), "$, percentage ", format(percentage, '.3f'), "%, using ", base, "$, earn ", int(earn), "$")

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
            print("diff ", int(diff), "$, percentage ", format(percentage, '.3f'), "%, using ", base, "$, earn ", int(earn), "$")

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

    print("total: ", total, ", win: ", win, ", percentage: ", format(win / total * 100, '.3f'), "%", ", total earn: ", int(totalEarn))

    writeIn = { "long": writeInLong, "short": writeInShort }

    serialize.dump(writeIn, analyseFileName)

macdFileName = "pkl/pattern/macd.lst"
def analyseMACD(li, opens, highs, lows, closes):
    continueCnt = 7
    curContinue = 1
    isLong = False

    macd = []

    mac, macdsignal, macdhist = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
    for idx in range(1, macdhist.__len__()):
        if isLong and macdhist[idx] > macdhist[idx - 1]:
            curContinue += 1
        elif not isLong and macdhist[idx] < macdhist[idx - 1]:
            curContinue += 1
        elif isLong and macdhist[idx] <= macdhist[idx - 1]:
            if curContinue >= continueCnt:
                macd.append(genList(li, idx, idx, 50))
            curContinue = 1
            isLong = False
        elif not isLong and macdhist[idx] >= macdhist[idx - 1]:
            if curContinue >= continueCnt:
                macd.append(genList(li, idx, idx, 50))
                pass
            curContinue = 1
            isLong = True
        idx += 1

    serialize.dump(macd, macdFileName)

patternFileName = "pkl/pattern/pattern.dict"
def analysePattern(li, opens, highs, lows, closes):
    results = talib.CDLUNIQUE3RIVER(opens, highs, lows, closes)
    print("debug pattern: ", results)
    long = []
    short = []
    for i in range(0, results.__len__()):
        leftIdx = 0 if (i - margin < 0) else (i - margin)
        rightIdx = i + margin + 1
        markIdx = i if i <= margin else margin
        if results[i] == 100:
            long.append([li[leftIdx : rightIdx], markIdx, markIdx])
            print("find 100: ", i)
        elif results[i] == -100:
            short.append([li[leftIdx : rightIdx], markIdx, markIdx])
            print("find -100: ", i)

    writeInPattern = { "long": long, "short": short }

    serialize.dump(writeInPattern, patternFileName)

def loadMACD(fileName = macdFileName):
    lst = serialize.load(fileName)
    return lst

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

def printItem(item):
    print("open: ", item[1], ", high: ", item[2], ", low: ", item[3], ", close: ", item[4], "ts: ", item[0], ", time: ", utils.formatTS(item[0]))

def printComplete(li):
    for item in li:
        printItem(item)

### weekend
# datetime.datetime(2023, 12, 30, 0, 0)
someSaturday = 1703865600000
# datetime.datetime(2012, 6, 30, 0, 0)
elderSat = someSaturday - (1000 * 60 * 60 * 24 * 7 * 600)
# two days
twoDays = 1000 * 60 * 60 * 24 * 2
oneWeek = 1000 * 60 * 60 * 24 * 7
def isWeekend(ts):
    t = (ts - elderSat) % oneWeek
    return t <= twoDays

def filterWeekendBound(li):
    l = li.__len__()
    idx = margin
    while isWeekend(int(li[idx][HISTORY_CANDLES_TS])):
        idx += 1

    while idx < l:
        if isWeekend(int(li[idx][HISTORY_CANDLES_TS])):
            begin = idx

            interval = int(li[1][HISTORY_CANDLES_TS]) - int(li[0][HISTORY_CANDLES_TS])
            barCnt2 = int(twoDays / interval)

            return [begin, barCnt2]
        else:
            idx += 1
    print("ERROR in filterWeekendBound")

def filterWeekends(li):
    weekends = []
    [begin, barCnt2] = filterWeekendBound(li)

    interval = int(li[1][HISTORY_CANDLES_TS]) - int(li[0][HISTORY_CANDLES_TS])
    barCnt7 = int(oneWeek / interval)

    b = begin
    e = b + barCnt2
    while b < li.__len__():
        weekends.append(genList(li, b, e))
        b += barCnt7
        e = b + barCnt2

    return weekends

def filterWeekendsCrypto(quantPre):
    coin = "EOS"
    latest = 1600
    bar = "5m"
    li = loadHistory(coin, coin + "-USDT", bar, quantPre)

    # handle this one
    li = li[-latest:]

    return filterWeekends(li)

def getDays(quantPre):
    return getInstDays()

def ayalyse():
    coin = "EOS"
    latest = 5500
    # latest = 200
    start = 100
    bar = "15m"
    li = loadHistory(coin, coin + "-USDT", bar)

    # handle this one
    li = li[-latest:]
    # printComplete(li[:-50])
    closes = np.array(loadClosePrice(li))
    opens = np.array(loadOpenPrice(li))
    highs = np.array(loadHighPrice(li))
    lows = np.array(loadLowPrice(li))
    # print("closes: ", closes)

    # analyseMACD(li, opens, highs, lows, closes)
    # analyseCycle(li, opens, highs, lows, closes)
    # analysePattern(li, opens, highs, lows, closes)
    analyseTest(li, opens, highs, lows, closes)

    # trade(li, opens, highs, lows, closes, start)


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


