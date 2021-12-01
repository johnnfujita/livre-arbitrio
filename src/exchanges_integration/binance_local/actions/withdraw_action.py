from binance.exceptions import BinanceAPIException
from binance import AsyncClient
from typing import Optional

################################################################################
#                                                                              #
#                  THIS SUBMODULE THAT JUST WITHDRAW CURRENCY                  #
#                                                                              #
#------------------------------------------------------------------------------#
#                                 withdraw                                     #
################################################################################


async def withdraw(client: AsyncClient, coin: str, address: str, amount: float):
    try:
        withdraw_result = await client.withdraw(coin=coin, address=address, amount=amount)
    except BinanceAPIException as e:
        print(e)
    else:
        print("Success")
        return withdraw_result




