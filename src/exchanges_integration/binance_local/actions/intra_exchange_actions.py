from binance import AsyncClient


################################################################################
#                                                                              #
#                  THIS SUBMODULE DEALS WITH INTRA BINANCE ACTIONS             #
#                                                                              #
#------------------------------------------------------------------------------#
#                           limit_buy, cancel_order, sell_limit                #
################################################################################

def limit_buy(client: AsyncClient, symbol: str, quantity: int, price: float):
    """
    :param client:
    :param symbol:
    :param quantity:
    :param price:
    :return:
    """
    return client.order_limit_buy(symbol=symbol, quantity=quantity, price=price)


def cancel_order(client: AsyncClient, symbol: str, order_id: str):
    """
    :param client:
    :param symbol:
    :param order_id:
    :return:
    """
    return client.cancel_order(symbol=symbol, orderId=order_id)

def sell_limit(client: AsyncClient, symbol: str, quantity: int, price: float):
    """
    :param client:
    :param symbol:
    :param quantity:
    :param price:
    :return:
    """
    return client.order_limit_sell(symbol=symbol, quantity=quantity, price=price)


def list_open_orders(client: AsyncClient, symbol: str):
    """
    :param client:
    :param symbol:
    :return:
    """
    return client.get_open_orders(symbol=symbol)
