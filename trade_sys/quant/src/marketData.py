#!/usr/bin/env python
# encoding: utf-8

import okx.MarketData as MarketData
from config import ConfigSingleton
import utils.utils as utils
from utils.logs import LogSingleton
import utils.serialize as serialize
import time

conf = ConfigSingleton()
log = LogSingleton()
marketDataAPI = MarketData.MarketAPI(flag = conf.simu_mode)

historyKLine = []

# already finished
# instSet = { "APE", "AVAX", "BCH", "BTC", "ENS", "EOS", "ETC", "ETH", "GMT", "LTC", "LUNA", "MATIC", "NEAR", "OKB", "OP", "ORDI", "SATS", "SOL", "TRB", "XRP" }
instSet = { "ETC" }

# [1s/1m/3m/5m/15m/30m/1H/2H/4H]
barDict = {
    # "1s": 1 * 1000,
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

    while True:
        try:
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

            return
        except Exception as e:
            log.debug("exception in downloadPage for instID: " + instID + ", bar: " + bar + ", fromTS: " + str(fromTS) + ", toTS: " + str(toTS) + ", msg: " + str(e))
            time.sleep(0.2)


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
    fileName = conf.marketDataFilePrefix + "DEMO-BTC-USDT-15m"
    dumpHistory(instID, bar, begin, end, fileName)

def getBeginEnd(instID):
    # okex
    if instID == "SATS-USDT":
        return [ConfigSingleton.getDayTS("2023", "12", "18"), conf.TS2024]
    if instID == "LUNA-USDT":
        return [ConfigSingleton.getDayTS("2022", "05", "28"), conf.TS2024]
    if instID == "OP-USDT":
        return [ConfigSingleton.getDayTS("2022", "05", "29"), conf.TS2024]
    if instID == "SOL-USDT":
        return [ConfigSingleton.getDayTS("2020", "09", "27"), conf.TS2024]
    if instID == "AVAX-USDT":
        return [ConfigSingleton.getDayTS("2020", "09", "20"), conf.TS2024]
    if instID == "TRB-USDT":
        return [ConfigSingleton.getDayTS("2020", "08", "23"), conf.TS2024]
    if instID == "ORDI-USDT":
        return [ConfigSingleton.getDayTS("2023", "05", "14"), conf.TS2024]
    if instID == "GMT-USDT":
        return [ConfigSingleton.getDayTS("2022", "03", "27"), conf.TS2024]
    if instID == "APE-USDT":
        return [ConfigSingleton.getDayTS("2022", "03", "13"), conf.TS2024]
    if instID == "ENS-USDT":
        return [ConfigSingleton.getDayTS("2021", "11", "07"), conf.TS2024]
    if instID == "MATIC-USDT":
        return [ConfigSingleton.getDayTS("2021", "03", "28"), conf.TS2024]

    return [conf.TS2019, conf.TS2024]

if __name__ == "__main__":
    instList = genInstIDList()
    bars = genBars()

    for instID in instList:
        for bar in bars:
            [begin, end] = getBeginEnd(instID)
            fileName = conf.marketDataFilePrefix + instID + "-" + bar

            print("dump history for ", instID, " for ", bar, ", from ", begin, " to ", end, ", dump to ", fileName, ".pkl.")
            dumpHistory(instID, bar, begin, end, fileName)

