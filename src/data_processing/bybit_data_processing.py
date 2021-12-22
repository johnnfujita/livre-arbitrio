from typing import List, Optional
from exchanges_integration.bybit_local.data_consumers.market_info import (
    get_best_bids_and_asks_for_symbols,
)
from pybit import HTTP


async def label_exchange_bybit(session: HTTP, symbols: List[str]) -> Optional[dict]:
    """
    function receive the symbols to retrieve data from bybit
    params:
        session: HTTP
        symbols: List[str]
    returns:
        bids_unordered: Optional(dict)
    """

    bybit_prices = get_best_bids_and_asks_for_symbols(session, symbols=symbols)

    if bybit_prices:
        bybit_data = {"exchange_name": "bybit", "data": bybit_prices}
    else:
        bybit_data = None

    return bybit_data


async def get_bybit_unordered_bids_and_ask(
    exchange_name, exchange_data_item, bids_unordered, asks_unordered
):

    """
    Functions injects the bybit bids and asks into the unordered dicts
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
        bid = item["bid_price"]
        ask = item["ask_price"]

        if item["symbol"] not in bids_unordered.keys():
            bids_unordered[item["symbol"]] = [(exchange_name, bid)]

        else:
            bids_unordered[item["symbol"]].append((exchange_name, bid))

        if item["symbol"] not in asks_unordered.keys():
            asks_unordered[item["symbol"]] = [(exchange_name, ask)]
        else:
            asks_unordered[item["symbol"]].append((exchange_name, ask))
    return bids_unordered, asks_unordered
