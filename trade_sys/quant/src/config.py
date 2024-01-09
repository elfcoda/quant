#!/usr/bin/env python
# encoding: utf-8

# my personal account for simu-trader0
class ConfigSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.api_key = "81531845-daf2-4097-8c5b-6278be6bb940"
        self.secret_key = "5B52C02E28A2BCC65DA667104D70E780"
        self.passphrase = "bH$558ga"

        # live trading: 0, demo trading: 1
        self.simu_mode = "1"

        # subscription
        self.privateSubUrl = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
        # self.publicSubUrl = "wss://wspap.okex.com:8443/ws/v5/public?brokerId=9999"
        self.publicSubUrl = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"

