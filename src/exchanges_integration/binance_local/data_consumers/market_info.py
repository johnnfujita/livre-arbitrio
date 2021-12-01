from typing import Optional

from binance import AsyncClient
import time
import websockets


################################################################################
#                                                                              #
#                  THIS SUBMODULE DEALS WITH MARKET INFO ONLY                  #
#                                                                              #
#------------------------------------------------------------------------------#
#           symbol tickers, global tickers, websocket persistent live stream   #
#           list_open_orders.                  (calls without the library)     #                                           
#                                                                              #
################################################################################

async def get_ticks(client: AsyncClient, symbol: str):
    """
    Get the ticker for a symbol
    """
    while True:
        try:
            prices =  await client.get_all_tickers()
            current_price = ""
            for price in prices:
                if price["symbol"] == symbol:
                    current_price = price

            return current_price
        except Exception as e:
            print(e)
            time.sleep(1)
        time.sleep(0.2) 

async def get_orderbook_ticks(client: AsyncClient, symbol: Optional[str] = None):
    """
    Get the ticker for a symbol
    """
    while True:
        try:
            prices =  await client.get_orderbook_tickers()
            if symbol:
                prices = [price for price in prices if price["symbol"] == symbol]
                
            else:
                prices = [price for price in prices]
            return prices
        except Exception as e:
            print(e)
            time.sleep(1)
        time.sleep(0.2) 

async def get_coin_stream(base_url: str, symbol: str, stream_type: Optional[str] = "ticker"):
    """
    Get persistent stream connection with Binance for a symbol

    params:
        base_url: str
        stream_type: str
        symbol: str
    """

    stream = websockets.connect(f'{base_url}stream?streams={symbol}@{stream_type}')
    while True:
        try:
            async with AsyncClient(base_url=base_url) as client:
                async with client.websocket_client(stream_type=stream_type, symbol=symbol) as ws:
                    async for msg in ws:
                        if msg.get("e") == "error":
                            print(msg)
                            time.sleep(1)
                        else:
                            return msg
        except Exception as e:
            print(e)
            time.sleep(1)
        time.sleep(0.2)