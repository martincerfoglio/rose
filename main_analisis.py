from download import get_csv
from operation_graph import graficar_alerta
import pandas as pd
from lista_de_cryptos import cryptos

print(cryptos)

df = pd.read_csv('1_Rose Signals - 0.1 BTC to 100 BTC 🌹.csv')

def asignar_tipo(row):
    if 'BUY' in row['message'].upper():
        return 'LONG'
    elif 'SHORT' in row['message'].upper():
        return 'SHORT'
    else:
        return None
    



df['tipo'] = df.apply(asignar_tipo, axis=1)
df['crypto'] = df['message'].str.extract(r'#(\w+)')


df.to_csv('alertas.csv')

for i in range (len(df['crypto'])):
    if df['crypto'][i] == 'BTC':
        pass
    elif df['crypto'][i] == 'ETH':
        pass
    else:
        try:
            get_csv(df['crypto'][i],df['timestamp'][i])
        except:
            print('no se pudo bajar '+ df['crypto'][i] + ' del ' + df['timestamp'][i][0:10])
        try:
            graficar_alerta(df['crypto'][i],df['timestamp'][i],df['user'][i],df['utc_ts'][i],df['content'][i])
        except:
            print('no se pudo graficar '+ df['crypto'][i] + ' del ' + df['timestamp'][i][0:10])