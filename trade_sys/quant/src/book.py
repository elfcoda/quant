#!/usr/bin/env python
# encoding: utf-8

import okx.MarketData as MarketData
from config import ConfigSingleton
import utils.utils as utils
conf = ConfigSingleton()

marketDataAPI = MarketData.MarketAPI(flag = conf.simu_mode)


print(utils.formatTS("1704912557601"))

# 获取产品深度
result = marketDataAPI.get_orderbook(
    instId="BTC-USDT",
    sz="1",
)
print(result)

