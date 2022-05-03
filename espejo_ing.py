from telethon import TelegramClient, events
from telethon.tl.types import MessageEntityTextUrl, MessageMediaWebPage

phone_number = '525610830260'
api_id = '7504340'
api_hash = 'a2d9b532bfc53b81ae70eb0293944b26'

tgclient = TelegramClient(phone_number, api_id, api_hash)

#traer listas de canales
id_canales_originales =     [-1001528793686, -1001270163214, -1001565883265, -1001541003693, -1001541965194, -1001528628594, -1001504674642, -1001519822361, -1001542175274, -1001245768522, -1001547716942, -1001301789090, -1001464139014, -1001316735978, -1001755807091, -1001524984835, -1001161712269, -1001507554529, -1001512048703, -1001519195868, -1001567732684, -1001557455731, -1001589642816, -1001246629900]
id_canales_copia_ing =      [-1001657550513, -1001750708220, -1001758730481, -1001616457923, -1001772377787, -1001627813158, -1001251261245, -1001632283508, -1001603430632, -1001638187563, -1001575574586, -1001770679920, -1001751711077, -1001530644292, -1001510193991, -1001592557882, -1001506072700, -1001797830280, -1001687280253, -1001735482090, -1001739439895, -1001637115099, -1001648519939, -1001505802921] #-1001637115099
#                              Always Win        The Bull        KIM Crypto      INNER CIRCLE    KILMMEX         HAVEN CBS      HAVEN LOMA    HAVEN KRILLIN   HAVEN PIERRE      CLAY ALTS      CLAY MARGIN    CLAY SCALPING   KRYPTON WOLF       BIRB NEST     ELONTRADES    RATICOIN ALTS   RATICOIN MARGIN BITCOIN BULLETS MARGIN WHALES    ROSE PREMIUM      FAT PIGS     BINANCE KILLERS RUSSIAN INSIDERS   Maverick
nombre_de_canales = ["Always Win", "The Bull", "Kim Crypto", "Inner Circle", "KilMex", "Haven CBS", "Haven Loma", "Haven Krillin", "Haven Pierre", "Alex Clay Alts", "Alex Clay Margin", "Alex Clay Scalping", "Krypton Wolf", "Birb Nest", "Elon Trades", "Raticoin Alts", "Raticoin MArgin", "Bitcoin Bullets", "Margin Whales", "Rose Premium Signal 2022", "Fat Pig Signals", "Binance Killers", "FED Russian Insiders", "Maverick"]
numero_de_canales=len(id_canales_originales)
palabras_prohibidas = ["bahasa", "membership", "indoleaks", "indonesia", "private circle", "Private circle", "Lifetime"]
canales_propios = [-1001519195868]
canal_filtro = -1001710792574
palabra_prohibida = False



print("Se encontraron "+str(numero_de_canales)+" canales por este órden:")
numero = 1
for nombre in nombre_de_canales:
    print(str(numero)+".- "+ nombre)
    numero +=1

#Función para conectar los canales
def conectar_canales(id_Canal_Original_Evento):
    for i in range(0, numero_de_canales):
        #si el id del canal que envió el evento es igual al id del canal original
        if id_Canal_Original_Evento == id_canales_originales[i]:
            #entonces asigna a la variable id_Canal_Copia el numero del valor que coincida en la lista
            id_Canal_Copia = id_canales_copia_ing[i]
            return id_Canal_Copia

def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]

