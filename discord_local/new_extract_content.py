from logs import to_logs
import sys
import os
from numpy import NaN, nan
cwd = os.getcwd()
sys.path.append(os.path.dirname(os.path.abspath(cwd)))
from globales import auth_discord
from globales import discord_url_base
from globales import channelid
import lista_de_cryptos as lc
import requests
import json
import re
import pandas as pd
import time
# import pytesseract
from logs import to_logs
from ast import literal_eval
from PIL import Image, ImageEnhance
import os
cwd = os.getcwd()
# if os.name == 'nt':
#     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# else:
#     pass


def retrieve_content(channelid):
    '''Toma como entradada el canal y devuelve un data frame'''
    headers = {'authorization': auth_discord['authorization'],} 
    url = discord_url_base + '/{}/messages'.format(channelid)
    r = requests.get(url,  
                     timeout=(4, 10),
                     headers = headers)
    if r.status_code == 200:
        print('Connected.')
    elif r.status_code == 404:
        print('Not Found.', ':', url)
    content_list_dict = json.loads(r.text)
    df= pd.DataFrame(content_list_dict, index= None ,columns=['id','timestamp','author','content','attachments','edited_timestamp','message_reference'])
    df = df.set_index('id')
    df = df.sort_values(by='id', ascending=True)
    df = df.replace(r'\r+|\n+|\t+',' ', regex=True) 
    df = df.reset_index()
    return df   

def ultimos_msg_y_df(channelid):
    '''Trae el canal y devuelve el ultimo mensaje, un data frame y el anteultimo mensaje'''
    datos= retrieve_content(channelid)
    ultimo= datos.iloc[-1]
    anteultimo = datos.iloc[-2]
    return ultimo,datos, anteultimo

def cambio_id(ultimo_mensaje,ultimo_id,ultimo_df):
    '''
    Si hay mensaje nuevo devuelve True
    '''
    if ultimo_mensaje['id'] == str(ultimo_id):
        print('No hubo mensaje nuevo')
        return False
    else:
        print('CAMBIO EL MENSAJE, ANALICEMOS!!')
        ultimo_df.to_csv('log.csv')
        return True

def safe_checker(mensaje):
    '''
    Chequea si un mensaje esta editado o referenciado. En ese caso, devuelve True.
    Si el mensaje es apto, devuelve False
    '''
    if mensaje.loc['edited_timestamp'] != None:
        return True
    elif type(mensaje.loc['message_reference']) == dict:
        return True
    else:
        return False

def safe_checker2(mensaje):
    '''
    Chequea si un mensaje tiene attachment. Se usa exclusivamente en el main para ver si el mensaje anterior tiene attachment.
    '''
    try:
        mensaje.loc['attachments'][0] 
        return True
    except:
        return False        

def att_download(url,id):
    '''Descarga la imagen adjunta'''
    r = requests.get(url)
    with open("./images/" + str(id) + ".png", 'wb') as f:
        f.write(r.content)

def cont_checker(ultimo):

    if type(ultimo.loc['content']) == str:
        return True
    else:
        return False

def cont_checker_crudo(ultimo):
    if ultimo.loc['content'] != '':
        return True
    else:
        return False

def att_checker(mensaje):
    if mensaje.loc['attachments'] != '':
        return True
    else:
        False

def search_words(words, string):
    """
    words (list): lista de words
    """
    match = "" 
    L = '(?<![A-Z])'
    R = '(?![A-Z])'
    for word in words:
        match = match + L + word + R + '|'
    match = match[:-1]
    search = re.search(match, string)
    if search:
        resultado=search.group()
        pass
    else:
        resultado=None
    return resultado

# def text_extract(id):
#     img_path = './images/'+ str(id) +'.png'
#     its=pytesseract.image_to_string(img_path)
#     return its

# def text_extractV2(id):
#     if type(id) == str:
#         img_path = './images/'+ str(id) +'.png'
#         its=pytesseract.image_to_string(img_path, config='--psm 11')
        
#         #its=pytesseract.image_to_string(img_path)
#     else:
#         its=pytesseract.image_to_string(id, config='--psm 11')
        
#         #its=pytesseract.image_to_string(id)
#     return its

def get_url(mensaje):
    if type(mensaje.loc['attachments']) == str:
        url = literal_eval(mensaje.loc['attachments'])[0]['url']
    else:
        url = mensaje.loc['attachments'][0]['url']
    return url

def contraste(imagen):
    if type(imagen) == str:
        ruta = cwd + '/images' + '/'
        im = Image.open(ruta+str(imagen)+'.png')
        enhancer = ImageEnhance.Contrast(im)
        factor = 10
        im_output = enhancer.enhance(factor)
        return im_output
    else:
        enhancer = ImageEnhance.Contrast(imagen)
        factor = 10
        im_output = enhancer.enhance(factor)
        return im_output
    # im_output.save(ruta+str(imagen)+'c.png')

def afilador(imagen):
    if type(imagen) == str:
        ruta = cwd + '/images' + '/'    
        im = Image.open(ruta+str(imagen)+'.png')
        enhancer = ImageEnhance.Sharpness(im)
        factor = 10
        im_output = enhancer.enhance(factor)
        return im_output
    else:
        enhancer = ImageEnhance.Sharpness(imagen)
        factor = 10
        im_output = enhancer.enhance(factor)
        return im_output
    # im_output.save(ruta+str(imagen)+'a.png')

def engrisar(imagen):
    if type(imagen) == str:    
        ruta = cwd + '/images' + '/'    
        im = Image.open(ruta+str(imagen)+'.png')
        im_output = im.convert('LA')
        return im_output
    else:
        im_output = imagen.convert('LA')
        return im_output        
    # im_output.save(ruta+str(imagen)+'g.png')

def blancnoir(imagen):
    if type(imagen) == str:
        ruta = cwd + '/images' + '/'    
        im = Image.open(ruta+str(imagen)+'.png')
        enhancer = ImageEnhance.Color(im)
        factor = 0
        im_output = enhancer.enhance(factor)
        return im_output
    else:
        enhancer = ImageEnhance.Color(imagen)
        factor = 0
        im_output = enhancer.enhance(factor)
        return im_output 

def corrector(imagen):
    '''ajuta sharpness y contraste'''
    if type(imagen) == str: 
        ruta = cwd + '/images' + '/'    
        im = Image.open(ruta+str(imagen)+'.png')
        enhancer = ImageEnhance.Sharpness(im)
        factor = 10
        im = enhancer.enhance(factor)
        enhancer = ImageEnhance.Contrast(im)
        im_output = enhancer.enhance(factor)
        return im_output
    else:
        enhancer = ImageEnhance.Sharpness(imagen)
        factor = 10
        im = enhancer.enhance(factor)
        enhancer = ImageEnhance.Contrast(im)
        im_output = enhancer.enhance(factor)
        return im_output
    # im_output.save(ruta+str(imagen)+'x.png')

def puntificador(imagen):
    #TODO: no anda esta mierda
    thresh = 150
    fn = lambda x : 255 if x > thresh else 0
    r = imagen.convert('L').point(fn, mode='1')
    
    if type(imagen) == str:
        ruta = cwd + '/images' + '/'    
        im = ruta+str(imagen)+'.png'
        r = imagen.convert('L').point(fn, mode='1')
        return pytesseract.image_to_string(r, config='--psm 11')
    else:
        r = imagen.convert('L').point(fn, mode='1')
        return pytesseract.image_to_string(r, config='--psm 11')
    



