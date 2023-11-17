import time
import apalancamientos
from binance_local import consultas
from binance_local import get_all_prices
import lista_de_cryptos
from logs import to_logs
from globales import AJUSTE, SALDO
##la idea es tener armada la cantidad que se va a comprar de cada cosa de antemano
ajuste = AJUSTE
saldo = SALDO
#consultas.obtener_balance()
apalancamiento = apalancamientos.apalancamiento
dict_de_precios_ts = get_all_prices.dict_de_precios_ts
pares = lista_de_cryptos.simbols

cantidades =[]
tss =[]
PARES_CON_PRECISION = {}

def dCount(no_str):
    """
    Cantidad de digitos despues del punto para calcular precision.
    """
    if "." in no_str:
         return len(no_str.split(".")[1].rstrip("0"))
    else:
         return 0

for i in pares:
    cantidades.append(int(round(consultas.quantity(ajuste, saldo, apalancamiento, dict_de_precios_ts[i][0]),0)))
    tss.append(dict_de_precios_ts[i][1])
    PARES_CON_PRECISION[i]= dCount(str(dict_de_precios_ts[i][0]))
    #print('error de ' + i)


dict_de_cantidades = dict(zip(pares,cantidades))
dict_de_tiempos = dict(zip(pares,tss))

def obtener_cantidad(par):
    return dict_de_cantidades[par]

print('\n')
print('DICT DE CANTIDADES: ',dict_de_cantidades)
print('\n')
print('DICT DE PRECISIONES: ',PARES_CON_PRECISION)
to_logs(dict_de_cantidades, 'log_de_cantidades.csv')
to_logs(dict_de_tiempos, 'log_de_tiempos_del_precio.csv')

try:
    assert sorted(consultas.LISTA_DE_PARES) == sorted(list(PARES_CON_PRECISION.keys()))
    print('\n')
    print("TODAS LAS CRYPTOS CARGADAS.")
    print('\n')
    print("WAITING FOR SIGNAL...")
    print('\n')
except:
    print('\n')
    print("ALGUNAS CRYPTOS NO FUERON CARGADAS.")
    print('\n')
