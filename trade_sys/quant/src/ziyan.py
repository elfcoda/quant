#!/usr/bin/env python
# encoding: utf-8

from binance_comm import *

#
# CFG_TYPE_GOOD 以及 CFG_TYPE_NORMAL
# 1小时级别: "SymbolBase_index": [price1, price2, hours, year, mon, day, hour, config_type]
# 表示某个币种后缀跟个下标，这个币种可以配置最多10条线
trendCoinHour_ZIYAN = {
        # 如：对JASMY配置的第一条，第一个价格是0.01551，第二个价格是0.01665，中间一共过了36小时，第二个价格的时间是2024年3月21日0点
        # 那么在下次到达趋势线附近会发送邮件
        # CFG_TYPE_GOOD表示当前配置是优质配置，到达这附近有大概率会反弹
        # CFG_TYPE_NORMAL表示当前配置为普通配置，但是已经到平均低点，可以先入场一部分
        # "JASMY_0": [0.01551, 0.01665, 36, 2024, 3, 21, 0, CFG_TYPE_GOOD],

        # please fill in your coins
}

# ziyan = [
#     "1000SATS",
#     "1INCH",
#     "AAVE",
#     "ADA",
#     "AGIX",
#     "ALGO",
#     "ALT",
#     "AMP",
#     "ANKR",
#     "APE",
#     "APT",
#     "AR",
#     "ARB",
#     "ASTR",
#     "ATOM",
#     "AVAX",
#     "AXL",
#     "AXS",
#     "BAT",
#     "BCH",
#     "BEAMX",
#     "BLUR",
#     "BNB",
#     "BOME",
#     "BONK",
#     "BTC",
#     "BTTC",
#     "CAKE",
#     "CELO",
#     "CFX",
#     "CHZ",
#     "CKB",
#     "COMP",
#     "CRV",
#     "DOGE",
#     "DOT",
#     "DYDX",
#     "DYM",
#     "EGLD",
#     "ELF",
#     "ENJ",
#     "ENS",
#     "EOS",
#     "ETC",
#     "ETH",
#     "ETHFI",
#     "FET",
#     "FIL",
#     "FLOKI",
#     "FLOW",
#     "FLUX",
#     "FTM",
#     "FTT",
#     "FXS",
#     "GAL",
#     "GALA",
#     "GAS",
#     "GLM",
#     "GLMR",
#     "GMT",
#     "GMX",
#     "GNO",
#     "GRT",
#     "HBAR",
#     "HOT",
#     "ICP",
#     "ID",
#     "ILV",
#     "IMX",
#     "INJ",
#     "IOTA",
# ]

