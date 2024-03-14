#!/usr/bin/env python
# encoding: utf-8

# 新加坡的IP可以用

import asyncio
import httpx
import requests

async def fetch_data(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        # response.text
        return response

async def fetch_all_data(urls):
    tasks = [fetch_data(url) for url in urls]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        pass

# asyncio.run(fetch_all_data())

HISTORY_CANDLES_TS = 0
HISTORY_CANDLES_OPEN = 1
HISTORY_CANDLES_HIGH = 2
HISTORY_CANDLES_LOW = 3
HISTORY_CANDLES_CLOSE = 4
HISTORY_CANDLES_VOL = 5

# 非现货或者是稳定币等无关
nonSpotSet = set(["BCC", "TUSD"])
# focus set
AI = set(["AGIX", "AI", "CTXC", "FET", "GRT", "IQ", "MDT", "NFP", "NMR", "OCEAN", "PHB", "RLC", "THETA", "WLD"])
RWA = set(["DUSK"])
DePIN = set(["RNDR", "IOTX", "IOTA", "JASMY", "NKN", "OCEAN", "DATA", "MDT", "LPT", "THETA"])
MoYin = set(["WIF", "PEPE", "FLOKI", "SEI", "INJ"])
# MoYin = set(["WIF", "FLOKI", "SEI", "INJ"])
Inscription = set(["ORDI"])

# 涨幅榜单日线正常
Others = set(["NEAR", "ZIL", "RUNE", "VANRY", "WAVES", "SSV", "ALGO", "BEL", "XEM", "SYS", "STMX", "SXP", "LTO", "FLUX", "ALICE", "LEVER", "ORDI", "IOST", "LINA", "KAVA", "BAT", "MATIC", "VITE", "ENJ", "CITY", "IDEX", "ERN", "SAND", "FLOW", "BURGER", "THETA", "REEF"])

# TODO: monitor this one
# 插针币: price1, price2, days, year, mon, day
neddleCoin = {
        "KEY": [0.006356, 0.007716, 20, 2024, 3, 12],
        "ZEN": [9.63, 11.6, 12, 2024, 3, 11],
        "KSM": [43.68, 49.25, 12, 2024, 3, 11],
        "SNX": [3.401, 4.014, 17, 2024, 3, 11],
        "CTK": [0.7653, 0.8497, 8, 2024, 3, 11],
        "FIRO": [1.738, 2.003, 12, 2024, 3, 11],
        "BNT": [0.8233, 0.9210, 9, 2024, 3, 12],
        "UNFI": [6.273, 7.957, 20, 2024, 3, 12],
        "STEEM": [0.2806, 0.3186, 6, 2024, 3, 12],
        "HFT": [0.4411, 0.4661, 4, 2024, 3, 12],
        "ORDI": [51.166, 70.0, 35, 2024, 3, 11]
}

def getFocusSet():
    focus = AI.union(RWA).union(DePIN).union(MoYin).union(Inscription).union(Others)
    return focus

def inFocusSet(symbolBase):
    focus = AI.union(RWA).union(DePIN).union(MoYin).union(Inscription).union(Others)
    return symbolBase in focus

def inSmartSet(symbolBase):
    smart = Others
    return symbolBase in smart

MATypeNone = 0
MATypeAbove = 1
MATypeBelow = 2

def formatPrint(MAType, symbolBase, content):
    if inSmartSet(symbolBase):
        print("\033[32m", content, "\033[0m")
    elif inFocusSet(symbolBase):
        print("\033[33m", content, "\033[0m")
    elif MAType == MATypeAbove:
        print("\033[33m", content, "\033[0m")
    elif MAType == MATypeBelow:
        print("\033[31m", content, "\033[0m")
    else:
        print(content)

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

latestPriceUrlPrefix = "https://api.binance.com/api/v3/ticker/price?symbol="
def toSymbol(symbolBase):
    return str(symbolBase) + "USDT"

def getLatestPrice(symbolBase):
    url = latestPriceUrlPrefix + toSymbol(symbolBase)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            ticker_info = response.json()
            latestPrice = float(ticker_info['price'])
            return latestPrice

        else:
            print("请求失败，状态码:", response.status_code)
    except requests.RequestException as e:
        print("请求异常:", e)


notifyDictComm = {}
def notifyAndSetupComm(nkey, currentTime, subject, content):
    global notifyDictComm

    print(content)

    # TODO
    # callMe(subject, content)
    notifyDictComm[nkey] = currentTime


def shouldNotifyComm(symbolBase, currentTime, nkey, notifyInterval = 1 * 60):
    global notifyDictComm

    previousNotify = 0
    # previous notify seconds
    if nkey in notifyDictComm:
        previousNotify = notifyDictComm[nkey]
    return currentTime - previousNotify > notifyInterval

