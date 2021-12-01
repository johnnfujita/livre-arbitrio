from pybit import HTTP
from data_processing.data_models import BybitSubscriptionModelV1
from typing import List, Optional
from exchanges_integration.bybit_local.utils import websocket_connector_prod

def get_best_bids_and_asks_for_symbols(session: HTTP, symbols: List[str]) -> List[dict]:
    """
        Get the best bid and ask for a symbol
        
        params:
            session: requests.Session
            symbol: str
        return:
            best_bid: float
            best_ask: float
    """
    list_of_symbols = []
    for symbol in symbols:
        symbol_info = session.latest_information_for_symbol(symbol=symbol)
        list_of_symbols.append(symbol_info["result"][0])
  
    return list_of_symbols

def generate_trade_subscription(symbol, params={"binary": False}):
    
    """
        Generate a trade subscription for a single symbol
        
        params:
            symbol: str
            params: dict
        
        returns:
            subscription: BybitSubscriptionModelV1
    """


    subs = BybitSubscriptionModelV1(topic="trade", symbol=symbol, params=params, event="sub")
  

    return subs


def generate_trade_subscription_pool(symbols: List[str], params={"binary": False})-> List[BybitSubscriptionModelV1]:
    
    """
        Generate a pool of subscritions for the symbols
        
        params:
            symbols: List[str]
            params: dict
        returns:
            List[BybitSubscriptionModelV1]
    """
    
    subs = []
    for symbol in symbols:
        subscription = generate_trade_subscription(symbol, params)
        subs.append(subscription)
    return subs




subs: BybitSubscriptionModelV1 = generate_trade_subscription(symbol="BTCUSDT")



def get_subs():
    return subs

def main():
    print(subs.to_json())

if __name__ == "__main__":
    main()