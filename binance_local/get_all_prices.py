import requests
import json

#import concurrent.futures
from binance_local import consultas
import lista_de_cryptos

pares = lista_de_cryptos.simbols
precios_ts =[]


#precios_ts_futures=[]
#with concurrent.futures.ThreadPoolExecutor(max_workers=(50)) as executor:
#    for i in pares:
#        precios_ts_futures.append(executor.submit(consultas.consultar_precio_ts,i))
#for i in precios_ts_futures:
#    precios_ts.append(i.result())

for par in pares:
    for item in consultas.DATA_PRICES_LIST_DICT_TENIENDO_EN_CUENTA_PROHIBIDOS:
        if item['symbol'] == par:   
            precios_ts.append((float(item['price']),item['time'])) #Notar el float


#print('precios_ts', precios_ts)        
dict_de_precios_ts = dict(zip(pares,precios_ts))
print('DICT_DE_PRECIOS_TS: ', dict_de_precios_ts)
