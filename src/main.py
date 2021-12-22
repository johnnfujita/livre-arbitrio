from dotenv import load_dotenv
import os
from binance import AsyncClient
import asyncio
import time
import json
from pybit import HTTP
from operator import itemgetter
from datetime import datetime

from sqlalchemy.sql.sqltypes import BigInteger


# Exchange Integration Functions
from exchanges_integration.bybit_local.data_consumers.market_info import (
    get_best_bids_and_asks_for_symbols,
    generate_trade_subscription_pool,
)
from exchanges_integration.bybit_local.utils import websocket_connector_prod
from exchanges_integration.binance_local.data_consumers.market_info import (
    get_ticks,
    get_orderbook_ticks,
)
from exchanges_integration.kraken_local.utils import get_kraken_time


## Data processing Functions
from data_processing.multiapi_data_normalizer import (
    generate_ordered_trades_for_each_exchange,
    kafka_serializer,
)
from data_processing.binance_data_processing import label_exchange_binance
from data_processing.bybit_data_processing import label_exchange_bybit
from data_processing.kraken_data_processing import label_exchange_kraken

from kafka import KafkaProducer

### POSTGRESQL ###
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Numeric,
    String,
    DateTime,
    Integer,
    Index,
)


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

#### POSTGRESQL PREP ####

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USERNAME")
db_pass = os.getenv("DB_PASSWORD")
db_endpoint_url = os.getenv("DB_ENDPOINT_URL")

metadata = MetaData()


entries = Table(
    "symbol_per_exchange_asks_n_bids",
    metadata,
    Column("entrie_id", Integer(), primary_key=True),
    Column("symbol", String(20), nullable=False),
    Column("highest_ask_value", Numeric(20, 10)),
    Column("highest_ask_exchange", String(50)),
    Column("lowest_bid_value", Numeric(20, 10)),
    Column("lowest_bid_exchange", String(50)),
    Column("lowest_ask_value", Numeric(20, 10)),
    Column("lowest_ask_exchange", String(50)),
    Column("highest_bid_value", Numeric(20, 10)),
    Column("highest_bid_exchange", String(50)),
    Column("start_time", BigInteger()),
    Column("end_time", BigInteger()),
    Index("symbol_3_index", "symbol"),
    Index("end_time_3_index", "end_time"),
)


engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pass}@{db_endpoint_url}:5432/{db_name}"
)
metadata.create_all(engine)
print("Database created")
connection = None
while connection is None:
    try:
        connection = engine.connect()
    except Exception as e:
        print(e)
        print("Retrying...")
        connection = None

### POSTGRESQL PREP END ###

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "MATICUSDT",
    "ADAUSDT",
    "ALGOUSDT",
    "DOGEUSDT",
    "DOTUSDT",
    "SOLUSDT",
]
symbols_kraken = [
    "BTCUSD",
    "ETHUSD",
    "MATICUSD",
    "ADAUSD",
    "ALGOUSD",
    "DOGEUSD",
    "DOTUSD",
    "SOLUSD",
]
symbols_extra = []


async def client_factory(api_key: str, secret_key: str) -> AsyncClient:

    try:
        client = await AsyncClient.create(api_key, secret_key)
    except Exception as e:
        print(e)
        print("Retrying...")
        client_factory()
    return client


