#!/usr/bin/env python
# encoding: utf-8

# 新加坡的IP可以用

import asyncio
import aiohttp
import time

# TODO SSL = False

# 其实不需要加index，已经是有序的
async def fetch_data(session, url, index):
    async with session.get(url, ssl=False) as response:
        # 获取响应内容
        data = await response.text()
        # 返回请求的索引和响应内容
        return index, data

async def send_batch(session, batch, base_index):
    tasks = []
    # 发送每个请求并保存任务
    for index, url in enumerate(batch):
        tasks.append(fetch_data(session, url, base_index + index))
    # 等待所有任务完成
    responses = await asyncio.gather(*tasks)
    # 返回
    return responses

async def request_urls_batch(urls, batch_size = 15, interval = 0.01):
    rsp = []
    async with aiohttp.ClientSession() as session:
        # 将所有 URL 列表分成每批的子列表
        batches = [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]
        base_index = 0
        # 异步发送每批请求
        for batch in batches:
            responses = await send_batch(session, batch, base_index)
            rsp.extend(responses)
            await asyncio.sleep(interval)
            base_index += batch_size

    # (index, data)
    # for item in rsp:
    #     print("idx: ", item[0], ", data: ", item[1])

    return rsp


