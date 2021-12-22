from typing import List, Optional
from exchanges_integration.kraken_local.data_consumers.market_info import (
    get_kraken_depth,
)


async def label_exchange_kraken(
    symbols: List[str], count: Optional[int] = 1
) -> List[dict]:
    """
    Gathers kraken's info on all symbols in the list and returns the real time data
    :param client: binance client
    :param symbols: list of symbols
    :return: dict exchange name and the data for all symbols
    """

    kraken_prices = await get_kraken_depth(symbols, count)
    if kraken_prices:
        kraken_data = {"exchange_name": "kraken", "data": kraken_prices}
    else:
        kraken_data = None
    return kraken_data


async def get_kraken_unordered_bids_and_ask(
    exchange_name, exchange_data_item, bids_unordered, asks_unordered
):

    """
    Functions injects the kraken bids and asks into the unordered dicts
    Introspecting the data structure of the kraken data

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

        bid = item["bids"][0]
        ask = item["asks"][0]
        print(bid)
        print(ask)
        if item["symbol"] not in bids_unordered.keys():
            bids_unordered[item["symbol"]] = [(exchange_name, bid)]

        else:
            bids_unordered[item["symbol"]].append((exchange_name, bid))

        if item["symbol"] not in asks_unordered.keys():
            asks_unordered[item["symbol"]] = [(exchange_name, ask)]
        else:
            asks_unordered[item["symbol"]].append((exchange_name, ask))
    return bids_unordered, asks_unordered
