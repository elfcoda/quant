#!/usr/bin/env python
# encoding: utf-8

from binance_comm import *

# 4亿以上市值
high_market_value = [
    "BTC",
    "ETH",
    "SOL",
    "BNB",
    "XRP",
    "ADA",
    "DOGE",
    "AVAX",
    "SHIB",
    "DOT",
    "LINK",
    "TRX",
    "WBTC",
    "MATIC",
    "BCH",
    "UNI",
    "NEAR",
    "LTC",
    "APT",
    "ICP",
    "STX",
    "FIL",
    "ARB",
    "ATOM",
    "ETC",
    "RNDR",
    "IMX",
    "XLM",
    "HBAR",
    "GRT",
    "INJ",
    "OP",
    "PEPE",
    "WBETH",
    "VET",
    "FTM",
    "RUNE",
    "THETA",
    "MKR",
    "TIA",
    "WIF",
    "LDO",
    "SUI",
    "AR",
    "SEI",
    "FLOKI",
    "FET",
    "ALGO",
    "FLOW",
    "BEAMX",
    "AAVE",
    "JUP",
    "GALA",
    "CFX",
    "EGLD",
    "STRK",
    "QNT",
    "BONK",
    "PYTH",
    "SAND",
    "AXS",
    "SNX",
    "AGIX",
    "ORDI",
    "BTTC",
    "MINA",
    "WLD",
    "AXL",
    "XTZ",
    "MANA",
    "CHZ",
    "APE",
    "RONIN",
    "EOS",
    "NEO",
    "KAVA",
    "1000SATS",
    "JASMY",
    "IOTA",
    "XEC",
    "CAKE",
    "DYDX",
    "ROSE",
    "GNO",
    "DYM",
    "KLAY",
    "CKB",
    "OSMO",
    "BLUR",
    "WOO",
    "LUNC",
    "ZRX",
    "ASTR",
    "CRV",
    "MANTA",
    "NEXO",
    "ENJ",
    "OCEAN",
    "PENDLE",
    "ENS",
    "IOTX",
    "1INCH",
    "FTT",
    "BOME",
    "ID",
    "LUNA",
    "CELO",
    "SUPER",
    "COMP",
    "RAY",
    "LPT",
    "RPL",
    "ZIL",
    "FXS",
    "HOT",
    "SSV",
    "PIXEL",
    "TWT",
    "METIS",
    "ALT",
    "GMT",
    "LRC",
    "SC",
    "OM",
    "SKL",
    "TFUEL",
    "ILV",
    "FLUX",
    "GAL",
    "GLM",
    "ZEC",
    "ETHFI",
    "ANKR",
    "BAT",
    "AMP",

    # 4亿到5亿
    "GLMR",
    "GMX",
    "QTUM",
    "ELF",
    "GAS",
    "MASK",
    "XEM",
    "ONE",
    "MEME",
    "DASH",
    "WAVES",
    "SUSHI",
    "DCR",
    "KDA",
    "PAXG",
    "ARKM",
    "DEXE",
]

# 5kw以上交易额
high_deal_24h = [
    "POLYX",
    "MEME",
    "JTO",
    "FRONT",
    "MASK",
    "JOE",
    "TRU",
    "ARKM",
    "AEVO",
    "HIFI",
    "CYBER",
    "QKC",
    "POWR",
    "YFI",
    "IQ",
    "DUSK",
    "VANRY",
    "AI",
    "API3",
    "PDA",
    "LOOM",
    "DASH",
    "QTUM",
    "XAI",
    "RSR",
    "PORTAL",
    "JST",
    "WIN",
    "MAGIC",
    "STORJ",
    "PEOPLE",
    "YGG",
    "RVN",
    "SUSHI",
    "SUN",
]

def selectVegasFilter():
    se = set(high_market_value).union(set(high_deal_24h))
    li = list(se)
    li = sorted(li)
    for item in li:
        print(item)

    return li

def getAllCoinsList():
    se = set(high_market_value).union(set(high_deal_24h)).union(set(bigAmpCoins)).union(set(lowValuesCoins))
    li = list(se)
    li = sorted(li)

    return li

def getHighValueCoinsList():
    se = set(high_market_value).union(set(high_deal_24h))
    li = list(se)
    li = sorted(li)

    return li

if __name__ == "__main__":
    # selectVegasFilter()

    se = set(high_market_value).union(set(high_deal_24h))
    li = list(se)

    li = sorted(li)

    # 仅使用高市值
    li = sorted(high_market_value[:-10])

    print("total: ", len(li))
    for item in li:
        print(item)



