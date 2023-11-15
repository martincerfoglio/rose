import requests
import json

from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from globales import *
import pandas as pd

def apalacar(par='',palanca=1):
    request_client = RequestClient(api_key=llave_en_uso, 
    secret_key=secreto_en_uso)
    result = request_client.change_initial_leverage(symbol=par, leverage=palanca)

def obtener_balance():
    request_client = RequestClient(api_key=llave_en_uso, 
    secret_key=secreto_en_uso)
    result = request_client.get_balance()
    df = pd.DataFrame([t.__dict__ for t in result])
    saldo= df.loc[1]["balance"]
    return saldo

def obtener_precio_de_entrada(par):
    request_client = RequestClient(api_key=llave_en_uso, secret_key=secreto_en_uso)
    result = request_client.get_position()
    df = pd.DataFrame([t.__dict__ for t in result])
    return df[df['symbol']==par]['entryPrice'].iloc[0]

def consultar_precio_ts(par):
    request_client = RequestClient(api_key=llave_en_uso, 
    secret_key=secreto_en_uso)
    result = request_client.get_symbol_price_ticker(symbol=par)
    df = pd.DataFrame([t.__dict__ for t in result])
    precio=df.loc[0]['price']
    ts=df.loc[0]['time']
    precio_ts=(precio,ts)
    return precio_ts

def obtener_tamanio_de_la_pos(par):
    request_client = RequestClient(api_key=llave_en_uso, secret_key=secreto_en_uso)
    result = request_client.get_position()
    df = pd.DataFrame([t.__dict__ for t in result])
    return df[df['symbol']==par]['positionAmt'].iloc[0]

def quantity(ajuste, saldo, apalancamiento, precio):
    cantidad= ajuste*saldo*apalancamiento/precio
    return cantidad

def orden_abierta():
    request_client = RequestClient(api_key=llave_en_uso, secret_key=secreto_en_uso)
    result = request_client.get_open_orders()
    df = pd.DataFrame([t.__dict__ for t in result])
    return df['orderId'][0]



def obtener_informacion_exchange():
    request_client = RequestClient(api_key=llave_en_uso, secret_key=secreto_en_uso)
    result = request_client.get_exchange_information()
    #df = pd.DataFrame([t.__dict__ for t in result])
    #return df[df['symbol']==par]['positionAmt'].iloc[0]
    return result

def lista_de_pares_from_info_exchange(resultado_de_informacion_exchange,tipo_par='USDT',pares_prohibidos=None):
    cantidad_of_symbols = len(resultado_de_informacion_exchange.symbols)
    list_de_pares = []
    if pares_prohibidos != None:
        for i in range(cantidad_of_symbols):
            par =  resultado_de_informacion_exchange.symbols[i].symbol
            if par not in pares_prohibidos:
                if par[len(par)-len(tipo_par):]==tipo_par:
                    list_de_pares.append(par)
    else:
        for i in range(cantidad_of_symbols):
            par=resultado_de_informacion_exchange.symbols[i].symbol
            if par[len(par)-len(tipo_par):]==tipo_par:
                list_de_pares.append(par)
    return list_de_pares


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


#Si uno quiere obtener la lista de pares directo del info exchange descomentar:
#INFO_EXCHANGE  = obtener_informacion_exchange()
#LISTA_DE_PARES = sorted(lista_de_pares_from_info_exchange(INFO_EXCHANGE,tipo_par='USDT',pares_prohibidos=PARES_PROHIBIDOS))

LISTA_DE_PARES = []
print('\n')
print('LOADING CRYPTOS...')
DATA_PRICES_LIST_DICT_TENIENDO_EN_CUENTA_PROHIBIDOS =lista_de_pares_y_precios_from_requests(tipo_par ='USDT' ,pares_prohibidos=PARES_PROHIBIDOS) 
for item in DATA_PRICES_LIST_DICT_TENIENDO_EN_CUENTA_PROHIBIDOS:
    LISTA_DE_PARES.append(item['symbol'])
LISTA_DE_PARES = sorted(LISTA_DE_PARES)
#print('\n')
#print('TOTAL LISTA DE PARES :',len(LISTA_DE_PARES) )
#print('\n')


