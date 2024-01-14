#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime

# my personal account for simu-trader0
class ConfigSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def getYearTS(year):
        return int(datetime.timestamp(datetime.strptime(year + "-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000

    @staticmethod
    def getDayTS(year, mon, day):
        return int(datetime.timestamp(datetime.strptime(year + "-" + mon + "-" + day + " 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000

    def __init__(self):
        self.api_key = "81531845-daf2-4097-8c5b-6278be6bb940"
        self.secret_key = "5B52C02E28A2BCC65DA667104D70E780"
        self.passphrase = "bH$558ga"

        # live trading: 0, demo trading: 1
        self.simu_mode = "0"

        # subscription
        self.privateSubUrl = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
        # self.publicSubUrl = "wss://wspap.okex.com:8443/ws/v5/public?brokerId=9999"
        self.publicSubUrl = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"

        # datetime
        self.TS2016 = ConfigSingleton.getYearTS("2016")
        self.TS2017 = ConfigSingleton.getYearTS("2017")
        self.TS2018 = ConfigSingleton.getYearTS("2018")
        self.TS2019 = ConfigSingleton.getYearTS("2019")
        self.TS2020 = ConfigSingleton.getYearTS("2020")
        self.TS2021 = ConfigSingleton.getYearTS("2021")
        self.TS2022 = ConfigSingleton.getYearTS("2022")
        self.TS2023 = ConfigSingleton.getYearTS("2023")
        self.TS2024 = ConfigSingleton.getYearTS("2024")

