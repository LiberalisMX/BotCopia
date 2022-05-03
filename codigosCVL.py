import os
import base64
import pymongo
import logging
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

mongodb_key = "mongodb+srv://Xicano22:CiudadDelSolG20@cluster0.jt7sg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongodb_key)
db_name = "CVL"
collection_name = "CVLCol"
db = client[db_name][collection_name]
lista_usuarios_permitidos = [1235054916, 1986600767, 1492682588, 5248329076]

def secure_rand(len=6):
    token=os.urandom(len)
    return base64.b64encode(token)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Callback data
CODIGO1, CODIGO2, START, CODIGO3, CODIGO4, CODIGO5, CODIGO6, ALA1, ALA2, ALA3 = range(10)

cod2 = "Ticket 20dls"
cod4 = "Ticket 38dls"
cod6 = "Ticket 55dls"
ala1 = "A la 9dls"
ala2 = "A la 16dls"
ala3 = "A la 22dls"


def start(update: Update, context: CallbackContext) -> None:
    global usuario, chat_id
    chat_id = update.message.chat_id
    user = update.message.from_user
    usuario = user['id']
    print(usuario)
    if usuario in lista_usuarios_permitidos:
        keyboard = [

            [
                InlineKeyboardButton(cod2, callback_data=str(CODIGO2))
            ],
            [
                InlineKeyboardButton(cod4, callback_data=str(CODIGO4))
            ],
            [
                InlineKeyboardButton(cod6, callback_data=str(CODIGO6))
            ],
            [
                InlineKeyboardButton(ala1, callback_data=str(ALA1))
            ],
            [
                InlineKeyboardButton(ala2, callback_data=str(ALA2))
            ],
            [
                InlineKeyboardButton(ala3, callback_data=str(ALA3))
            ],                        
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Elige el canal para el que quieres generar un código:', reply_markup=reply_markup)

    else:
        update.message.reply_text('You are not allowed anon')    
def start2(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    query = update.callback_query
    query.answer()
    if usuario in lista_usuarios_permitidos:
        keyboard = [
            [
                InlineKeyboardButton(cod2, callback_data=str(CODIGO2))
            ],
            [
                InlineKeyboardButton(cod4, callback_data=str(CODIGO4))
            ],
            [
                InlineKeyboardButton(cod6, callback_data=str(CODIGO6))
            ],
            [
                InlineKeyboardButton(ala1, callback_data=str(ALA1))
            ],
            [
                InlineKeyboardButton(ala2, callback_data=str(ALA2))
            ],
            [
                InlineKeyboardButton(ala3, callback_data=str(ALA3))
            ],             
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text('Elige el canal para el que quieres generar un código:', reply_markup=reply_markup)

    else:
        query.edit_message_text('You are not allowed anon')

def codigo2(update: Update, context: CallbackContext) -> None:
    global mensaje
    query = update.callback_query
    query.answer()
    codigo = "2" + str(secure_rand())
    print(codigo)
    ahora = datetime.now()
    try:
        dic_events = db.find_one({"id":1})[cod2]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{cod2:dic_events}})
    except:    
        dic_events = db.find_one({"id":1})["codigos"]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{cod2:dic_events}})
        print("Se insertó una nueva entrada")

    keyboard = [
        [
            InlineKeyboardButton("Volver", callback_data=str(START))
        ]      
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    texto_codigo = "Tu código con valor de $7 es canjeable por 1 mes de suscripción para un Paquete con todos los canales"
    query.edit_message_text(text=f"Se ha registrado el código {codigo} para {cod2} en la base de datos🔑🔄. Debes entregar este mensaje al usuario, solo podrá utilizarlo en una ocasión.\n\nReénviar mensaje al usuario", reply_markup=reply_markup)
    mensaje = context.bot.send_message(chat_id=chat_id, text=f"<b>Bienvenido a ⚜️HispanLeaks⚜️</b>\n\n{texto_codigo}, libre a tu elección.\n\n<b>Haz click en el código para copiarlo:</b>\n<code>{codigo}</code>\n\n<i>Instrucciones:\n\n1. <a href='https://t.me/HispanLeaksBot'>Vuelve al Bot</a> @HispanLeaksBot y reinicia con el comando /start.\n2. Dale al botón '🔑Código de acceso'.\n3. Introduce el código y valídalo.\n5. ¡Listo! Entra a los canales VIP.</i>\n\nCualquier duda te podemos atender por este medio (@HispanLeaks)", parse_mode=ParseMode.HTML)

def codigo4(update: Update, context: CallbackContext) -> None:
    global mensaje
    query = update.callback_query
    query.answer()
    codigo = "4" + str(secure_rand())
    print(codigo)
    ahora = datetime.now()
    try:
        dic_events = db.find_one({"id":1})[cod4]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{cod4:dic_events}})
    except:    
        dic_events = db.find_one({"id":1})["codigos"]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{cod4:dic_events}})
        print("Se insertó una nueva entrada")

    keyboard = [
        [
            InlineKeyboardButton("Volver", callback_data=str(START))
        ]      
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    texto_codigo = "Tu código con valor de $13 es canjeable por 2 meses de suscripción para un Paquete con todos los canales"
    query.edit_message_text(text=f"Se ha registrado el código {codigo} para {cod4} en la base de datos🔑🔄. Debes entregar este mensaje al usuario, solo podrá utilizarlo en una ocasión.\n\nReénviar mensaje al usuario", reply_markup=reply_markup)
    mensaje = context.bot.send_message(chat_id=chat_id, text=f"<b>Bienvenido a ⚜️HispanLeaks⚜️</b>\n\n{texto_codigo}, libre a tu elección.\n\n<b>Haz click en el código para copiarlo:</b>\n<code>{codigo}</code>\n\n<i>Instrucciones:\n\n1. <a href='https://t.me/HispanLeaksBot'>Vuelve al Bot</a> @HispanLeaksBot y reinicia con el comando /start.\n2. Dale al botón '🔑Código de acceso'.\n3. Introduce el código y valídalo.\n5. ¡Listo! Entra a los canales VIP.</i>\n\nCualquier duda te podemos atender por este medio (@HispanLeaks)", parse_mode=ParseMode.HTML)

def codigo6(update: Update, context: CallbackContext) -> None:
    global mensaje
    query = update.callback_query
    query.answer()
    codigo = "6" + str(secure_rand())
    print(codigo)
    ahora = datetime.now()
    try:
        dic_events = db.find_one({"id":1})[cod6]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{cod6:dic_events}})
    except:    
        dic_events = db.find_one({"id":1})["codigos"]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{cod6:dic_events}})
        print("Se insertó una nueva entrada")

    keyboard = [
        [
            InlineKeyboardButton("Volver", callback_data=str(START))
        ]      
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    texto_codigo = "Tu código con valor de $13 es canjeable por 3 meses de suscripción para un Paquete con todos los canales"
    query.edit_message_text(text=f"Se ha registrado el código {codigo} para {cod6} en la base de datos🔑🔄. Debes entregar este mensaje al usuario, solo podrá utilizarlo en una ocasión.\n\nReénviar mensaje al usuario", reply_markup=reply_markup)
    mensaje = context.bot.send_message(chat_id=chat_id, text=f"<b>Bienvenido a ⚜️HispanLeaks⚜️</b>\n\n{texto_codigo}, libre a tu elección.\n\n<b>Haz click en el código para copiarlo:</b>\n<code>{codigo}</code>\n\n<i>Instrucciones:\n\n1. <a href='https://t.me/HispanLeaksBot'>Vuelve al Bot</a> @HispanLeaksBot y reinicia con el comando /start.\n2. Dale al botón '🔑Código de acceso'.\n3. Introduce el código y valídalo.\n5. ¡Listo! Entra a los canales VIP.</i>\n\nCualquier duda te podemos atender por este medio (@HispanLeaks)", parse_mode=ParseMode.HTML)

def a_la_carta1(update: Update, context: CallbackContext) -> None:
    global mensaje
    query = update.callback_query
    query.answer()
    codigo = "7" + str(secure_rand())
    print(codigo)
    ahora = datetime.now()
    try:
        dic_events = db.find_one({"id":1})[ala1]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{ala1:dic_events}})
    except:    
        dic_events = db.find_one({"id":1})["codigos"]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{ala1:dic_events}})
        print("Se insertó una nueva entrada")

    keyboard = [
        [
            InlineKeyboardButton("Volver", callback_data=str(START))
        ]      
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    texto_codigo = "Tu código con valor de $4 es canjeable por 1 mes de suscripción para un canal a la carta"
    query.edit_message_text(text=f"Se ha registrado el código {codigo} para {ala1} en la base de datos🔑🔄. Debes entregar este mensaje al usuario, solo podrá utilizarlo en una ocasión.\n\nReénviar mensaje al usuario", reply_markup=reply_markup)
    mensaje = context.bot.send_message(chat_id=chat_id, text=f"<b>Bienvenido a ⚜️HispanLeaks⚜️</b>\n\n{texto_codigo}, libre a tu elección.\n\n<b>Haz click en el código para copiarlo:</b>\n<code>{codigo}</code>\n\n<i>Instrucciones:\n\n1. <a href='https://t.me/HispanLeaksBot'>Vuelve al Bot</a> @HispanLeaksBot y reinicia con el comando /start.\n2. Dale al botón '🔑Código de acceso'.\n3. Introduce el código y valídalo.\n5. ¡Listo! Entra a los canales VIP.</i>\n\nCualquier duda te podemos atender por este medio (@HispanLeaks)", parse_mode=ParseMode.HTML)

def a_la_carta2(update: Update, context: CallbackContext) -> None:
    global mensaje
    query = update.callback_query
    query.answer()
    codigo = "8" + str(secure_rand())
    print(codigo)
    ahora = datetime.now()
    try:
        dic_events = db.find_one({"id":1})[ala2]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{ala2:dic_events}})
    except:    
        dic_events = db.find_one({"id":1})["codigos"]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{ala2:dic_events}})
        print("Se insertó una nueva entrada")

    keyboard = [
        [
            InlineKeyboardButton("Volver", callback_data=str(START))
        ]      
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    texto_codigo = "Tu código con valor de $7 es canjeable por 2 meses de suscripción para un canal a la carta"
    query.edit_message_text(text=f"Se ha registrado el código {codigo} para {ala2} en la base de datos🔑🔄. Debes entregar este mensaje al usuario, solo podrá utilizarlo en una ocasión.\n\nReénviar mensaje al usuario", reply_markup=reply_markup)
    mensaje = context.bot.send_message(chat_id=chat_id, text=f"<b>Bienvenido a ⚜️HispanLeaks⚜️</b>\n\n{texto_codigo}, libre a tu elección.\n\n<b>Haz click en el código para copiarlo:</b>\n<code>{codigo}</code>\n\n<i>Instrucciones:\n\n1. <a href='https://t.me/HispanLeaksBot'>Vuelve al Bot</a> @HispanLeaksBot y reinicia con el comando /start.\n2. Dale al botón '🔑Código de acceso'.\n3. Introduce el código y valídalo.\n5. ¡Listo! Entra a los canales VIP.</i>\n\nCualquier duda te podemos atender por este medio (@HispanLeaks)", parse_mode=ParseMode.HTML)


def a_la_carta3(update: Update, context: CallbackContext) -> None:
    global mensaje
    query = update.callback_query
    query.answer()
    codigo = "9" + str(secure_rand())
    print(codigo)
    ahora = datetime.now()
    try:
        dic_events = db.find_one({"id":1})[ala3]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{ala3:dic_events}})
    except:    
        dic_events = db.find_one({"id":1})["codigos"]
        dic_events.update({codigo:ahora}) 
        db.update_one({"id":1}, {"$set":{ala3:dic_events}})
        print("Se insertó una nueva entrada")

    keyboard = [
        [
            InlineKeyboardButton("Volver", callback_data=str(START))
        ]      
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)


    texto_codigo = "Tu código con valor de $10 es canjeable por 3 meses de suscripción para un canal a la carta"
    query.edit_message_text(text=f"Se ha registrado el código {codigo} para {ala3} en la base de datos🔑🔄. Debes entregar este mensaje al usuario, solo podrá utilizarlo en una ocasión.\n\nReénviar mensaje al usuario", reply_markup=reply_markup)
    mensaje = context.bot.send_message(chat_id=chat_id, text=f"<b>Bienvenido a ⚜️HispanLeaks⚜️</b>\n\n{texto_codigo}, libre a tu elección.\n\n<b>Haz click en el código para copiarlo:</b>\n<code>{codigo}</code>\n\n<i>Instrucciones:\n\n1. <a href='https://t.me/HispanLeaksBot'>Vuelve al Bot</a> @HispanLeaksBot y reinicia con el comando /start.\n2. Dale al botón '🔑Código de acceso'.\n3. Introduce el código y valídalo.\n5. ¡Listo! Entra a los canales VIP.</i>\n\nCualquier duda te podemos atender por este medio (@HispanLeaks)", parse_mode=ParseMode.HTML)


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5105977351:AAG9zGo4Uh_D-kOyPANlZCZfDzk6t91EItk")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(start2, pattern='^' + str(START) + '$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(codigo2, pattern='^' + str(CODIGO2) + '$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(codigo4, pattern='^' + str(CODIGO4) + '$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(codigo6, pattern='^' + str(CODIGO6) + '$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(a_la_carta1, pattern='^' + str(ALA1) + '$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(a_la_carta2, pattern='^' + str(ALA2) + '$'))
    updater.dispatcher.add_handler(CallbackQueryHandler(a_la_carta3, pattern='^' + str(ALA3) + '$'))    
    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()