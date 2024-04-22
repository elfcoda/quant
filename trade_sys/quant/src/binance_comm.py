#!/usr/bin/env python
# encoding: utf-8

# 新加坡的IP可以用

import asyncio
import httpx
import requests
import time
from datetime import datetime

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
STRATEGY_TREND = 0
STRATEGY_VEGAS = 1

HISTORY_CANDLES_TS = 0
HISTORY_CANDLES_OPEN = 1
HISTORY_CANDLES_HIGH = 2
HISTORY_CANDLES_LOW = 3
HISTORY_CANDLES_CLOSE = 4
HISTORY_CANDLES_VOL = 5

# 非现货或者是稳定币等无关
# UP DOWN
nonSpotSet = set(["BCC", "TUSD", "VEN", "MITH", "TOMO", "PERL", "STRAT", "AION", "BNBBEAR", "WTC", "DNT", "AUTO", "MIR", "UST", "MULTI", "NEBL", "MOB", "DREP", "PNT"])
# 低成交额(USD)
lowAmountSet = set(["IRIS", "DOCK", "OAX", "FARM", "BIFI", "HARD", "FIRO", "AST", "FUN", "ATM", "WING"])
# 低市值
lowValueSet = set(["BIDR", "DAI", "ASR", "PNT", "DREP", "IDRT", "OAX", "ATM", "OOKI", "ACM", "JUV"])
# focus set
AI = set(["AGIX", "AI", "CTXC", "FET", "GRT", "IQ", "MDT", "NFP", "NMR", "OCEAN", "PHB", "RLC", "THETA", "WLD"])
RWA = set(["DUSK"])
DePIN = set(["RNDR", "IOTX", "IOTA", "JASMY", "NKN", "OCEAN", "DATA", "MDT", "LPT", "THETA"])
MoYin = set(["WIF", "PEPE", "FLOKI", "SEI", "INJ"])
# MoYin = set(["WIF", "FLOKI", "SEI", "INJ"])
Inscription = set(["ORDI"])

# 涨幅榜单日线正常
Others = set(["NEAR", "ZIL", "RUNE", "VANRY", "WAVES", "SSV", "ALGO", "BEL", "XEM", "SYS", "STMX", "SXP", "LTO", "FLUX", "ALICE", "LEVER", "ORDI", "IOST", "LINA", "KAVA", "BAT", "MATIC", "VITE", "ENJ", "CITY", "IDEX", "ERN", "SAND", "FLOW", "BURGER", "THETA", "REEF", "JUP", "POLYX", "TRU", "FLOKI", "ETHFI", "DUSK", "AXL", "SSV", "HIFI", "RSR", "UTK", "API3", "CTK", "JUP", "PEPE", "SYN", "RAY", "BCH", "SKL", "AERGO", "QKC", "RUNE", "WIF", "FLM", "WIF", "ROBIN", "PROM", "THETA", "POND", "ONE", "UFT", "PYTH", "POWR", "JASMY", "XAI", "MAV", "SNX", "PORTAL", "STX", "LTO", "DYM", "LOOM", "PENDLE", "STEEM", "DEAMX", "METIS", "AEVO", "STEEM", "RIF", "SPELL", "ONG", "MBL", "ICX"])

def minsBy3m(n):
    return n * 3

def minsBy5m(n):
    return n * 5

def minsBy15m(n):
    return n * 15

def minsBy30m(n):
    return n * 30

def minsBy1h(n):
    return n * 60

def minsBy2h(n):
    return n * 120

def minsBy4h(n):
    return n * 240

def minsBy1d(n):
    return minsBy1h(n) * 24


