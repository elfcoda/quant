#!/usr/bin/env python
# encoding: utf-8

from binance_comm import *

# 1 bad, 2 mid, 3 good
#
# CFG_TYPE_GOOD 以及 CFG_TYPE_NORMAL
# 1小时级别: "SymbolBase_index": [price1, [year, mon, day, hour], price2, [year, mon, day, hour], config_type]
# 表示某个币种后缀跟个下标，这个币种可以配置最多10条线
trendCoinHour_WENJIE = {
    # 如：对JASMY配置的第一条，第一个价格是0.01551，后面跟时间，第二个价格是0.01665，第二个价格的时间是2024年3月21日0点
    # 那么在下次到达趋势线附近会发送邮件
    # CFG_TYPE_GOOD表示当前配置是优质配置，到达这附近有大概率会反弹
    # CFG_TYPE_NORMAL表示当前配置为普通配置，但是已经到平均低点，可以先入场一部分
    # "JASMY_0": [STRATEGY_TREND, 0.01551, [2024, 3, 19, 12], 0.01665, [2024, 3, 21, 0], CFG_TYPE_GOOD],


    # vegas币的配置:
    # "JASMY_1": [STRATEGY_VEGAS] # fst: 2, snd: 3, trd: 1 (不写也可以)

    ## 用 ## 注释掉还没开始上涨的vegas
    "MKR_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],

    "OCEAN_V": [STRATEGY_VEGAS, CFG_TYPE_NORMAL],
    "ONE_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    "OP_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD], # ema576 676
    "PEPE_V": [STRATEGY_VEGAS, CFG_TYPE_NORMAL],
    "POLYX_V": [STRATEGY_VEGAS, CFG_TYPE_NORMAL],
    "RSR_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],

    "SAND_V": [STRATEGY_VEGAS],
    "SKL_V": [STRATEGY_VEGAS], # ema576 676
    "SUSHI_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    "TFUEL_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    "THETA_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    "TRU_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    # "VANRY_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],

    "WAVES_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD], # 插针币
    "WBETH_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    "ZIL_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],  # 插针币
    "TNSR_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    "ENA_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],


    "MASK_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    "MATIC_V": [STRATEGY_VEGAS],
    "MEME_V": [STRATEGY_VEGAS],

    ## "NEO_V": [STRATEGY_VEGAS],
    "NEXO_V": [STRATEGY_VEGAS],

    "RVN_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],

    ## "VET_V": [STRATEGY_VEGAS],

    "WIN_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    "WOO_V": [STRATEGY_VEGAS],
    "XEM_V": [STRATEGY_VEGAS],
    "XTZ_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    "YFI_V": [STRATEGY_VEGAS, CFG_TYPE_GOOD],
    "ZEC_V": [STRATEGY_VEGAS], # 插针币


    # Trend List (From binance_special_pump_6.py)
    # "LUNC_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "MAGIC_0": [STRATEGY_TREND, 1.0368, [2024, 3, 22, 20], 1.1296, [2024, 3, 25, 20], CFG_TYPE_GOOD],
    # "MANA_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "MANTA_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "MASK_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "MATIC_0": [STRATEGY_TREND, 0.9856, [2024, 3, 25, 1], 1.026, [2024, 3, 27, 0], CFG_TYPE_GOOD],
    # "MEME_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "MINA_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "NEO_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "NEXO_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "OP_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "ORDI_0": [STRATEGY_TREND, 60.541, [2024, 3, 23, 4], 63.1, [2024, 3, 25, 20], CFG_TYPE_GOOD],
    # "OSMO_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "PEOPLE_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "POWR_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "QKC_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "QTUM_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "ROSE_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "RPL_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "RVN_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "RDNT_0": [STRATEGY_TREND, 0.2155, [2023, 10, 17, 0], 0.3073, [2024, 3, 19, 0], CFG_TYPE_GOOD],
    # "SAND_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "SC_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "SEI_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "SHIB_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "STORJ_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "SUN_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "SUSHI_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "TFUEL_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "TIA_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "TRX_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "TWT_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "UNI_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "VET_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "WBETH_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "WIN_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "WLD_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "XAI_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "XEM_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "XLM_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "XRP_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "XTZ_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "YFI_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    # "ZEC_0": [STRATEGY_TREND, , [], , [], CFG_TYPE_GOOD],
    "ZRX_0": [STRATEGY_TREND, 0.8575, [2024, 3, 24, 17], 0.9505, [2024, 3, 25, 23], CFG_TYPE_GOOD],

        # 更新的时候注意如果某个币有日线低点加速上涨的趋势，以其他策略单独标注

        # please fill in your coins
        # "IOTX_0": [],
        # "JASMY_0": [],
        # "JUP_0": [],
        # "KAVA_0": [],
        # "KLAY_0": [],
        # "LDO_0": [],
        # "LINK_0": [],
        # "LPT_0": [],
        # "LRC_0": [],
        # "LTC_0": [],
        # "LUNA_0": [],
        # "LUNC_0": [],
        # "MANA_0": [],
        # "MANTA_0": [],
        # "MASK_0": [],
        # "MATIC_0": [],
        # "METIS_0": [],
        # "MINA_0": [],
        # "MKR_0": [],
        # "NEAR_0": [],
        # "NEO_0": [],
        # "NEXO_0": [],
        # "OCEAN_0": [],
        # "OM_0": [],
        # "OP_0": [],
        # "ORDI_0": [],
        # "OSMO_0": [],
        # "PENDLE_0": [],
        # "PEPE_0": [],
        # "PIXEL_0": [],
        # "PYTH_0": [],
        # "QNT_0": [],
        # "QTUM_0": [],
        # "RAY_0": [],
        # "RNDR_0": [],
        # "RONIN_0": [],
        # "ROSE_0": [],
        # "RPL_0": [],
        # "RUNE_0": [],
        # "SAND_0": [],
        # "SC_0": [],
        # "SEI_0": [],
        # "SHIB_0": [],
        # "SKL_0": [],
        # "SNX_0": [],
        # "SOL_0": [],
        # "SSV_0": [],
        # "STRK_0": [],
        # "STX_0": [],
        # "SUI_0": [],
        # "SUPER_0": [],
        # "TFUEL_0": [],
        # "THETA_0": [],
        # "TIA_0": [],
        # "TRX_0": [],
        # "TWT_0": [],
        # "UNI_0": [],
        # "VET_0": [],
        # "WBETH_0": [],
        # "WBTC_0": [],
        # "WIF_0": [],
        # "WLD_0": [],
        # "WOO_0": [],
        # "XEC_0": [],
        # "XEM_0": [],
        # "XLM_0": [],
        # "XRP_0": [],
        # "XTZ_0": [],
        # "ZEC_0": [],
        # "ZIL_0": [],
        # "ZRX_0": [],
}
