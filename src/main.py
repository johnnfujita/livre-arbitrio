from dotenv import load_dotenv
import os
from binance import AsyncClient
import asyncio

from pybit import HTTP
from data_processing.multiapi_data_normalizer import generate_ordered_trades_for_each_exchange
from exchanges_integration.binance_local.data_consumers.market_info import get_ticks, get_orderbook_ticks

from exchanges_integration.bybit_local.data_consumers.market_info import get_best_bids_and_asks_for_symbols, generate_trade_subscription_pool
from exchanges_integration.bybit_local.utils import websocket_connector_prod
load_dotenv()
"""
Possibilities to add here: 

    Source of data:
    whale wallet analysis
    sentiment analysis of some main social accounts
    mining and transaction volume


Must Implement:
    visualization tools matplotlib
    pandas to visualize data

"""




API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")



async def client_factory(api_key: str, secret_key: str) -> AsyncClient:
    client = await AsyncClient.create(api_key, secret_key)
    return client


async def main():
    print("trying to connect to binance...")
    print(API_KEY, SECRET_KEY)
    client = await client_factory(API_KEY, SECRET_KEY)
    print("logged in to binance")

    print("\n\ntrying to connect to bybit...")
    session = HTTP(
    endpoint=os.getenv("BYBIT_ENDPOINT"),
    api_key=os.getenv("BYBIT_API_KEY"),
    api_secret=os.getenv("BYBIT_API_SECRET"),
)
    print("logged in to bybit")
    
    print("Starting program...")
    print("\n\n Starting data collection...")
    print("collecting data from binance to check for arbitrage...")
    ## Binance ##
    binance_time = await client.get_server_time()
    binance_prices = await get_orderbook_ticks(client, symbol="BTCUSDT")
    exchange_data = [{"exchange_name": "binance", "data": binance_prices}]
    
    print("binance data collected")

    print("collecting data from bybit to check for arbitrage...")
    ## Bybit ##
    bybit_time = session.server_time()["time_now"]
    bybit_prices = get_best_bids_and_asks_for_symbols(session, symbols=["BTCUSDT", "ETHUSDT", "MATICUSDT"])
    
    exchange_data.append({"exchange_name": "bybit", "data": bybit_prices})

    print("Finished collecting data from bybit")
    print("\n Data collection finished")

    print("\n\n Starting data processing...")
    bids, asks = await generate_ordered_trades_for_each_exchange(exchange_data)
    print("\n Finished Ordering Bids and Asks from all Exchanges!")
    
    
    print("\n\n Starting data analysis...")
    print("no action to take...")
    print("\n Finished data analysis")

    print("\n\n Starting data storage...")
    
    print("BYBIT TIME: ", bybit_time)
    print("BINANCE TIME: ", binance_time)
    print("\nBIDS", bids)
    print("ASKS", asks)
    await client.close_connection()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())