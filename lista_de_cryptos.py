from binance_local.consultas import LISTA_DE_PARES
cryptos = []
for par in LISTA_DE_PARES:
    cryptos.append(par[:-4]) #quito el USDT

cryptos = sorted(cryptos)

simbols = []
for i in cryptos:
    simbols.append(i+"USDT")
paresUSDT = dict(zip(cryptos,simbols))

def obtener_par(par):
        return paresUSDT[par]

#if __name__ == "__main__":
#    obtener_par()
