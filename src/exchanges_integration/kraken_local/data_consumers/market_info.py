from typing import Optional
import aiohttp
import asyncio
import json
from typing import Optional


async def get_kraken_assets_info():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                "https://api.kraken.com/0/public/Assets"
            ) as response:
                resp = await response.json()
                data = resp["result"]
        except Exception as e:
            print(e)
            get_kraken_assets_info()

    return data


async def get_kraken_depth(symbols, count: Optional[int] = 1):
    async with aiohttp.ClientSession() as session:
        data = []
        for symbol in symbols:
            try:
                async with session.get(
                    f"https://api.kraken.com/0/public/Depth?pair={symbol}&count={count}"
                ) as response:
                    resp = await response.json()

                    resp = resp["result"][next(iter(resp["result"].keys()))]
                    resp["asks"] = [resp["asks"][0][0]]
                    resp["bids"] = [resp["bids"][0][0]]
                    resp["symbol"] = f"{symbol}T"
                    data.append(resp)
            except Exception as e:
                print(e)
                can_continue = False
                while not can_continue:
                    try:
                        async with session.get(
                            f"https://api.kraken.com/0/public/Depth?pair={symbol}&count={count}"
                        ) as response:
                            resp = await response.json()

                            resp = resp["result"][next(iter(resp["result"].keys()))]
                            resp["asks"] = [resp["asks"][0][0]]
                            resp["bids"] = [resp["bids"][0][0]]
                            resp["symbol"] = f"{symbol}T"
                            if resp:
                                data.append(resp)
                                can_continue = True
                    except Exception as e:
                        print(e)
                        await asyncio.sleep(1)

        return data
