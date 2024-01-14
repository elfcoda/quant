#!/usr/bin/env python
# encoding: utf-8

import okx.MarketData as MarketData
from config import ConfigSingleton
import utils.utils as utils
import utils.serialize as serialize

conf = ConfigSingleton()
marketDataAPI = MarketData.MarketAPI(flag = conf.simu_mode)

historyKLine = []

instSet = { "TRB", "EOS", "1000SATS", "ORDI", "BNB", "BTC", "ETH", "XRP", "BCH", "LTC", "ETC",
            "GMT", "APE", "OP", "NEAR", "AVAX", "SOL", "ENS", "LUNA", "MATIC", "STEEM", "XMR" }

# [1s/1m/3m/5m/15m/30m/1H/2H/4H]
barDict = {
    "1s": 1 * 1000,
    "1m": 60 * 1000,
    "3m": 3 * 60 * 1000,
    "5m": 5 * 60 * 1000,
    "15m": 15 * 60 * 1000,
    "30m": 30 * 60 * 1000,
    "1H": 60 * 60 * 1000,
    "2H": 2 * 60 * 60 * 1000,
    "4H": 4 * 60 * 60 * 1000,
}

def download(instID, bar, beginTime, endTime, limit = 100):
    interval = barDict[bar]
    fromTS = beginTime
    toTS = fromTS + interval * limit

    while (fromTS < endTime):
        downloadPage(instID, bar, fromTS, toTS)
        fromTS = toTS
        toTS = fromTS + interval * limit

def downloadPage(instID, bar, fromTS, toTS):
    # Retrieve history candlestick charts from recent years

    # fromTS 07:45 toTS 08:30, get 08:00 to 08:15 for 15m
    # needs to minus 1 for before and after
    print("get history candlestick for ", instID, " in ", bar, ", from ", fromTS, ", to ", toTS)

    result = marketDataAPI.get_history_candlesticks(
        instId  = instID,
        bar     = bar,
        before  = str(fromTS - 1),
        after   = str(toTS - 1),
        # limit = "100",
    )
    dataList = utils.formatResponse(result)
    dataList.reverse()

    global historyKLine
    historyKLine.extend(dataList)

def dumpHistory(instID, bar, begin, end, fileName):

    global historyKLine
    historyKLine = []
    download(instID, bar, begin, end)

    serialize.dump(historyKLine, fileName)

def genInstIDList():
    global instSet
    return list(map(lambda inst: inst + "-USDT", instSet))

def genBars():
    barList = []
    global barDict
    for k in barDict:
        barList.append(k)

    return barList


def demo():
    instID = "BTC-USDT"
    bar = "15m"
    begin = conf.TS2019
    end = conf.TS2024
    fileName = "./pkl/" + "DEMO-BTC-USDT-15m"
    dumpHistory(instID, bar, begin, end, fileName)

def getBeginEnd(instID):
    # if instID == "BTC-USDT":
    #     return [conf.TS2024, ConfigSingleton.getDayTS("2024", "01", "02")]
    # elif instID == "ETH-USDT":
    #     return [conf.TS2024, ConfigSingleton.getDayTS("2024", "01", "02")]

    return [conf.TS2019, conf.TS2024]

if __name__ == "__main__":
    instList = genInstIDList()
    bars = genBars()

    for instID in instList:
        for bar in bars:
            [begin, end] = getBeginEnd(instID)
            fileName = "./pkl/" + instID + "-" + bar

            print("dump history for ", instID, " for ", bar, ", from ", begin, " to ", end, ", dump to ", fileName, ".pkl.")
            dumpHistory(instID, bar, begin, end, fileName)

