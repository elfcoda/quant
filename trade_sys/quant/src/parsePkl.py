#!/usr/bin/env python
# encoding: utf-8

import utils.serialize as serialize
import numpy as np
import talib
from config import ConfigSingleton
conf = ConfigSingleton()

HISTORY_CANDLES_OPEN = 1
HISTORY_CANDLES_HIGH = 2
HISTORY_CANDLES_LOW = 3
HISTORY_CANDLES_CLOSE = 4
HISTORY_CANDLES_VOL = 5

def loadHistory(instID, bar):
    fileName = conf.marketDataFilePrefix + instID + "-" + bar
    li = serialize.load(fileName)
    for item in li:
        print(item)
    print("total: ", li.__len__())

    return li

# turn [["1.1", "2.2", "3.3"], ["4.4", "5.5", "6.6"]], 2 into [3.3, 6.6]
def loadColumn(li, idx):
    return list(map(lambda item: float(item[idx]), li))

def loadClosePrice(li):
    return loadColumn(li, HISTORY_CANDLES_CLOSE)



if __name__ == "__main__":
    li = loadHistory("BTC-USDT", "1H")
    close = np.array(loadClosePrice(li))
    print("close: ", close)
    sma = talib.SMA(close)
    # MACD and analyse directly
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    print("DIFF: ", macd)
    print("DEA: ", macdsignal)
    print("STICK_MACD: ", macdhist)



