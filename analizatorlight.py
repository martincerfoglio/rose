from numpy import nan
from discord_local.new_extract_content import search_words
import discord_local.palabras_filtro as pf
from logs import to_logs
from globales import channelid
import lista_de_cryptos as lc
import re
from datetime import datetime

def algoritmo1_texto(texto):
    """
                 Busca en orden PRIMARY_ENTRY, ENTRIES, lista de cryptos.
                 Luego filtra de acuerdo a FORBIDDEN y busca si
                 esta la palabra SHORT. Si es asi entonces es un
                 short y si no es un long.
    """
    if type(texto) != str:
        return 'nada','nada','nada'
    else:
        texto = texto.upper()
        primary_entry = search_words(words=pf.PRIMARY_ENTRY,string=texto)
        entry = search_words(words=pf.ENTRIES,string=texto)
        crypto = search_words(words=lc.cryptos,string=texto)
        short = search_words(words=pf.SHORT,string=texto)
        forbidden = search_words(words=pf.FORBIDDEN,string=texto)
        largo = 'LONG'
        corto = 'SHORT'
        
        if crypto != None:
            if entry != None:
                if primary_entry != None:
                    if forbidden == None:
                        if short == None:
                            comentario = 'Long de ' + crypto
                            return crypto, largo, comentario
                        else:
                            comentario = 'Short de ' + crypto        
                            return crypto, corto, comentario
                    else:
                        comentario = crypto + ' con palabra prohibida: ' + forbidden 
                        return crypto, 'nada', comentario
                else:
                    comentario = crypto + ' sin primary entry'
                    return crypto, 'nada', comentario
            else:
                comentario = crypto + ' sin entry'
                return crypto, 'nada', comentario
        else:
            comentario = 'sin Crypto'
            return 'nada', 'nada', comentario

def algoritmo2_texto(texto):
    """
                 Busca en orden lista de cryptos, PRIMARY_ENTRY, que tenga números
                 y que tenga un Stop Loss.
                 Luego filtra de acuerdo a FORBIDDEN y busca si
                 esta la palabra SHORT. Si es asi entonces es un
                 short y si no es un long.
    """
    if type(texto) != str:
        return 'nada','nada','nada'
    else:
        texto = texto.upper()
        #entry = search_words(words=pf.ENTRIES,string=texto)
        entry = 'DALE NOMAS'
        crypto = search_words(words=lc.cryptos,string=texto)
        numeros = re.search('[0-9]\.?[0-9]',texto)
        sl = search_words(words=['SL', 'STOP'],string=texto)
        primary_entry = search_words(words=pf.PRIMARY_ENTRY,string=texto)
        short = search_words(words=pf.SHORT,string=texto)
        forbidden = search_words(words=pf.FORBIDDEN,string=texto)
        largo = 'LONG'
        corto = 'SHORT'
        if crypto != None:
            if primary_entry != None:
                if numeros != None:
                    if sl != None:
                        if forbidden == None:
                            if short == None:
                                comentario = 'Long de ' + crypto
                                return crypto, largo, comentario
                            else:
                                comentario = 'Short de ' + crypto 
                                return crypto, corto, comentario
                        else:
                            comentario = crypto + ' con palabra prohibida: ' + forbidden
                            return crypto, 'nada', comentario
                    else:
                        comentario = crypto + ' no hay SL o TP'
                        return crypto, 'nada', comentario
                else:
                    comentario = crypto + ' sin cifras'
                    return crypto, 'nada', comentario
            else:
                comentario = crypto + ' sin primary entry'
                return crypto, 'nada', comentario
        else:
            comentario = 'sin Crypto'
            return 'nada', 'nada', comentario

def algoritmo3_texto(texto):
    ''' 
        Toma como entrada un strg de texto 
        y lo analiza con los dos algoritmos para texto
    '''
    crypto,longshort,comentario = algoritmo1_texto(texto)
    if longshort != 'nada':
        return crypto,longshort,comentario
    else:
        crypto,longshort,comentario = algoritmo2_texto(texto)
        return crypto,longshort,comentario

def algoritmo_rose_trades_texto(texto):
    """
                 Busca en orden PRIMARY_ENTRY, ENTRIES, lista de cryptos.
                 Luego filtra de acuerdo a FORBIDDEN y busca si
                 esta la palabra SHORT. Si es asi entonces es un
                 short y si no es un long.
    """
    if type(texto) != str:
        return 'nada','nada','nada'
    else:
        texto = texto.upper()
        primary_entry = search_words(words=pf.PRIMARY_ENTRY_ROSE_TRADES,string=texto)
        entry = search_words(words=pf.ENTRIES_ROSE_TRADES,string=texto)
        hashtag_crypto = search_words(words=["#"+crypto for crypto in lc.cryptos],
                                      string=texto) #El '#' es porque rose-trades lo ponen asi
        try:
            crypto = hashtag_crypto[1:]
        except:
            crypto = None
        short = search_words(words=pf.SHORT,string=texto)
        forbidden = search_words(words=pf.FORBIDDEN,string=texto)
        largo = 'LONG'
        corto = 'SHORT'
        
        if crypto != None:
            if entry != None:
                if primary_entry != None:
                    if forbidden == None:
                        if short == None:
                            comentario = 'Long de ' + crypto
                            return crypto, largo, comentario
                        else:
                            comentario = 'Short de ' + crypto        
                            return crypto, corto, comentario
                    else:
                        comentario = crypto + ' con palabra prohibida: ' + forbidden 
                        return crypto, 'nada', comentario
                else:
                    comentario = crypto + ' sin primary entry'
                    return crypto, 'nada', comentario
            else:
                comentario = crypto + ' sin entry'
                return crypto, 'nada', comentario
        else:
            comentario = 'sin Crypto'
            return 'nada', 'nada', comentario
