import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from download import get_csv
from pandas._libs.tslibs import timestamps 
from globales import channel_folder
from datetime import datetime

def graficar_alerta(alerta, timestamp,crypto):
    archivo = crypto+'USDT-trades-'+ timestamp[0:10] +'.csv'
    nametime = str(timestamp[0:10])+'_'+str(timestamp[11:13])+'hs'+str(timestamp[14:16])+'min'
    data= pd.read_csv('csvs/' + channel_folder +archivo, sep=',')
    data.columns = ['order', 'price', 'quantity', 'total_money', 'time', 'maker']
    # Obtener información de la alerta
    alert_info = alerta.split(',')
    timestamp_alerta = alert_info[2].strip()
    crypto = alert_info[3].strip()
    tipo_alerta = alert_info[4].strip()

    # Filtrar el DataFrame de trades para la criptomoneda específica
    df_cripto = data.columns[data.columns['symbol'] == crypto]

    # Convertir el timestamp de la alerta a milisegundos
    timestamp_alerta_dt = datetime.strptime(timestamp_alerta, '%Y-%m-%d %H:%M:%S%z')
    timestamp_alerta_ms = int(timestamp_alerta_dt.timestamp() * 1000)

    # Graficar el DataFrame de trades
    plt.plot(df_cripto['time'], df_cripto['price'], label='Precio')

    # Agregar línea vertical en el momento de la alerta
    plt.axvline(x=timestamp_alerta_ms, color='r', linestyle='--', label='Alerta')

    # Añadir etiquetas y leyenda
    plt.xlabel('Timestamp')
    plt.ylabel('Precio')
    plt.title(f'Gráfico de Trades para {crypto}')
    plt.legend()
    

    
    plt.savefig('./graficos/' + channel_folder +str(nametime)+'_'+str(crypto)+'_'+'.png')

    
    
# graficar_alerta('4,18693,2023-11-11 16:16:14+00:00,#DYDX Buy Setup,DYDX,LONG,','2023-11-11 16:16:14+00:00','DYDX')
# '4,18693,2023-11-11 16:16:14+00:00,#DYDX Buy Setup,DYDX,LONG,'
