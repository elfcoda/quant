#!/usr/bin/env python
# encoding: utf-8

from config import ConfigSingleton
conf = ConfigSingleton()

import okx.PublicData as PublicData

publicDataAPI = PublicData.PublicAPI(flag=conf.simu_mode)

# Retrieve a list of instruments with open contracts
result = publicDataAPI.get_instruments(
    instType="SPOT"
)
print(result)

