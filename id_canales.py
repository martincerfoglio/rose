from telethon import TelegramClient, events, sync
import time
import pandas as pd
import asyncio


#Se colca el nombre del chat y trae el ID para poder pinguear mensajes
api_id = 6330330
api_hash = '14d15dbe4057afa4c697e79287dd38f7'

client = TelegramClient('session_name', api_id, api_hash)
client.start()

canales = pd.read_csv("canales.csv")

for i in range(len(canales)):
    print(canales["nombre"][i])

    my_private_channel_id = None
    my_private_channel = None

    for dialog in client.iter_dialogs():
        if dialog.name == canales["nombre"][i]:
            my_private_channel = dialog
            my_private_channel_id = dialog.id
            canales["id"][i] = str(my_private_channel_id)
            break

canales.to_csv("canales.csv", index=False)
