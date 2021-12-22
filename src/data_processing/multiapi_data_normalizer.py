import websockets
import asyncio
import json
import datetime
from pydantic import BaseModel
import datetime
import pandas as pd

from .data_models import BinanceModel

from data_processing.bybit_data_processing import get_bybit_unordered_bids_and_ask
from data_processing.binance_data_processing import get_binance_unordered_bids_and_asks
from data_processing.kraken_data_processing import get_kraken_unordered_bids_and_ask


def kafka_serializer(message) -> None:
    """
    Serializer for kafka message
    """
    return json.dumps(message).encode("utf-8")


async def generate_ordered_trades_for_each_exchange(exchanges_data: list):
    bids_unordered = {}
    asks_unordered = {}

    for exchange_data_item in exchanges_data:
        exchange_name = exchange_data_item["exchange_name"]

        if exchange_name == "binance":

            bids_unordered, asks_unordered = await get_binance_unordered_bids_and_asks(
                exchange_name, exchange_data_item, bids_unordered, asks_unordered
            )

        elif exchange_name == "bybit":
            bids_unordered, asks_unordered = await get_bybit_unordered_bids_and_ask(
                exchange_name, exchange_data_item, bids_unordered, asks_unordered
            )

        elif exchange_name == "kraken":
            bids_unordered, asks_unordered = await get_kraken_unordered_bids_and_ask(
                exchange_name, exchange_data_item, bids_unordered, asks_unordered
            )
    # sorting bids and asks
    bids_ordered = {}
    asks_ordered = {}

    for key, value in bids_unordered.items():

        value.sort(key=lambda x: float(x[1]), reverse=True)

        bids_ordered[key] = value

    for key, value in asks_unordered.items():
        value = value.sort(key=lambda x: float(x[1]))
        asks_ordered[key] = value

    return bids_ordered, asks_unordered


# stream = websockets.connect('wss://stream.binance.com:9443/stream?streams=adausdt@ticker')


# def generate_data_model(data):

#     binance_ticker = BinanceModel(
#         event_time=data["E"],
#         symbol=str(data['s']),
#         last_price=float(data['c']),
#         last_quantity=float(data['q']),
#         price_change=float(data['p']),
#         price_change_percent=float(data['P']),
#         open_price = float(data['o']),
#         high = float(data['h']),
#         low = float(data['l']),
#         volume = float(data['v']),
#         quote_volume = float(data['Q'])
#     )

#     return binance_ticker

# def create_data_frame(data):
#     df = pd.DataFrame([data])
#     df.event_time = pd.to_datetime(df.event_time, unit='ms')
#     print(df.tail())

# async def main():
#     while True:
#         async with stream as receiver:
#             data_dict = {}
#             data = await receiver.recv()

#             data = json.loads(data)["data"]

#         binance_ticker = generate_data_model(data)
#         create_data_frame(binance_ticker.dict())
