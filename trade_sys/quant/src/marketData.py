#!/usr/bin/env python
# encoding: utf-8

import okx.MarketData as MarketData
from config import ConfigSingleton

conf = ConfigSingleton()
marketDataAPI = MarketData.MarketAPI(flag = conf.simu_mode)

# Retrieve history candlestick charts from recent years
result = marketDataAPI.get_history_candlesticks(
    instId="BTC-USDT",

)
print(result)



# result = marketDataAPI.get_tickers(instType="SPOT")
# print(result)

