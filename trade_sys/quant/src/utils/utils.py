#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime
from utils.logs import LogSingleton

log = LogSingleton()

def formatTS(ts):
    dt_object = datetime.fromtimestamp(int(ts) / 1000)
    return str(dt_object)

# code msg data
def formatResponse(rsp):
    code = int(rsp["code"])
    msg = rsp["msg"]

    if code != 0:
        log.error("error in formatResponse: " + msg)
        raise ValueError(msg)

    # list of ['1704595500000', '43940.1', '43956.5', '43842.4', '43929.8', '1140.31704231', '50064751.471025097', '50064751.471025097', '1']
    data = rsp["data"]

    print("total: ", data.__len__())

    for item in data:
        time = formatTS(item[0])
        openPrice = item[1]
        highestPrice = item[2]
        lowestPrice = item[3]
        closePrice = item[4]
        # 张
        volume = item[5]
        # 币
        volumeCcy = item[6]
        # USDT
        volumeCcyQuote = item[7]
        confirm = item[8]

        item.append(time)

        # print(item)

    return data