CFG_TYPE_GOOD = 1
CFG_TYPE_NORMAL = 2
# 1小时级别: "SymbolBase_index": [price1, price2, hours, year, mon, day, hour, config_type]
# 表示某个币种后缀跟个下标，这个币种可以配置最多10条线
trendCoinHour = {
        # 如：对JASMY配置的第一条，第一个价格是0.01551，第二个价格是0.01665，中间一共过了18 * 2小时，第二个价格的时间是2024年3月21日0点
        # 那么在下次到达趋势线附近会发送邮件
        # CFG_TYPE_GOOD表示当前配置是优质配置，到达这附近有大概率会反弹
        # CFG_TYPE_NORMAL表示当前配置为普通配置，但是已经到平均低点，可以先入场一部分
        "JASMY_0": [0.01551, 0.01665, 18 * 2, 2024, 3, 21, 0, CFG_TYPE_GOOD],
        # "_0": [, , , 2024, 3, 11, 4, CFG_TYPE_NORMAL],
        # "_0": [, , , 2024, 3, 11, 4, CFG_TYPE_NORMAL],
        # "_0": [, , , 2024, 3, 11, 4, CFG_TYPE_NORMAL],
        # "_0": [, , , 2024, 3, 11, 4, CFG_TYPE_NORMAL],
        # "_0": [, , , 2024, 3, 11, 4, CFG_TYPE_NORMAL],
        # "_0": [, , , 2024, 3, 11, 4, CFG_TYPE_NORMAL],
}

