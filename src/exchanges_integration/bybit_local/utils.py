from pybit import HTTP, WebSocket
from dotenv import load_dotenv
from data_processing.data_models import BybitSubscriptionModelV1

from typing import List

import os
from dotenv import load_dotenv
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")
production_http_url = "https://api.bybit.com"
websocket_url_v1 = os.getenv("BYBIT_WEBSOCKET_BASE_URL_V1")

def http_session_constructor_prod(api_key: str = api_key, api_secret: str= api_secret, endpoint: str=production_http_url, spot: bool=True) -> HTTP:
    """
    Constructor for the HTTP session.
    :param api_key: API key
    :param api_secret: API secret
    :param endpoint: Endpoint URL
    :param spot: True if spot trading, False if margin trading
    :return: HTTP session
    """
    return HTTP(api_key=api_key, api_secret=api_secret, endpoint=endpoint, spot=spot )


def websocket_connector_prod(endpoint: str=websocket_url_v1, subs: List[BybitSubscriptionModelV1]=[], run: bool=False) -> WebSocket:
    """
    Constructor for the WebSocket session.
    :param endpoint: Endpoint URL
    :param subs: List of subscriptions
    :return: WebSocket session
    """
    print(endpoint, subs)
    subs = [sub.json() for sub in subs]
    ws = WebSocket(endpoint, subscriptions=subs)
    if run:
        while True:
            try:
                for idx in range(len(subs)):
                    data = ws.fetch(subs[idx])
                    
                    if data:
                        print(data)
            except Exception as e:
                print(e)
    else:

        return WebSocket(endpoint, subscriptions=subs)