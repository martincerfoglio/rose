from telethon import TelegramClient, events, sync
import time
import pandas as pd


# Este script trae los mensaje de un canal

api_id = 6330330
api_hash = '14d15dbe4057afa4c697e79287dd38f7'

client = TelegramClient('session_name', api_id, api_hash)
client.start()
print(client.get_me().stringify())
#client.send_message('541141726683', 'Hello! Talking to you from Telethon')
#client.download_profile_photo('me')

time_delta = time.time()

dialogos = client.get_dialogs()

df = pd.DataFrame(dialogos)
df.to_csv('dialogos.csv', mode='a')

canales = pd.read_csv("canales.csv")

for i in range(len(canales)):
     nombre = canales['nombre'][i]
     id = canales['id'][i]
     
     with open(str(i)+'_'+nombre+'.txt', 'a', encoding='utf-8') as f:
          for message in client.iter_messages(int(id),limit=1000):
               try: 
                    mensaje = message.text.replace('\n', ' ') 
               except:
                    mensaje = message.text 
               string = str(message.id)+ ',' +str(message.date)+ ','+ str(mensaje)
               
               if "BUY SETUP" in mensaje.upper() or "SHORT SETUP" in mensaje.upper():
                    f.write(string + '\n')
               
     
  

tiempo = time.time() - time_delta 