trendCoin4h = {
        "KEY": [0.006356, 0.007716, 20, 2024, 3, 12],
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

def formatPrint4(content):
    print("\033[32m", content, "\033[0m")

def formatPrint3(tp, content):
    # wenjie: 1 2, ziyan: 3 4
    if tp == 1:
        print("\033[31m", content, "\033[0m")
    elif tp == 2:
        print("\033[32m", content, "\033[0m")
    elif tp == 3:
        print("\033[33m", content, "\033[0m")
    elif tp == 4:
        print("\033[34m", content, "\033[0m")
    else:
        print(content)

def formatPrint2(tp, symbolBase, content, macd_UP = False):
    if tp == 1:
        print("\033[31m", content, "\033[0m")
    elif tp == 2:
        print("\033[32m", content, "\033[0m")
    else:
        print(content)

# 35 洋红  36 青色  37 白色
def formatPrint(MAType, symbolBase, content, macd_UP = False):
    if macd_UP and inFocusSet(symbolBase):
        print("\033[31m", content, "\033[0m") # red
    elif inSmartSet(symbolBase):
        print("\033[32m", content, "\033[0m") # green
    elif inFocusSet(symbolBase):
        print("\033[33m", content, "\033[0m") # yellow
    elif MAType == MATypeAbove:
        print("\033[34m", content, "\033[0m") # blue
    elif MAType == MATypeBelow:
        print("\033[34m", content, "\033[0m")
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

def inSleepMode():
    # sleep from 01:00:00
    startTS = int(datetime.timestamp(datetime.strptime("2024-03-20 01:00:00", "%Y-%m-%d %H:%M:%S")))
    # sleep for 8 hours
    periodTS = 8 * 60 * 60

    currentTime = int(time.time())
    oneDayTS = 24 * 60 * 60
    passedInDay = (currentTime - startTS) % oneDayTS
    if passedInDay < periodTS:
        print("In Sleep Mode")
        return True
    else:
        return False

vegas_excluded_list = [""]

# 买过的 绿色
lv1 = [ "MEME", "ID", "INJ", "SUSHI", "DYM", "TWT", "SC", "GNO", "ARKM", "FTM", "MATIC", "XTZ", "FLOW", "GMX", "CRV", "MANTA", "DOT", "CKB", "SHIB", "APT", "ETHFI"]
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
# 4kw ~ 4亿, 还没涨过的
lowValuesCoins = [
        "HARD", "VITE", "PSG", "WING", "BAR", "DOCK", "ALPACA", "AMB", "KP3R", "ADX", "VOXEL", "BURGER", "VIDT", "FIS", "AVA", "COS", "CHESS", "CREAM", "QUICK", "KEY", "BSW",
        "KMD", "AEUR", "FIDA", "BEL", "UNFI", "LOKA", "LIT", "IRIS", "UTK", "MDX", "COMBO",
        "ALCX", "REEF", "MLN", "DEGO", "FUN", "FLM", "MDT", "DIA", "ORN", "IDEX", "AERGO", "LEVER", "BETA", "DATA", "PDA", "ATA", "WAN", "GHST", "WNXM", "NULS",
        "PERP", "VIC", "FORTH", "REN", "XVG", "CTXC", "TLM", "QKC", "HIGH", "MBL", "FRONT", "LTO", "TKO", "NKN", "POLS", "CLV", "WRX", "STMX", "QI", "OGN",
        "ERN", "CTK", "AGLD", "MBOX", "SPELL", "RARE", "BAKE", "ALICE", "LQTY", "PHB", "ARDR", "BADGER", "GTC", "DAR", "ALPHA", "LOOM", "MTL", "HIFI", "STG",
        "STEEM", "OMG", "GNS", "SUN", "OXT", "WIN", "RDNT", "STPT", "DODO", "ONG", "KNC", "RAD", "MAV", "PUNDIX", "HFT", "REQ", "ACA", "STRAX", "BLZ",
        "TRU", "MOVR", "SNT", "ARK", "DENT", "SCRT", "PEOPLE", "BNX", "HOOK", "PHA", "POWR", "PYR", "ZEN", "HIVE", "SYS", "CVC", "XNO", "NFP", "DGB", "TRB",
        "NMR", "ACE", "SYN", "REI", "CTSI", "SLP", "USTC", "LSK", "CYBER", "XVS", "CELR", "AI", "IOST", "PROM", "IQ", "RLC", "RIF", "DUSK", "POND", "BAL",
        "SXP", "MAGIC", "C98", "COTI", "EDU", "BAND", "ONT", "ACH", "VTHO", "VANRY",
        # 再加点中等市值的
        "CRV", "MANTA", "NEXO", "ENJ", "OCEAN", "PENDLE", "ENS", "IOTX", "1INCH", "FTT", "BOME", "ID", "LUNA", "CELO", "SUPER", "COMP", "RAY", "LPT", "RPL", "ZIL", "FXS", "HOT", "SSV", "PIXEL",
        "TWT", "METIS", "ALT", "GMT", "LRC", "SC", "OM", "SKL", "TFUEL", "ILV", "FLUX", "GAL", "GLM", "ZEC", "ETHFI", "ANKR", "BAT", "AMP", "GLMR", "GMX", "QTUM", "ELF", "GAS", "MASK",
        "XEM", "ONE", "MEME", "DASH", "WAVES", "SUSHI", "DCR", "KDA", "PAXG", "ARKM", "DEXE" ]

# 红色缓慢上升就等绿柱，否则直接上.非vegas币基本不用看
VegasInlowValuesCoins = [
    "HARD", "VITE", "PSG", "BAR", "DOCK", "ALPACA", "AMB", "ADX", "VOXEL", "BURGER", "VIDT", "FIS", "COS", "CREAM", "FUN", "FLM", "LEVER", "QKC", "HIGH", "LTO", "NKN", "MBOX", "SPELL", "RARE", "ARDR", "GTC",
    "DAR", "MTL", "HIFI", "STG", "STEEM", "OXT", "RDNT", "STPT", "KNC", "RAD", "MAV", "HFT", "REQ", "HOOK", "PHA", "SYS", "DGB", "SYN", "BAL", "SXP", "C98", "VANRY"
]


bigAmpCoins = ["REI", "FOR", "BOND", "AEVO", "CLV", "ETHFI", "WAN", "TRU"]

def isInTrendUp(ema1h_n):
    if ema1h_n[-2] > ema1h_n[-4]  > ema1h_n[-6] > ema1h_n[-8] > ema1h_n[-10] > ema1h_n[-12] > ema1h_n[-14] > ema1h_n[-16] > ema1h_n[-18]: # > ema1h_n[-20] > ema1h_n[-22] > ema1h_n[-24]:
        return True
    return False
