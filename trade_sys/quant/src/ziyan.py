#!/usr/bin/env python
# encoding: utf-8

from binance_comm import *

STRATEGY_TREND = 0
STRATEGY_VEGAS = 1
# 1 bad, 2 mid, 3 good
#
# CFG_TYPE_GOOD 以及 CFG_TYPE_NORMAL
# 1小时级别: "SymbolBase_index": [price1, [year, mon, day, hour], price2, [year, mon, day, hour], config_type]
# 表示某个币种后缀跟个下标，这个币种可以配置最多10条线
trendCoinHour_ZIYAN = {
    # 如：对JASMY配置的第一条，第一个价格是0.01551，后面跟时间，第二个价格是0.01665，第二个价格的时间是2024年3月21日0点
    # 那么在下次到达趋势线附近会发送邮件
    # CFG_TYPE_GOOD表示当前配置是优质配置，到达这附近有大概率会反弹
    # CFG_TYPE_NORMAL表示当前配置为普通配置，但是已经到平均低点，可以先入场一部分
    # "JASMY_0": [STRATEGY_TREND, 0.01551, [2024, 3, 19, 12], 0.01665, [2024, 3, 21, 0], CFG_TYPE_GOOD],

    # 更新的时候注意如果某个币有日线低点加速上涨的趋势，以其他策略单独标注

    # please fill in your coins
    "APT_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],  # 点多，间隔小于天
    "AR_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],  # 后段符合vages
    "BCH_V": [STRATEGY_VEGAS, CFG_TYPE_NORMAL],  # 最近进入vages线路,但前面有跌出长线
    "BOME_V": [STRATEGY_VEGAS, CFG_TYPE_NORMAL],  # 新币无长线，但15分钟已进入vagas
    "CFX_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],  #
    "CYBER_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],  # 1h线很好
    "DEXE_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],  #
    "ETHFI_V": [STRATEGY_VEGAS], # 15m
    "FLOKI_V": [STRATEGY_VEGAS, CFG_TYPE_NORMAL],  # 1h线还可以
    "FTM_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],  #
    "GAL_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],  #
    "HIFI_V": [STRATEGY_VEGAS, CFG_TYPE_NORMAL],  # 感觉还可以，虽然中间有跌穿，与之前大涨有关
    "ICP_V": [STRATEGY_VEGAS, CFG_TYPE_NORMAL],  # 上涨趋势强，在补前面的坑，线后面感觉会成vegas
    "JUP_V": [STRATEGY_VEGAS, CFG_TYPE_NORMAL],  # 还可以趋势向上，踩点也算准，但间隔较长，当前阶段K线离中线不远


    # Trend inst的例子:
    # "PAXG_0": [STRATEGY_TREND, 2130, [2024, 3, 21, 0], 2155, [2024, 3, 25, 20], CFG_TYPE_GOOD],
    # 请更新以下趋势，如果不存在趋势，忽略它，如果存在，解开注释并填充
    # "1000SATS_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "1INCH_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "AAVE_0": [STRATEGY_TREND, 114.46, [2024, 3, 22, 20], 125.52, [2024, 3, 26, 20], CFG_TYPE_GOOD], # ave
    "AI_0": [STRATEGY_TREND, 1.536, [2024, 3, 21, 0], 1.628, [2024, 3, 25, 0], CFG_TYPE_GOOD],
    "ALGO_0": [STRATEGY_TREND, 0.2146, [2024, 3, 19, 16], 0.251, [2024, 3, 25, 12], CFG_TYPE_GOOD], # ave
    "APE_0": [STRATEGY_TREND, 1.695, [2024, 3, 20, 12], 1.891, [2024, 3, 25, 0], CFG_TYPE_GOOD], # ave
    "ARB_0": [STRATEGY_TREND, 1.4453, [2024, 3, 19, 16], 1.6645, [2024, 3, 27, 0], CFG_TYPE_GOOD],
    "ARKM_0": [STRATEGY_TREND, 2.236, [2024, 3, 20, 12], 2.6862, [2024, 3, 25, 20], CFG_TYPE_GOOD], # ave
    # "ASTR_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "ATOM_0": [STRATEGY_TREND, 10.811, [2024, 3, 20, 12], 11.292, [2024, 3, 25, 0], CFG_TYPE_GOOD], # ave
    "AXS_0": [STRATEGY_TREND, 9.198, [2024, 3, 21, 0], 10.361, [2024, 3, 25, 20], CFG_TYPE_GOOD], # ave
    "BAT_0": [STRATEGY_TREND, 0.2654, [2024, 3, 21, 0], 0.3042, [2024, 3, 25, 16], CFG_TYPE_GOOD], # ave
    # "BEAMX_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "BLUR_0": [STRATEGY_TREND, 0.5351, [2024, 3, 21, 0], 0.5644, [2024, 3, 25, 0], CFG_TYPE_GOOD],
    # "BTTC_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "CELO_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "CHZ_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "CRV_0": [STRATEGY_TREND, 0.5865, [2024, 3, 20, 12], 0.6707, [2024, 3, 25, 20], CFG_TYPE_GOOD], # ave
    # "DASH_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "DCR_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "DOT_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "DYDX_0": [STRATEGY_TREND, 3.179, [2024, 3, 22, 20], 3.273, [2024, 3, 24, 8], CFG_TYPE_GOOD], # ave
    # "DYM_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "EGLD_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "ELF_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "ENJ_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "ENS_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "EOS_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "ETC_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "ETH_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "ETHFI_0": [STRATEGY_TREND, 4.4, [2024, 3, 26, 9], 4.644, [2024, 3, 26, 21], CFG_TYPE_GOOD],
    # "FIL_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "FLOW_0": [STRATEGY_TREND, 1.273, [2024, 3, 25, 1], 1.388, [2024, 3, 26, 22], CFG_TYPE_GOOD], # ave
    # "FTT_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "FXS_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "GAS_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "GLMR_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "GMT_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "GMX_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "GNO_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "HBAR_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "IMX_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "INJ_0": [STRATEGY_TREND, 34.92, [2024, 3, 24, 12], 36.57, [2024, 3, 25, 20], CFG_TYPE_GOOD],
    # "IOTA_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "JASMY_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "JST_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "KAVA_0": [STRATEGY_TREND, 0.8233, [2024, 3, 20, 4], 0.8973, [2024, 3, 24, 12], CFG_TYPE_GOOD],
    # "KDA_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "KLAY_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "LINK_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "LTC_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
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

