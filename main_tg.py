from telethon import TelegramClient, events
import telethon.sync
import os
import sys
from logs import to_logs
import time
from datetime import datetime
import pandas as pd
import analizatorlight
import time
from datetime import datetime
from logs import to_logs
from globales import channelid, token, REFRESH_DISCORD, OPERACION, FORCE_TIPO_ENTRY, BUENOS_AUTORES, BUENA_OPERACION, MALOS_AUTORES
from globales import MARGEN_DE_GANANCIA_ESTANDAR, MARGEN_DE_PERDIDA_ESTANDAR, BUEN_MARGEN_DE_GANANCIA, BUEN_MARGEN_DE_PERDIDA, CALLBACK
import pandas as pd
#no sacar main_cantidades, carga el dict de cantidades!!
import main_cantidades
import funciones_v2 as funciones
from binance_local import precision
from collections import OrderedDict

import asyncio

cwd = os.getcwd()
ruta = cwd + '/logs' + '/'

operacion = OPERACION
force_tipo_entry=FORCE_TIPO_ENTRY

tokenenuso = token
api_id = 6330330
api_hash = '14d15dbe4057afa4c697e79287dd38f7'

client = TelegramClient('martin', api_id, api_hash)
n=[]
async def main():
    me= await client.get_me()
    print(me.stringify())

    username = me.username
    print(username)
    print(me.phone)



@client.on(events.NewMessage)
async def my_event_handler(event):
    # print(event.message)
    # print(event.message.message)
    # print(event.peer_id)
    # print('ID:')
    # print(event.peer_id.channel_id)
    # print(event.date)
    # print(type(event.message.message))
    # if 'hola' in event.raw_text:
    #     await event.reply('hola! esta es una respuesta automatica.')


   

    if str(event.peer_id.channel_id) == '1274714505' or str(event.peer_id.channel_id) == '2141038725':
            # print(event.message)
            print("*******************************************************************************************************************")
            print("Numero de mensaje de la corrida: " + str(len(n)))
            print('Contenido del mensaje: ' + event.message.message)
            ultimo_mensaje = event.message.message
            # print("TS de creacion: " + str(event.date))
            print("Hora recibida: " + str(datetime.now()))
            # print(datetime.now()-event.date+pd.Timedelta(hours=3))

            #if str(event.message.reply_to) ==  'None': #POSIBLE MANERA DE DESCARTAR REPETIDO
            if True:    
                inicio_analisis = datetime.now()
                tupla = analizatorlight.algoritmo_rose_trades_texto(ultimo_mensaje)
                # print("Tiempo de analisis: " + str(datetime.now()-inicio_analisis))
                crypto,longshort,comentario = tupla
                author = 'Rose'
                if crypto != 'nada':
                    if longshort == 'nada':
                        print('No se determino longshort por '+comentario)
                        
                    else:
                        par_a_operar=crypto+'USDT'
                        operacion = OPERACION
                        margen_de_perdida = MARGEN_DE_PERDIDA_ESTANDAR
                        margen_de_ganancia = MARGEN_DE_GANANCIA_ESTANDAR
                        print('Esto hace un '+ longshort+ ' de ' + par_a_operar + ' de una señal de ' + author + ' de tipo ' + operacion)
                        
                        old_stdout = sys.stdout # backup current stdout
                        sys.stdout = open(os.devnull, "w")
                        funciones.operar(par_a_operar=par_a_operar,tipo_entry=longshort, operacion=operacion,
                        margen_de_perdida=margen_de_perdida, margen_de_ganancia=margen_de_ganancia)    
                        sys.stdout = old_stdout 
                        
                        # time.sleep(10)        
                n.append(1)
            
            else:
                print('esta respondido')
            # print(datetime.now()-event.date+pd.Timedelta(hours=3))
            print("*******************************************************************************************************************")
            







client.start()
client.run_until_disconnected()


# with client:
#     #client.loop.run_until_complete(main())
#     client.loop.run_forever()