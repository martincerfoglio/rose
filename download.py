import wget
import zipfile
import sys
import os
from globales import channel_folder

#ejemplo de url trades https://data.binance.vision/data/futures/um/daily/trades/BATUSDT/BATUSDT-trades-2021-06-22.zip'
#ejemplo de url 15m 'https://data.binance.vision/data/futures/um/daily/markPriceKlines/AAVEUSDT/15m/AAVEUSDT-15m-2023-11-09.zip'
#tipo: "trades" o "15m"

def get_csv(crypto, timestamp):
    url_base = 'https://data.binance.vision/data/futures/um/daily/trades/'
    par = crypto + 'USDT'
    fecha = timestamp[0:10]
    url = url_base + par + '/' + par +'-trades-' + fecha + '.zip'    
    local_file = './zips/' + channel_folder + par + fecha + '.zip'
    print(url)

    if os.path.exists(local_file):
        print(f"Ya existe un archivo para {par} en la fecha {fecha}. No es necesario descargarlo nuevamente.")
        return
    
    #descarga el archivo
    wget.download(url, local_file)
    cwd = os.getcwd()
    sys.path.append(os.path.dirname(os.path.abspath(cwd)))
    ruta = cwd + '/csvs/' + channel_folder
    archivo = local_file
    with zipfile.ZipFile(archivo, 'r') as zip_ref:
        zip_ref.extractall(ruta)



