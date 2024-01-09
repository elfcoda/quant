#!/usr/bin/env python
# encoding: utf-8

import okx.Account as Account
from config import ConfigSingleton
conf = ConfigSingleton()

accountAPI = Account.AccountAPI(conf.api_key,
                                conf.secret_key,
                                conf.passphrase,
                                False,
                                conf.simu_mode)

result = accountAPI.get_account_balance()
print(result)
