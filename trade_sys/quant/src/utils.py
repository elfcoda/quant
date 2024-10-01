#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import numpy as np


def MA(li_prices, timeperiod):
    price_series = pd.Series(li_prices)
    ma = price_series.rolling(window=timeperiod).mean()
    return ma

def EMA(li_prices, timeperiod):
    price_series = pd.Series(li_prices)
    ema = price_series.ewm(span=timeperiod, adjust=False).mean()
    return ema

def MACD(li_prices, fastperiod = 12, slowperiod = 26, signalperiod = 9):
    price_series = pd.Series(li_prices)
    short_ema = price_series.ewm(span=fastperiod, adjust=False).mean()
    long_ema = price_series.ewm(span=slowperiod, adjust=False).mean()

    dif = short_ema - long_ema
    dea = dif.ewm(span=signalperiod, adjust=False).mean()
    macd = 2 * (dif - dea)

    return macd
