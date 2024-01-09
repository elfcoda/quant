import asyncio

from okx.websocket.WsPublicAsync import WsPublicAsync
from config import ConfigSingleton

conf = ConfigSingleton()

def publicCallback(message):
    print("publicCallback", message)


async def main():
    ws = WsPublicAsync(url  = conf.publicSubUrl)
    await ws.start()
    args = []
    arg1 = {"channel": "instruments", "instType": "FUTURES"}
    arg2 = {"channel": "instruments", "instType": "SPOT"}
    arg3 = {"channel": "tickers", "instId": "BTC-USDT-SWAP"}
    arg4 = {"channel": "tickers", "instId": "ETH-USDT"}
    args.append(arg1)
    args.append(arg2)
    args.append(arg3)
    args.append(arg4)
    await ws.subscribe(args, publicCallback)
    await asyncio.sleep(5)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    args2 = [arg4]
    await ws.unsubscribe(args2, publicCallback)
    await asyncio.sleep(5)
    print("-----------------------------------------unsubscribe all--------------------------------------------")
    args3 = [arg1, arg2, arg3]
    await ws.unsubscribe(args3, publicCallback)


if __name__ == '__main__':
    asyncio.run(main())
