from binance.um_futures import UMFutures
from globales import *

key = llave_en_uso
secret = secreto_en_uso

um_futures_client = UMFutures(key=key, secret=secret)

def comprar_market(par='',cantidad=0,reducir=False):
    um_futures_client.new_order(
        symbol=par,
        side="BUY",
        type="MARKET",
        quantity=cantidad,
    )

def comprar_stop_loss(par='',cantidad=0,precio_stop=1,reducir=False):
    um_futures_client.new_order(
        symbol=par,
        side="BUY",
        type="STOP",
        timeInForce="GTC",
        price=precio_stop,
        stopPrice=precio_stop,
        quantity=cantidad,
        reduceOnly=reducir
    )
      
def comprar_take_profit(par='', cantidad=1, preciotp=1,reducir=False):
    um_futures_client.new_order(
        symbol=par,
        side="BUY",
        type="LIMIT",
        timeInForce="GTC",
        price=preciotp,
        quantity=cantidad,
        reduceOnly=reducir
    )

def buy_trailing_stop(par='', cantidad=1, preciotp=1, callback=0.1, reducir=False):
    # um_futures_client.new_order(
    #     symbol=par,
    #     side="BUY",
    #     type="LIMIT",
    #     timeInForce="GTC",
    #     price=preciotp,
    #     quantity=cantidad,
    #     reduceOnly=reducir
    # )
    # result = request_client.post_order(
    #                                     symbol=par, 
    #                                     side=OrderSide.BUY, 
    #                                     ordertype=OrderType.TRAILING_STOP_MARKET,
    #                                     callbackRate=callback,
    #                                     timeInForce='GTC',
    #                                     activationPrice=preciotp,
    #                                     quantity=cantidad,
    #                                     reduceOnly=reducir)
    pass

def vender_market(par='',cantidad=0,reducir=False):
    um_futures_client.new_order(
        symbol=par,
        side="SELL",
        type="MARKET",
        quantity=cantidad,
        reduceOnly=reducir
    )

def vender_stop_loss(par='',cantidad=0,precio_stop=1,reducir=False):
    um_futures_client.new_order(
        symbol=par,
        side="SELL",
        type="STOP",
        timeInForce="GTC",
        price=precio_stop,
        stopPrice=precio_stop,
        quantity=cantidad,
        reduceOnly=reducir
    )

def vender_take_profit(par='', cantidad=1, preciotp=1,reducir=False):
    um_futures_client.new_order(
        symbol=par,
        side="SELL",
        type="LIMIT",
        timeInForce="GTC",
        price=preciotp,
        quantity=cantidad,
        reduceOnly=reducir
    )

def vender_trailing_stop(par='', cantidad=1, preciotp=1, callback=0.1, reducir=False):
    # request_client = RequestClient(api_key=llave_en_uso, 
    #                                secret_key=llave_en_uso)
    # result = request_client.post_order(
    #                                     symbol=par, 
    #                                     side=OrderSide.SELL, 
    #                                     ordertype=OrderType.TRAILING_STOP_MARKET,
    #                                     callbackRate=callback,
    #                                     timeInForce='GTC',
    #                                     activationPrice=preciotp,
    #                                     quantity=cantidad,
    #                                     reduceOnly=reducir)
    pass

def cancelar_todas_ordenes():
    um_futures_client.cancel_open_orders(symbol="BTCUSDT", recvWindow=2000)

def cancelar_orden(par='',orden=''):
    um_futures_client.cancel_order(symbol=par, orderId=orden, recvWindow=2000)


