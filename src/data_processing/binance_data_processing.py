from typing import List
from exchanges_integration.binance_local.data_consumers.market_info import (
    get_orderbook_ticks,
)


async def label_exchange_binance(client, symbols: List[str]) -> List[dict]:
    """
    Gathers binance info on all symbols in the list and returns the real time data
    :param client: binance client
    :param symbols: list of symbols
    :return: dict exchange name and the data for all symbols
    """
    try:
        binance_prices = await get_orderbook_ticks(client, symbols=symbols)
        if binance_prices:
            binance_data = {"exchange_name": "binance", "data": binance_prices}
    except Exception as e:
        print(e)
        print("Retrying...")
        label_exchange_binance(client, symbols)
    return binance_data


async def get_binance_unordered_bids_and_asks(
    exchange_name, exchange_data_item, bids_unordered, asks_unordered
):

    """
    Functions injects the binance bids and asks into the unordered dicts
    Introspecting the data structure of the bybit data

    params:
        exchange_name: str
        exchange_data_item: dict
        bids_unordered: dict
        asks_unordered: dict
    returns:
        bids_unordered: dict
        asks_unordered: dict
    """

    for item in exchange_data_item["data"]:
        if item["symbol"] not in bids_unordered.keys():
            bids_unordered[item["symbol"]] = [(exchange_name, item["bidPrice"])]

        else:
            bids_unordered[item["symbol"]].append((exchange_name, item["bidPrice"]))
        if item["symbol"] not in asks_unordered.keys():
            asks_unordered[item["symbol"]] = [(exchange_name, item["askPrice"])]
        else:
            asks_unordered[item["symbol"]].append((exchange_name, item["askPrice"]))
    return bids_unordered, asks_unordered
