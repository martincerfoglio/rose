from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from globales import *
import pandas as pd

def comprar_market(par='',cantidad=0,reducir=False):
    request_client = RequestClient(api_key=llave_en_uso, 
                                secret_key=secreto_en_uso)
    result = request_client.post_order(
                                        symbol=par, 
                                        side=OrderSide.BUY, 
                                        ordertype=OrderType.MARKET,
                                        quantity=cantidad,
                                        reduceOnly=reducir)

def comprar_stop_loss(par='',cantidad=0,precio_stop=1,reducir=False):
    request_client = RequestClient(api_key=llave_en_uso, 
                                   secret_key=secreto_en_uso)
    result = request_client.post_order(
                                        symbol=par, 
                                        side=OrderSide.BUY, 
                                        ordertype=OrderType.STOP, 
                                        timeInForce="GTC",
                                        price=precio_stop,
                                        stopPrice=precio_stop,
                                        quantity=cantidad,
                                        reduceOnly=reducir)

def comprar_take_profit(par='', cantidad=1, preciotp=1,reducir=False):
    request_client = RequestClient(api_key=llave_en_uso, 
                                   secret_key=secreto_en_uso)
    result = request_client.post_order(
                                        symbol=par, 
                                        side=OrderSide.BUY, 
                                        ordertype=OrderType.LIMIT,
                                        timeInForce='GTC',
                                        price=preciotp,
                                        quantity=cantidad,
                                        reduceOnly=reducir)

def buy_trailing_stop(par='', cantidad=1, preciotp=1, callback=0.1, reducir=False):
    request_client = RequestClient(api_key=llave_en_uso, 
                                   secret_key=llave_en_uso)
    result = request_client.post_order(
                                        symbol=par, 
                                        side=OrderSide.BUY, 
                                        ordertype=OrderType.TRAILING_STOP_MARKET,
                                        callbackRate=callback,
                                        timeInForce='GTC',
                                        activationPrice=preciotp,
                                        quantity=cantidad,
                                        reduceOnly=reducir)

def vender_market(par='',cantidad=0,reducir=False):
    request_client = RequestClient(api_key=llave_en_uso, 
                                   secret_key=secreto_en_uso)
    result = request_client.post_order(
                                        symbol=par, 
                                        side=OrderSide.SELL, 
                                        ordertype=OrderType.MARKET, 
                                        quantity=cantidad,
                                        reduceOnly=reducir)

def vender_stop_loss(par='',cantidad=0,precio_stop=1,reducir=False):
    request_client = RequestClient(api_key=llave_en_uso, 
                                   secret_key=secreto_en_uso)
    result = request_client.post_order(
                                        symbol=par, 
                                        side=OrderSide.SELL, 
                                        ordertype=OrderType.STOP, 
                                        timeInForce="GTC",
                                        price=precio_stop,
                                        stopPrice=precio_stop,
                                        quantity=cantidad,
                                        reduceOnly=reducir)

def vender_take_profit(par='', cantidad=1, preciotp=1,reducir=False):
    request_client = RequestClient(api_key=llave_en_uso, 
                                   secret_key=secreto_en_uso)
    result = request_client.post_order(
                                        symbol=par, 
                                        side=OrderSide.SELL, 
                                        ordertype=OrderType.LIMIT,
                                        timeInForce='GTC',
                                        price=preciotp,
                                        quantity=cantidad,
                                        reduceOnly=reducir)

def vender_trailing_stop(par='', cantidad=1, preciotp=1, callback=0.1, reducir=False):
    request_client = RequestClient(api_key=llave_en_uso, 
                                   secret_key=llave_en_uso)
    result = request_client.post_order(
                                        symbol=par, 
                                        side=OrderSide.SELL, 
                                        ordertype=OrderType.TRAILING_STOP_MARKET,
                                        callbackRate=callback,
                                        timeInForce='GTC',
                                        activationPrice=preciotp,
                                        quantity=cantidad,
                                        reduceOnly=reducir)

def cancelar_todas_ordenes(par=''):
    request_client = RequestClient(api_key=llave_en_uso, 
                                   secret_key=llave_en_uso)
    result = request_client.cancel_all_orders(par)

def cancelar_orden(par='',orden=''):
    request_client = RequestClient(api_key=llave_en_uso, 
                                   secret_key=llave_en_uso)
    result = request_client.cancel_order(symbol=par, orderId=orden)