@tgclient.on(events.NewMessage(id_canales_originales))
async def my_event_handler(event):
  
    raw_text = event.raw_text
    text = event.text

    prohibido_detectado = False
    try:
        text = remove_last_line_from_string(text)
    except:
        pass    
    try:
        text = text.replace("- By @Indoleaks -", "")

    except:
        pass 
    try:
        if "-" in text[-5:]:
            text = text[:-3]
    except:
        pass        
    try:
        text = text.replace("Indoleaks", "HispanLeaks")
    except:
        pass

    msg = event.message
    msg_id = event.message.id
    media = event.message.media

    
    id_Canal_Original_Evento = event.chat_id
    #borrar una parte de texto que sobra en Haven CBS
    if id_Canal_Original_Evento == -1001528628594:
        text = text.replace ("by", "")
    id_Canal_Copia = conectar_canales(id_Canal_Original_Evento) 

    for  palabra in palabras_prohibidas:
        raw_text_low = text.lower()
        if palabra in raw_text_low:
            print('si está')
            prohibido_detectado = True    
    #Si hay texto citado
    print(text)
    if prohibido_detectado == False:
        try:
            #obtener el id del mensaje citado en el canal original
            citado_id = event.reply_to.reply_to_msg_id
            iter_msg = await tgclient.get_messages(id_Canal_Original_Evento, limit=50)
            for message in iter_msg:
                if message.id == citado_id:
                    texto_citado = message.text
                    iter_copia = await tgclient.get_messages(id_Canal_Copia, limit=50)
                    for message_ in iter_copia:
                        try:
                            if message_.text == texto_citado:
                                id_msg = message_.id
                                if media != None:
                                    file = await tgclient.download_media(event.message.media, file=bytes)
                                    await tgclient.send_message(id_Canal_Copia, text, file=file, reply_to=id_msg)
                                else:                                        
                                    await tgclient.send_message(id_Canal_Copia, text, reply_to=id_msg)
                                    print("Mensaje citado enviado")
                        except:
                            pass        
        except:
            if media != None:
                file = await tgclient.download_media(event.message.media, file=bytes, thumb=-1)
                await tgclient.send_message(id_Canal_Copia, text, file=file)
            else:    
                await tgclient.send_message(id_Canal_Copia, text) 

    if prohibido_detectado == True:
        if media != None:
            file = await tgclient.download_media(event.message.media, file=bytes)
            await tgclient.send_message(id_Canal_Copia, text, file=file)
        else:    
            await tgclient.send_message(canal_filtro, text)                       
        
#Reacciona cuando un mensaje es editado
@tgclient.on(events.MessageEdited(id_canales_originales))
async def handler(event):
    palabra_prohibida = False
    text = event.text
    print(text)
    raw_text = event.raw_text    
    #obtener el id del mensaje editado
    msg_id = event.message.id
    id_Canal_Original_Evento = event.chat_id
    print("Mensaje editado en canal " + str(id_Canal_Original_Evento))
    for  palabra in palabras_prohibidas:
        raw_text_low = raw_text.lower()
        if palabra in raw_text_low:
            print('si está')
            palabra_prohibida = True
    id_Canal_Copia = conectar_canales(id_Canal_Original_Evento)

    if palabra_prohibida == False:   
        #obtener el id del ultimo mensaje del canal original y restarle el id del mensaje editado
        mensaje_original= await tgclient.get_messages(id_Canal_Original_Evento)
        ultimo_mensaje_original = mensaje_original[-1]
        ultimo_mensaje_original = ultimo_mensaje_original.id
        contador_editado =  int(ultimo_mensaje_original)- int(msg_id)
        #obtener el id del ultimo mensaje del canal de copuia y restarle el resultado de la resta anterior para determinar el id a editar
        mensajes= await tgclient.get_messages(id_Canal_Copia)
        mensaje = mensajes[-1]
        mensaje = mensaje.id
        contador_editado_copia = int(mensaje)- int(contador_editado)
        try:
            text = remove_last_line_from_string(text)
        except:
            pass    
        try:
            text = text.replace("- By @Indoleaks -", "")

        except:
            pass 
        try:
            if "-" in text[-5:]:
                text = text[:-3]
        except:
            pass 
        try:  
            await tgclient.edit_message(id_Canal_Copia, contador_editado_copia, text)  
        except:
            pass    
       

        
#Reacciona cuando una acción es descadenada (foto de perfil, mensajes fijados, etc..)    
@tgclient.on(events.ChatAction(id_canales_originales))
async def my_event_handler(event):
    id_Canal_Original_Evento = event.chat_id
    id_Canal_Copia = conectar_canales(id_Canal_Original_Evento)
    #Si hay una nueva foto de perfil enviar la imagen al canal destino en forma de imagen       
    """if event.new_photo:
        try:
            print("Nueva foto de perfil")
            photos = await tgclient.get_profile_photos(event.chat_id)
            image = await tgclient.download_media(photos[0], file=bytes, thumb=3)
            await tgclient.send_file(id_Canal_Copia, file=image)
        except:
            print("Hubo un error descargando la foto de perfil")"""

    if event.new_pin:
        #obtener el id del mensaje pinneado detectado
        nuevo_pin = event.action_message.reply_to
        id_mensaje_fijado = nuevo_pin.reply_to_msg_id
        iter_msg = await tgclient.get_messages(id_Canal_Original_Evento, limit=50)
        for message in iter_msg:
            if message.id == id_mensaje_fijado:
                texto_citado = message.text
                iter_copia = await tgclient.get_messages(id_Canal_Copia, limit=50)
                for message_ in iter_copia:
                    try:
                        if message_.text == texto_citado:
                            id_msg = message_.id
                            await tgclient.pin_message(id_Canal_Copia, id_msg, notify=True)  
                            print("Nuevo pin fijado")
                    except:
                        pass  
tgclient.start()
tgclient.run_until_disconnected()
