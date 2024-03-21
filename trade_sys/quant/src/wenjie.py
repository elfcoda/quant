#!/usr/bin/env python
# encoding: utf-8

from binance_comm import *

#
# CFG_TYPE_GOOD 以及 CFG_TYPE_NORMAL
# 1小时级别: "SymbolBase_index": [price1, price2, hours, year, mon, day, hour, config_type]
# 表示某个币种后缀跟个下标，这个币种可以配置最多10条线
trendCoinHour_WENJIE = {
        # 如：对JASMY配置的第一条，第一个价格是0.01551，第二个价格是0.01665，中间一共过了36小时，第二个价格的时间是2024年3月21日0点
        # 那么在下次到达趋势线附近会发送邮件
        # CFG_TYPE_GOOD表示当前配置是优质配置，到达这附近有大概率会反弹
        # CFG_TYPE_NORMAL表示当前配置为普通配置，但是已经到平均低点，可以先入场一部分
        # "JASMY_0": [0.01551, 0.01665, 36, 2024, 3, 21, 0, CFG_TYPE_GOOD],

        # 更新的时候注意如果某个币有日线低点加速上涨的趋势，以其他策略单独标注

        # please fill in your coins
}

# wenjie = [
#     "IOTX",
#     "JASMY",
#     "JUP",
#     "KAVA",
#     "KLAY",
#     "LDO",
#     "LINK",
#     "LPT",
#     "LRC",
#     "LTC",
#     "LUNA",
#     "LUNC",
#     "MANA",
#     "MANTA",
#     "MASK",
#     "MATIC",
#     "METIS",
#     "MINA",
#     "MKR",
#     "NEAR",
#     "NEO",
#     "NEXO",
#     "OCEAN",
#     "OM",
#     "OP",
#     "ORDI",
#     "OSMO",
#     "PENDLE",
#     "PEPE",
#     "PIXEL",
#     "PYTH",
#     "QNT",
#     "QTUM",
#     "RAY",
#     "RNDR",
#     "RONIN",
#     "ROSE",
#     "RPL",
#     "RUNE",
#     "SAND",
#     "SC",
#     "SEI",
#     "SHIB",
#     "SKL",
#     "SNX",
#     "SOL",
#     "SSV",
#     "STRK",
#     "STX",
#     "SUI",
#     "SUPER",
#     "TFUEL",
#     "THETA",
#     "TIA",
#     "TRX",
#     "TWT",
#     "UNI",
#     "VET",
#     "WBETH",
#     "WBTC",
#     "WIF",
#     "WLD",
#     "WOO",
#     "XEC",
#     "XEM",
#     "XLM",
#     "XRP",
#     "XTZ",
#     "ZEC",
#     "ZIL",
#     "ZRX",
# ]
