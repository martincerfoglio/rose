import logging
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
from binance.error import ClientError
from globales import *
import time
import requests

key = llave_en_uso
secret = secreto_en_uso

um_futures_client = UMFutures(key=key, secret=secret)

def obtener_balance():
    """Devuelve un float con el saldo en udst disponible para ser gastado. 
    Si hay algo comprometido en una orden no va a estar disponible"""
    data = um_futures_client.balance(recvWindow=6000)
    usdt_balance = float(next(item['availableBalance'] for item in data if item['asset'] == 'USDT'))
    return usdt_balance

def consultar_precio_ts(par):
    response = um_futures_client.ticker_price(par)    
    return (response['price'],response['time'])


def apalancar(par='',palanca=1):
    response = um_futures_client.change_leverage(symbol=par, leverage=palanca, recvWindow=6000)
    print(response)

def obtener_precio_de_entrada(symbol):
    result = um_futures_client.account(recvWindow=6000)
    position = next((position for position in result['positions'] if position['symbol'] == symbol), None)
    position = position["entryPrice"]
    return position

def consultar_precio(par):
    response = um_futures_client.ticker_price(par)    
    return (response['price'],response['time'])


def obtener_tamanio_de_la_pos(symbol):
    result = um_futures_client.account(recvWindow=6000)
    position = next((position for position in result['positions'] if position['symbol'] == symbol), None)
    position = position["positionAmt"]
    return position

def quantity(ajuste, saldo, apalancamiento, precio):
    cantidad= ajuste*saldo*apalancamiento/precio
    return cantidad

def lista_de_pares_y_precios_from_requests(tipo_par = None ,pares_prohibidos=None):
    api = 'https://fapi.binance.com/fapi/v1/ticker/price'
    data_prices = requests.get(api)
    data_prices_list_dict_total = data_prices.json()
    #TODO: Terminar de hacer esta funcion y terminar  get_all_prices con la info de esta funcion y definir aca abajo LISTA_DE_PARES
    data_prices_list_dict_teniendo_en_cuenta_prohibidos = []
    if pares_prohibidos != None:
        for item in data_prices_list_dict_total:
            par = item['symbol']
            if par not in pares_prohibidos:
                if tipo_par == None:
                    data_prices_list_dict_teniendo_en_cuenta_prohibidos.append(item)
                else:
                    if par[len(par)-len(tipo_par):]==tipo_par:
                        data_prices_list_dict_teniendo_en_cuenta_prohibidos.append(item)
    else:
        data_prices_list_dict_teniendo_en_cuenta_prohibidos =data_prices_list_dict_total 
    print('\n')
    #print('PARES Y PRECIOS: ', data_prices_list_dict_teniendo_en_cuenta_prohibidos)
    return data_prices_list_dict_teniendo_en_cuenta_prohibidos

LISTA_DE_PARES = []
print('\n')
# print('LOADING CRYPTOS...')
DATA_PRICES_LIST_DICT_TENIENDO_EN_CUENTA_PROHIBIDOS =lista_de_pares_y_precios_from_requests(tipo_par ='USDT' ,pares_prohibidos=PARES_PROHIBIDOS) 
for item in DATA_PRICES_LIST_DICT_TENIENDO_EN_CUENTA_PROHIBIDOS:
    LISTA_DE_PARES.append(item['symbol'])
LISTA_DE_PARES = sorted(LISTA_DE_PARES)

