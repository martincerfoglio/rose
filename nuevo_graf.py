import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from globales import channel_folder
import numpy as np
from download import get_csv

def obtener_precios_30s_despues(df, timestamp_alerta, segundos_despues=30):
    # Calcular el timestamp para 30 segundos después de la alerta
    timestamp_despues = timestamp_alerta + segundos_despues * 1000

    # Filtrar el DataFrame para obtener los datos 30 segundos después de la alerta
    df_filtrado = df[(df['time'] >= timestamp_alerta) & (df['time'] <= timestamp_despues)]

    # Obtener el precio de compra y venta
    precio_compra = df_filtrado['price'].min()
    precio_venta = df_filtrado['price'].max()

    return precio_compra, precio_venta

def graficar_alerta(alerta, segundos_despues=30):
    # Obtener información de la alerta
    alert_info = alerta.split(',')
    timestamp_alerta = alert_info[2].strip()
    crypto = alert_info[4].strip()

    # Construir la ruta del archivo CSV
    get_csv(crypto,timestamp_alerta)
    print(timestamp_alerta)
    ruta_csv = f'd:\\rose\\csvs\\rose\\{crypto}USDT-trades-{timestamp_alerta[0:10]}.csv'

    try:
        # Intentar leer el DataFrame desde el archivo CSV
        df_cripto = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        print(f"¡Archivo {ruta_csv} no encontrado!")
        return

    # Convertir el timestamp de la alerta a milisegundos
    timestamp_alerta_dt = datetime.strptime(timestamp_alerta, '%Y-%m-%d %H:%M:%S%z')
    timestamp_alerta_str = timestamp_alerta_dt.strftime('%Y-%m-%d_%H-%M-%S')
    plt.figure()

    # Graficar el DataFrame de trades
    plt.plot(df_cripto['time'], df_cripto['price'], label='Precio')

    # Agregar línea vertical en el momento de la alerta
    plt.axvline(x=timestamp_alerta_dt.timestamp() * 1000, color='r', linestyle='--', label='Alerta')

    # Calcular el timestamp para la línea vertical segundos_despues después de la alerta
    timestamp_despues = timestamp_alerta_dt.timestamp() * 1000 + segundos_despues * 1000
    plt.axvline(x=timestamp_despues, color='g', linestyle='--', label=f'{segundos_despues} segundos después')

    # Ajustar el límite del eje x para mostrar 5 segundos antes y segundos_despues después de la alerta
    plt.xlim(np.int64(timestamp_alerta_dt.timestamp() * 1000 - 5000), np.int64(timestamp_despues + 5000))

    # Ajustar el límite del eje y para una escala más ampliada (ajusta estos valores según sea necesario)
    # escala_ampliada = 0.5  # Puedes ajustar este valor según tus necesidades
    # plt.ylim(df_cripto['price'].min() - escala_ampliada, df_cripto['price'].max() + escala_ampliada)

    # Añadir etiquetas y leyenda
    plt.xlabel('Timestamp')
    plt.ylabel('Precio')
    plt.title(f'Gráfico de Trades para {crypto}')
    plt.legend()

    # Guardar la imagen con un nombre compatible con Windows
    plt.savefig(f'./graficos/{channel_folder}{timestamp_alerta_str}_{crypto}_{segundos_despues}s.png')

    # Obtener precios de compra y venta
    precio_inicio, precio_fin = obtener_precios_30s_despues(df_cripto, timestamp_alerta_dt.timestamp() * 1000, segundos_despues)

    if alert_info[5].strip() == 'LONG':
        resultado = (precio_fin-precio_inicio)/precio_inicio
    else:
        resultado = (precio_inicio-precio_fin)/precio_inicio

    string = alerta.strip() + ',' + str(precio_inicio) + ',' + str(precio_fin) + ',' + str(resultado)
   
    with open('resultados.csv', 'a', encoding='utf-8') as f:
        f.write(string + '\n')
               

# Ejemplo de uso con la alerta proporcionada y 30 segundos después
# alerta = "4,18693,2023-11-11 16:16:14+00:00,#DYDX Buy Setup,DYDX,LONG,"
# graficar_alerta(alerta, segundos_despues=30)

nombre_archivo = 'alertas.txt'

with open(nombre_archivo, 'r') as archivo:
    for linea in archivo:
        try:
            graficar_alerta(linea)
        except:
            pass