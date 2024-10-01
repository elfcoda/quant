#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import numpy as np


def calc_ma(li_prices):
    price_series = pd.Series(li_prices)
    ma = price_series.rolling(window=5).mean()
    return ma

def calc_ema(li_prices):
    price_series = pd.Series(li_prices)
    ema = price_series.ewm(span=5, adjust=False).mean()
    return ema

def calc_macd(li_prices):
    price_series = pd.Series(li_prices)
    short_ema = price_series.ewm(span=12, adjust=False).mean()
    long_ema = price_series.ewm(span=26, adjust=False).mean()

    dif = short_ema - long_ema
    dea = dif.ewm(span=9, adjust=False).mean()
    macd = 2 * (dif - dea)

    return macd