async def main():
    ## Kafka Producer ##
    # producer = KafkaProducer(
    #     bootstrap_servers=[os.getenv("KAFKA_BROKER_URL")],
    #     value_serializer=kafka_serializer,
    # )

    data = {}
    print("trying to connect to binance...")

    client = await client_factory(API_KEY, SECRET_KEY)
    print("logged in to binance")

    print("\n\ntrying to connect to bybit...")
    session = None
    while session is None:
        try:
            session = HTTP(
                endpoint=os.getenv("BYBIT_ENDPOINT"),
                api_key=os.getenv("BYBIT_API_KEY"),
                api_secret=os.getenv("BYBIT_API_SECRET"),
            )
        except Exception as e:
            print(e)
            print("retrying...")
            time.sleep(5)

    print("logged in to bybit")

    print("Starting program...")
    print("\n\nStarting data collection...")
    print("collecting data from binance to check for arbitrage...")

    while True:
        exchange_data = []
        exchange_time = []
        total_processing_time = None
        ## Binance ##

        binance_data = await label_exchange_binance(client, symbols=symbols)
        binance_time = None
        while not binance_time:
            try:
                binance_time = await client.get_server_time()
            except Exception as e:
                print(e)
                print("retrying...")
                time.sleep(5)
        binance_time = binance_time["serverTime"]

        if binance_data:
            exchange_data.append(binance_data)

        print("binance data collected")

        ### Kraken ##
        print("collecting data from kraken to check for arbitrage...")
        kraken_data = await label_exchange_kraken(symbols=symbols_kraken)

        kraken_time = None
        while not kraken_time:
            try:
                kraken_time = await get_kraken_time()
            except Exception as e:
                print(e)
                print("retrying...")
                time.sleep(5)

        if kraken_data:
            exchange_data.append(kraken_data)
        print("kraken data collected")

        ## Bybit ##
        print("collecting data from bybit to check for arbitrage...")
        bybit_data = await label_exchange_bybit(session, symbols=symbols)
        bybit_time = None
        while bybit_time is None:
            bybit_time = session.server_time()["time_now"]
        if bybit_data:
            exchange_data.append(bybit_data)
        print("bybit data collected")
        print("\nData collection finished")

        print("\n\nStarting data processing...")
        bids, asks = await generate_ordered_trades_for_each_exchange(exchange_data)
        print("Finished Ordering Bids and Asks from all Exchanges!")

        ### DATA ANALYSIS ###
        print("\n\nStarting data analysis...")

        # LIST OF ENTRIES TO INSERT INTO DB
        entries_list = []

        for key in bids.keys():
            entry = {}
            entry["symbol"] = key
            entry["highest_ask_value"] = max(asks[key], key=itemgetter(1))[1]
            entry["highest_ask_exchange"] = max(asks[key], key=itemgetter(1))[0]
            entry["lowest_bid_value"] = min(bids[key], key=itemgetter(1))[1]
            entry["lowest_bid_exchange"] = min(bids[key], key=itemgetter(1))[0]
            entry["lowest_ask_value"] = min(asks[key], key=itemgetter(1))[1]
            entry["lowest_ask_exchange"] = min(asks[key], key=itemgetter(1))[0]
            entry["highest_bid_value"] = max(bids[key], key=itemgetter(1))[1]
            entry["highest_bid_exchange"] = max(bids[key], key=itemgetter(1))[0]
            entry["start_time"] = binance_time
            entry["end_time"] = int(round(time.time() * 1000))

            print("COIN: ", key)
            print("highest_ask_value: ", entry["highest_ask_value"])
            print("highest_ask_exchange: ", entry["highest_ask_exchange"])
            print("lowest_bid_value: ", entry["lowest_bid_value"])
            print("lowest_bid_exchange: ", entry["lowest_bid_exchange"])
            print("lowest_ask_value: ", entry["lowest_ask_value"])
            print("lowest_ask_exchange: ", entry["lowest_ask_exchange"])
            print("highest_bid_value: ", entry["highest_bid_value"])
            print("highest_bid_exchange: ", entry["highest_bid_exchange"])
            print("start_time: ", entry["start_time"])
            print("end_time: ", entry["end_time"])
            print("\n")
            entries_list.append(entry)
        print("entries_list: ", entries_list)

        print("no action to take...")
        print("Finished data analysis")

        ### DATA STORAGE ###
        print("\n\nStarting data storage...")

        ins = entries.insert()

        print("Database connected")
        result = connection.execute(ins, entries_list)

        print(result)

        print("BYBIT TIME: ", bybit_time)
        print("BINANCE TIME: ", binance_time)
        print("KRAKEN TIME: ", kraken_time)
        print(
            "TIMEDELTA: ",
            int(float(bybit_time) * 1000) - int(float(binance_time)),
        )
        # print("\n\n Complete data:", data)
        # print("\nBIDS", bids)
        # print("\nASKS", asks)

        print(f"\n\nTime: {datetime.now()}\nSending data to kafka...")

        # producer.send(os.getenv("KAFKA_TOPIC"), data)
        time.sleep(0.5)

    print("\n\n Closing Connection and Shutting program down.")
    await client.close_connection()
    print("Database connected")
    connection.close()
    print("Database closed")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
