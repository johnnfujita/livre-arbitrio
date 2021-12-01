from binance.exceptions import BinanceAPIException
from binance import AsyncClient
from typing import Optional


################################################################################
#                                                                              #
#                  THIS SUBMODULE DEALS WITH ACCOUNT INFO                      #
#                                                                              #
#------------------------------------------------------------------------------#
#         balance, deposit_history, withdrawal_history, deposit_address        #
################################################################################

async def get_account_info(client: AsyncClient):
    """
    Get the account info
    """
    return await client.get_account()

async def get_balance(client: AsyncClient, symbol: str):
    """
    Get the balance of a symbol
    """
    return await client.get_asset_balance(asset=symbol)

async def fetch_deposit_history(client: AsyncClient, coin: Optional[str] = None):
    if coin:
        try:
            deposit_history = await client.get_deposit_history(coin=coin)
        except BinanceAPIException as e:
            print(e)
        else:
            print("Success")
            return deposit_history
    else:
        try:
            deposit_history = await client.get_deposit_history()
        except BinanceAPIException as e:
            print(e)
        else:
            print("Success")
            return deposit_history


async def fetch_withdrawal_history(client: AsyncClient, coin: Optional[str] = None):
    if coin:
        try:
            withdrawal_history = await client.get_withdraw_history(coin=coin)
        except BinanceAPIException as e:
            print(e)
        else:
            print("Success")
            return withdrawal_history
    else:
        try:
            withdrawal_history = await client.get_withdraw_history()
        except BinanceAPIException as e:
            print(e)
        else:
            print("Success")
            return withdrawal_history


async def get_deposit_address(client: AsyncClient, coin: str):
    try:
        deposit_address = await client.get_deposit_address(coin=coin)
    except BinanceAPIException as e:
        print(e)
    else:
        print("Success")
        return deposit_address
