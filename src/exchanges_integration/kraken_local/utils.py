import urllib.parse
import hashlib
import hmac
import base64
import time

import aiohttp
import asyncio


async def get_kraken_time():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get("https://api.kraken.com/0/public/Time") as response:
                resp = await response.json()
        except Exception as e:
            print(e)
            get_kraken_time()
    return resp["result"]["unixtime"]


def get_kraken_signature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data["nonce"]) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())

    return sigdigest.decode()


### SIGNING EXAMPLE
# api_sec = "kQH5HW/8p1uGOVjbgWA7FunAmGO8lsSUXNsu3eow76sz84Q18fWxnyRzBHCd3pd5nE9qa99HAZtuZuj6F1huXg=="

# data = {
#     "nonce": int(time.time() * 1000),
#     "ordertype": "limit",
#     "pair": "XBTUSD",
#     "price": 37500,
#     "type": "buy",
#     "volume": 1.25,
# }
