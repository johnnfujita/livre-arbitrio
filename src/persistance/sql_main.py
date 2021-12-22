import asyncio
from datetime import datetime


# from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os
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

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USERNAME")
db_pass = os.getenv("DB_PASSWORD")
db_endpoint_url = os.getenv("DB_ENDPOINT_URL")

metadata = MetaData()


entries = Table(
    "highest_lowest_asks_bids_per_coin_per_exchange",
    metadata,
    Column("entrie_id", Integer(), primary_key=True),
    Column("coin", String(6), nullable=False),
    Column("highest_ask_value", Numeric(20, 10)),
    Column("highest_ask_exchange", String(50)),
    Column("lowest_bid_value", Numeric(20, 10)),
    Column("lowest_bid_exchange", String(50)),
    Column("lowest_ask_value", Numeric(20, 10)),
    Column("lowest_ask_exchange", String(50)),
    Column("highest_bid_value", Numeric(20, 10)),
    Column("highest_bid_exchange", String(50)),
    Column("start_time", DateTime()),
    Column("close_time", DateTime(), default=datetime.utcnow),
    Index("coin_index", "coin"),
    Index("close_time_index", "close_time"),
)


# async def async_main():
# engine = create_async_engine(
# "postgresql+asyncpg://db_user:db_pass@db_endpoint_url:5432/db_endpoint_url",
# echo=True,
# future=True
# )
# async with engine.begin() as conn:
# await conn.run_sync(meta.drop_all)
# await conn.run_sync(meta.create_all)

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/mydb")
metadata.create_all(engine)
print("Database created")

connection = engine.connect()

highest_ask_value = 0.0
highest_ask_exchange = ""
lowest_bid_value = 0.0
lowest_bid_exchange = ""
lowest_ask_value = 0.0
lowest_ask_exchange = ""
highest_bid_value = 0.0
highest_bid_exchange = ""


ins = entries.insert().values(
    highest_ask_value=highest_ask_value,
    highest_ask_exchange=highest_ask_exchange,
    lowest_bid_value=lowest_bid_value,
    lowest_bid_exchange=lowest_bid_exchange,
    lowest_ask_value=lowest_ask_value,
    lowest_ask_exchange=lowest_ask_exchange,
    highest_bid_value=highest_bid_value,
    highest_bid_exchange=highest_bid_exchange,
)
print(str(ins.compile().params))

print("Database connected")
connection.close()
print("Database closed")
