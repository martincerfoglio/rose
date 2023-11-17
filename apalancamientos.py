import lista_de_cryptos
from binance_local import consultas
from globales import APALANCAMIENTO

apalancamiento = APALANCAMIENTO

def cambiar_apalancamientos():
    for i in lista_de_cryptos.simbols:
        consultas.apalacar(i,apalancamiento)


if __name__ == "__main__":
    cambiar_apalancamientos()
