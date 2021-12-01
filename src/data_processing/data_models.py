from pydantic import BaseModel
import datetime
from typing import List, Optional

class BinanceModel(BaseModel):
    event_time:int
    symbol:str
    last_price: float
    last_quantity: float
    price_change: float
    price_change_percent: float
    open_price: float
    high: float
    low: float
    volume: float
    quote_volume: float

class GenericTickModel(BaseModel):
    event_time: str
    buy_price: float
    sell_price: float
    exchange_name: str
    symbol: str
    buy_quantity: float
    sell_quantity: float

class BybitSubscriptionModelV1(BaseModel):
    topic: str
    event: str
    symbol: str
    params: dict

class BybitParamsV2(BaseModel):
    symbol: str
    binary: bool = False
    kline_type: Optional[str] = None


class BybitSubscriptionModelV2(BaseModel):
    topic: str
    event: str
    

    