#!/usr/bin/env python
# encoding: utf-8

import okx.Trade as Trade
from config import ConfigSingleton

conf = ConfigSingleton()

tradeAPI = Trade.TradeAPI(conf.api_key,
                          conf.secret_key,
                          conf.passphrase,
                          False,
                          conf.simu_mode)

result = tradeAPI.place_order(
    instId="LTC-USDT",
    tdMode="cash",
    side="buy",
    ordType="market",
    sz="100",
)
print(result)
