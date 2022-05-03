# coding=utf8
from cgitb import html
import logging
import time
import pymongo
from datetime import datetime
from datetime import timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ParseMode
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters)
from typing import Dict
from pyCoinPayments import CryptoPayments
import os
from urllib.request import urlopen
import base64


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
## setup db
dic_user = {}
mongodb_key = "mongodb+srv://Xicano22:CiudadDelSolG20@cluster0.jt7sg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongodb_key)
db_name = "CVL"
collection_name = "CVLCol"
db = client[db_name][collection_name]
duracion, amount, address = "", "", ""
eleccionCantidad_bool = False
eleccionRed_bool, plan_todo = False, False
ids = []
eleccion = []
eleccion_a_la_carta = []
plan_a_la = False
plan_esp = False
plan_ing = False
plan_TODO = False
codigo_ala = False
eleccion_a_la_carta_bool = False
codigo_escrito = False
codigo_usuario = ""
fecha_temprana = 0
nombre_de_canales_ing = ["Always Win VIP\n\nLearn more about this Trader👇\nhttps://t.me/+ETvC93B1rBdlNmVh", "The Bull\n\nLearn more about this Trader👇\nhttps://t.me/+VmRX1TF9dCQ3MzQx", "Kim Crypto\n\nLearn more about this Trader👇\nhttps://t.me/+Jl8st7zvSeBhZjBh", "Inner Circle\n\nLearn more about this Trader👇\nhttps://t.me/+WOXMSKqox6g1YzYx", "KilMex\n\nLearn more about this Trader👇\nhttps://t.me/+JYZut02RqGA5ZmQx", "Haven CBS\n\nLearn more about this Trader👇\nhttps://t.me/+HKyRXEQjKnJiYTE5", "Haven Loma\n\nLearn more about this Trader👇\nhttps://t.me/+HKyRXEQjKnJiYTE5", "Haven Krillin\n\nLearn more about this Trader👇\nhttps://t.me/+HKyRXEQjKnJiYTE5", "Haven Pierre\n\nLearn more about this Trader👇\nhttps://t.me/+HKyRXEQjKnJiYTE5", "Alex Clay Alts\n\nLearn more about this Trader👇\nhttps://t.me/+IIVqmmZOfIdjNTUx", "Alex Clay Margin\n\nLearn more about this Trader👇\nhttps://t.me/+IIVqmmZOfIdjNTUx", "Alex Clay Scalping\n\nLearn more about this Trader👇\nhttps://t.me/+IIVqmmZOfIdjNTUx", "Krypton Wolf\n\nLearn more about this Trader👇\nhttps://t.me/+OQJKeH6iVNM3ZjRh", "Birb Nest\n\nLearn more about this Trader👇\nhttps://t.me/+85zpHRHWMB01ODk5", "Elon Trades\n\nLearn more about this Trader👇\nhttps://t.me/+-oc1qfrnsl85M2Zh", "Raticoin Alts\n\nLearn more about this Trader👇\nhttps://t.me/+x2bds4pk8ZU4NjNh", "Raticoin MArgin\n\nLearn more about this Trader👇\nhttps://t.me/+x2bds4pk8ZU4NjNh", "Bitcoin Bullets\n\nLearn more about this Trader👇\nhttps://t.me/+K3yey0-GRdxlMjIx", "Margin Whales\n\nLearn more about this Trader👇\nhttps://t.me/+L91Og9qMB3w1MTFh", "Rose Premium Signal 2022\n\nLearn more about this Trader👇\nhttps://t.me/+M7gRLkXTgQE2ODM5", "Fat Pig Signals\n\nLearn more about this Trader👇\nhttps://t.me/+dhHbAecrLnQxMzRh", "Binance Killers\n\nLearn more about this Trader👇\nhttps://t.me/+H9IRck2X2vgzNGMx", "FED Russian Insiders\n\nLearn more about this Trader👇\nhttps://t.me/+ZhZCS5ABjZQyYTMx", "APILeakers - Binance Announcements\n\nLearn more about this Trader👇\nhttps://t.me/+UfzkVt2Y99s4ZjAx", "APILeakers - Coin Gecko Listing\n\nLearn more about this Trader👇\nhttps://t.me/+UfzkVt2Y99s4ZjAx" , "APILeakers  -CoinMArketCap Listing\n\nLearn more about this Trader👇\nhttps://t.me/+UfzkVt2Y99s4ZjAx", "Walsh Wealth Discord\n\nLearn more about this Trader👇\nhttps://t.me/+UfzkVt2Y99s4ZjAx", "Credible Crypto\n\nLearn more about this Trader👇\nhttps://t.me/+UfzkVt2Y99s4ZjAx", "Heisenberg Signals\n\nLearn more about this Trader👇\nhttps://t.me/+UfzkVt2Y99s4ZjAx", "Universal Crypto\n\nLearn more about this Trader👇\nhttps://t.me/+UfzkVt2Y99s4ZjAx"]
nombre_de_canales_esp = ["Trading Latino\n\nLearn more about this Trader👇\nhttps://t.me/TradingLatinoInformacion", "Gran Mago VIP\n\nLearn more about this Trader👇\nhttps://t.me/GranMagoInfo", "BitLobo\n\nLearn more about this Trader👇\nhttps://t.me/BitLoboInfo", "InvestClub\n\nLearn more about this Trader👇\nhttps://t.me/InvestClubInfo", "Crypto Nova Premium Indicators\n\nLearn more about this Trader👇\nhttps://t.me/CryptoNovaInfo", "CryptoNova Challenge\n\nLearn more about this Trader👇\nhttps://t.me/CryptoNovaInfo", "CTI BLACK Spot\n\nLearn more about this Trader👇\nhttps://t.me/CTIBlackInfo", "CTI BLACK Futuros\n\nLearn more about this Trader👇\nhttps://t.me/CTIBlackInfo", "Team Camilo VIP\n\nLearn more about this Trader👇\nhttps://t.me/TeamCamiloInfo", "Maverick Trading\n\nLearn more about this Trader👇\nhttps://t.me/MaverickTradingInfo", "Ozzy Master Spot(Miami Trading)\n\nLearn more about this Trader👇\nhttps://t.me/ozzyInfo", "Ozzy Master Futuros(Miami Trading)\n\nLearn more about this Trader👇\nhttps://t.me/ozzyInfo", "APILeakers - Binance Announcements\n\nLearn more about this Trader👇\nhttps://t.me/+UfzkVt2Y99s4ZjAx", "APILeakers - Coin Gecko Listing\n\nLearn more about this Trader👇\nhttps://t.me/+UfzkVt2Y99s4ZjAx" , "APILeakers  -CoinMArketCap Listing\n\nLearn more about this Trader👇\nhttps://t.me/+UfzkVt2Y99s4ZjAx"]
nombre_de_canales_ing_html = ["Always Win VIP</b>\n<i><a href='https://t.me/+ETvC93B1rBdlNmVh'>Learn more about this Trader</a></i>🔎", "The Bull</b>\n<i><a href='https://t.me/+VmRX1TF9dCQ3MzQx'>Learn more about this Trader</a></i>🔎", "Kim Crypto</b>\n<i><a href='https://t.me/+Jl8st7zvSeBhZjBh'>Learn more about this Trader</a></i>🔎", "Inner Circle</b>\n<i><a href='https://t.me/+WOXMSKqox6g1YzYx'>Learn more about this Trader</a></i>🔎", "KilMex</b>\n<i><a href='https://t.me/+JYZut02RqGA5ZmQx'>Learn more about this Trader</a></i>🔎", "Haven CBS\n-Haven Loma\n-Haven Krillin\n-Haven Pierre</b>\n<i><a href='https://t.me/+HKyRXEQjKnJiYTE5'>Learn more about this Trader</a></i>🔎", "Alex Clay Alts\n-Alex Clay Margin\n-Alex Clay Scalping</b>\n<i><a href='https://t.me/+IIVqmmZOfIdjNTUx'>Learn more about this Trader</a></i>🔎", "Krypton Wolf</b>\n<i><a href='https://t.me/+OQJKeH6iVNM3ZjRh'>Learn more about this Trader</a></i>🔎", "Birb Nest</b>\n<i><a href='https://t.me/+85zpHRHWMB01ODk5'>Learn more about this Trader</a></i>🔎", "Elon Trades</b>\n<i><a href='https://t.me/+-oc1qfrnsl85M2Zh'>Learn more about this Trader</a></i>🔎", "Raticoin Alts\n-Raticoin Margin</b>\n<i><a href='https://t.me/+x2bds4pk8ZU4NjNh'>Learn more about this Trader</a></i>🔎", "Bitcoin Bullets</b>\n<i><a href='https://t.me/+K3yey0-GRdxlMjIx'>Learn more about this Trader</a></i>🔎", "Margin Whales</b>\n<i><a href='https://t.me/+L91Og9qMB3w1MTFh'>Learn more about this Trader</a></i>🔎", "Rose Premium Signal 2022</b>\n<i><a href='https://t.me/+M7gRLkXTgQE2ODM5'>Learn more about this Trader</a></i>🔎", "Fat Pig Signals</b>\n<i><a href='https://t.me/+dhHbAecrLnQxMzRh'>Learn more about this Trader</a></i>🔎", "Binance Killers</b>\n<i><a href='https://t.me/+H9IRck2X2vgzNGMx'>Learn more about this Trader</a></i>🔎", "FED Russian Insiders</b>\n<i><a href='https://t.me/+ZhZCS5ABjZQyYTMx'>Learn more about this Trader</a></i>🔎", "APILeakers - Binance Announcements</b>\n<i><a href='https://t.me/+UfzkVt2Y99s4ZjAx'>Learn more about this Trader</a></i>🔎", "APILeakers - CoinGecko Listing</b>\n<i><a href='https://t.me/+UfzkVt2Y99s4ZjAx'>Learn more about this Trader</a></i>🔎", "APILeakers - CoinMarketCap Listing</b>\n<i><a href='https://t.me/+UfzkVt2Y99s4ZjAx'>Learn more about this Trader</a></i>🔎", "Walsh Wealth</b>\n<i><a href='https://t.me/crearcanal'>Learn more about this Trader</a></i>🔎", "Credible Crypto</b>\n<i><a href='https://t.me/crearcanal'>Learn more about this Trader</a></i>🔎", "Heisenberg Signals</b>\n<i><a href='https://t.me/crearcanal'>Learn more about this Trader</a></i>🔎", "Universal Crypto</b>\n<i><a href='https://t.me/crearcanal'>Learn more about this Trader</a></i>🔎"]
nombre_de_canales_esp_html = ["Trading Latino</b>\n<i><a href='https://t.me/TradingLatinoInformacion'>Learn more about this Trader</a></i>🔎", "BitLobo</b>\n<i><a href='https://t.me/BitLoboInfo'>Learn more about this Trader</a></i>🔎", "InvestClub</b>\n<i><a href='https://t.me/InvestClubInfo'>Learn more about this Trader</a></i>🔎", "CryptoNova Premium Indicators\n-CryptoNova Challenge</b>\n<i><a href='https://t.me/CryptoNovaInfo'>Learn more about this Trader</a></i>🔎", "CTI BLACK Spot\n-CTI BLACK Futuros</b>\n<i><a href='https://t.me/CTIBlackInfo'>Learn more about this Trader</a></i>🔎", "TeamCamilo</b>\n<i><a href='https://t.me/TeamCamiloInfo'>Learn more about this Trader</a></i>🔎", "Maverick Trading</b>\n<i><a href='https://t.me/MaverickTradingInfo'>Learn more about this Trader</a></i>🔎", "Ozzy VIP Spot</b>\n<i><a href='https://t.me/ozzyInfo'>Learn more about this Trader</a></i>🔎","Ozzy VIP Spot</b>\n<i><a href='https://t.me/ozzyInfo'>Learn more about this Trader</a></i>🔎"]
nombre_de_canales_esp_texto = ["Trading Latino", "Gran Mago", "BitLobo", "InvestClub", "CryptoNova Premium Indicators", "CryptoNova Challenge", "CTIBLACK Spot", "CTIBLACK Futuros", "TeamCamilo", "Ozzy VIP Spot", "Ozzy VIP Futuros", "API Leakers - Anuncios de Binance", "API Leakers - CoinGecko New Listing", "API Leakers - CoinMarketCap New Listing"]
nombre_de_canales_eng_texto = ["Always Win", "The Bull", "Kim Crypto", "Inner Circle", "KilMex", "Haven CBS", "Haven Loma", "Haven Krillin", "Haven Pierre", "Alex Clay Alts", "Alex Clay Margin", "Alex Clay Scalping", "Krypton Wolf", "Birb Nest", "Elon Trades", "Raticoin Alts", "Raticoin MArgin", "Bitcoin Bullets", "Margin Whales", "Rose Premium Signal 2022", "Fat Pig Signals", "Binance Killers", "FED Russian Insiders", "Maverick", "API Leakers", "API Leakers - Binance Announcements", "API Leakers - CoinGecko New Listing", "API Leakers - CoinMarketCap New Listing"]

API_KEY = "00db512a379e25fc7ed3b3ae6338733fcf156edb81c48af1d51aa56305c95b9f"
API_SECRET = "543318F264b2374bF484d2193fd8237C5c1B6ac201e343957A23CBAF10D4983C"
IPN_SECRET = "http://laguiadigital.mx/coinpayments.php"
# Estados
PRIMERO, SEGUNDO = range(2)
# Callback data
PLAN_ES, ACTIVARPRUEBA, RED, MES2, MES3, COMP, LINK_ESP, TRAN, END, START, PACKS, PLAN_IN, PLAN_TOTAL, COD, COD_COMP, SABER, ALA, ALA_ES, ALA_EN, PLAN_ALA, LINK_ING, LINK_TODO, LINK_ALA, TIPO, PAY = range(25)

#Función que genera una transacción en coinpayments
def crearTransaccion(cantidad, moneda, nombre):
    global amount, address, qrcode, link, transaction
    create_transaction_params = {
        'amount' : cantidad, #cantidad
        'currency1' : 'USD',
        'currency2' : moneda, #moneda
        'buyer_email' : (nombre + '@gmail.com')}
    #Crear client
    client = CryptoPayments(API_KEY, API_SECRET, IPN_SECRET)
    #hacer una llamada a createTransaction de crypto payments API
    transaction = client.createTransaction(create_transaction_params)
    if transaction['error'] == 'ok': 
        amount= transaction['amount'] #cantidad 
        address = transaction['address'] #dirección de billetera
        qrcode = transaction['qrcode_url'] #url del código QR
        link = transaction['checkout_url'] # url del checkout
    else:
        print (transaction['error'])   
#funcion que comprueba el estado de la transacción
def comprobarTransaccion():
    client = CryptoPayments(API_KEY, API_SECRET, IPN_SECRET) 
    try:
        post_params1 = {'txid' : transaction['txn_id']}
    except:
        post_params1 = {'txid' : ""} 
    #llamada a la API de coinpayments para comprobarel estado de la transacción
    transactionInfo = client.getTransactionInfo(post_params1) 
    if transactionInfo['error'] == 'ok':
        print (transactionInfo)
        status = transactionInfo['status']   
    else:
        print (transactionInfo['error'])
        status = 0
    return int(status)    
                   

#función para actualizar los datos de la base de datos MongoDB
def actualizarBD(usuario, name, date):
    dic_events = db.find_one({"id":usuario})["events"]
    dic_events.update({name:date})
    db.update_one({"id":usuario}, {"$set":{"events":dic_events}})

#función para insertar a nuevos usuarios en la base de datos
def instertarBD(usuario, dic_event, name):
    db.insert_one({"id":usuario, "events":{dic_event:name, "Plan":0}})
#funciones que crean alarmas para envíar cuando se está terminado tu plan
def alarm1(context: CallbackContext) -> None:
    global mensaje1, chat_id_, fecha_temprana
    job = context.job
    text = "<b><u>There are 3 days left until your plan ends⏳</u></b>\n\n<i> IF YOU RENEW TODAY WE WILL GIVE YOU 2 DAYS 🎁</i>.\n\n (Your 3 remaining days + 2 days gift + 1 month subscription = <b>35 days/$20</b>)\n ¡ This promotion expires in 24h!\n(applies to any package)"
    mensaje = context.bot.send_message(job.context, text=text, parse_mode=ParseMode.HTML)
    mensaje1 = mensaje.message_id
    chat_id_ = mensaje.chat_id
    fecha_temprana = 5
def alarm2(context: CallbackContext) -> None:
    global mensaje2, fecha_temprana
    job = context.job
    text = "<b><u>There are 2 days left until your plan ends⏳</u></b>"
    mensaje = context.bot.send_message(job.context, text=text, parse_mode=ParseMode.HTML)
    mensaje2 = mensaje.message_id
    context.bot.delete_message(chat_id=mensaje.chat_id, message_id=mensaje1)
    fecha_temprana = 3
def alarm3(context: CallbackContext) -> None:
    global mensaje3, fecha_temprana
    job = context.job
    text = "<b>❗️ Your plan is very close to expiration! ⌛️.\n\n<i> You will be banned from the channels within the next 24 hours </i></b>. You can hire a plan from $20 with the button above 👆"
    mensaje = context.bot.send_message(job.context, text=text, parse_mode=ParseMode.HTML)
    mensaje3 = mensaje.message_id
    context.bot.delete_message(chat_id=mensaje.chat_id, message_id=mensaje2)
    fecha_temprana = 1
def alarm4(context: CallbackContext) -> None:
    global mensaje4
    job = context.job
    text = "<b> Sorry, your plan has expired and you can no longer access the channels </b> 😔\n\n<u> You can hire a plan with the button above </u> 👆"
    mensaje = context.bot.send_message(job.context, text=text, parse_mode=ParseMode.HTML)
    mensaje4 = mensaje.message_id
    context.bot.delete_message(chat_id=mensaje.chat_id, message_id=mensaje3)
    

###código para obtener la prueba gratuita únicamente si tienen Código de acceso
"""def start(update: Update, context: CallbackContext) -> int:
    global name
    global usuario
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    print('You talk with user {} and his user ID: {} '.format(user['username'], user['id']))
    name = str(user['username'])
    usuario = str(user['id'])
    try:
        dic_events = db.find_one({"id":usuario})["events"]
        print("Se encontró al usuario " + name + " en la base de datos")
    except:
        dic_event = "User_id"
        instertarBD(usuario, dic_event, name)
        plan = "Plan"
        plan_tiempo = 0
        instertarBD(usuario, plan, plan_tiempo)
        print("No se encontró al ususario y se ha registrado la nueva entrada")
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("Planes", callback_data=str(VERPLANES)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    user = update.message.from_user
    texto = "Hola " + user.first_name + " bienvenido a Bote Espejo, iniciaste el Bot sin Código de acceso, elige un plan o si cuentas con un código escribelo ahora"
    update.message.reply_text(texto, reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `PRIMERO` now
    return PRIMERO"""

#función inicial cuando el usuario le da a "iniciar"
def start(update: Update, context: CallbackContext) -> int:
    global name, user, nuevo_usuario
    global usuario, chat_id
    chat_id = update.message.chat_id
    # Obtener los datos del usuario
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    print('You talk with user {} and his user ID: {} '.format(user['username'], user['id']))
    name = str(user['username'])
    usuario = str(user['id'])
    # buscar en la base de datos si existe el usuario, si no está insertarlo
    nuevo_usuario = True
    try:
        dic_events = db.find_one({"id":usuario})["events"]
        print("Se encontró al usuario " + name + " en la base de datos")
        nuevo_usuario = False
    except:
        dic_event = "User_id"
        instertarBD(usuario, dic_event, name)
        print("No se encontró al ususario y se ha registrado la nueva entrada")
        nuevo_usuario = True

    keyboard = [
        [InlineKeyboardButton("🎁 10-DAY FREE TRIAL 🎁", callback_data=str(ACTIVARPRUEBA))],
        [InlineKeyboardButton("⚜ Plans and Channels ⚜", callback_data=str(PACKS))],
        [InlineKeyboardButton("Access code 🔑", callback_data=str(COD))],        
        #[InlineKeyboardButton("About this service ❔", callback_data=str(SABER))]        
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Enviar mensaje de text junto con el teclado
    user = update.message.from_user
    context.bot.send_photo(chat_id, "https://i.postimg.cc/Kb9gJMyr/photo-2022-03-06-08-30-05.jpg?dl=1")
    if nuevo_usuario == True:
        texto = "Hello " + user.first_name + "!\n\n🎁 You can activate your 10-day free trial for ALL channels without obligation.🎁\n\n<b>⚠️ LIMITED TIME OFFER ⚠️</b>"
    if nuevo_usuario == False:
        texto = "Hello " + user.first_name + "!\n\n🎁 If your trial is over please choose a Plan.👍"
        
    
    update.message.reply_text(texto, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return PRIMERO 

def start2(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("🎁 10-DAY FREE TRIAL 🎁", callback_data=str(ACTIVARPRUEBA))],
        [InlineKeyboardButton("⚜ Plans and Channels ⚜", callback_data=str(PACKS))],
        [InlineKeyboardButton("Access code 🔑", callback_data=str(COD))],        
        #[InlineKeyboardButton("About this service ❔", callback_data=str(SABER))]        
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Enviar mensaje de text junto con el teclado
    if nuevo_usuario == True:
        texto = "Hello " + user.first_name + "!\n\n🎁 You can activate your 10-day free trial for ALL channels without obligation.🎁\n\n<b>⚠️ LIMITED TIME OFFER ⚠️</b>"
    if nuevo_usuario == False:
        texto = "Hello " + user.first_name + "!\n\n🎁 If your trial is over please choose a Plan.👍"
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_comprobar)  
    except:
        pass         
    query.edit_message_text(texto, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    # Decir a ConversationHandler que ahora estamos en el estado PRIMERO
    return PRIMERO       
def saber_mas (update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton(text="¿Quiénes somos? 👤", url="https://t.me/+J2uMCGcZ8g1iZDNh")],
        [InlineKeyboardButton(text="¿Cómo funciona nuestro servicio? ⚙️", url="https://t.me/+4A0nLiAkxgNkZWQ5")],
        #[InlineKeyboardButton(text="¿Qué nos diferencia de otros servicios? 🔝", url="")],
        [InlineKeyboardButton(text="Sistema de referidos 💵", url="https://t.me/+hsqrr69A3zczYzk5")],
        [InlineKeyboardButton(text="¿Pagas otros canales VIP? ¡Hagámos un trato! 🤝", url="https://t.me/+d7AOZejZdsVjNzcx")],
        [InlineKeyboardButton(text="Back ↩️", callback_data=str(START))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Aquí encontrarás información más detallada de nuestros servicios así cómo las maneras de colaborar con nostros para ganar dinero u obtener el servicio gratis.", reply_markup=reply_markup
    )

    return PRIMERO

#menú cuando aprietas el boton 'Código de acceso'     
def codigo_acceso (update: Update, context: CallbackContext) -> int:
    global id_mensaje_comprobar, codigo_escrito
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton(text="Check validity 🎟", callback_data=str(COD_COMP))],
        [InlineKeyboardButton(text="Back ↩️", callback_data=str(START))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)    

    query.edit_message_text(
        text="<b><u>¿ How to redeem my code?</u>\n\n1️⃣ You must write the code and send it </b>,\n2️⃣ press the 'Check Validity' button 🎟'", reply_markup=reply_markup, parse_mode=ParseMode.HTML
    )
    mensaje_continuar = context.bot.send_message(chat_id =chat_id, text="Submit your code and press 'Check validity 🎟' 👆") 
    id_mensaje_comprobar = mensaje_continuar.message_id
    codigo_escrito = True

    return PRIMERO
def comprobar_codigo (update: Update, context: CallbackContext) -> int:
    global codigo_ala, codigo_usuario
    query = update.callback_query
    query.answer()
    cod2 = "Ticket 20dls"
    cod4 = "Ticket 38dls"
    cod6 = "Ticket 55dls"
    ala1 = "A la 9dls"
    ala2 = "A la 16dls"
    ala3 = "A la 22dls"   

    if codigo_usuario == "":
        keyboard = [
                [InlineKeyboardButton(text="Check validity 🎟", callback_data=str(COD_COMP))],
                [InlineKeyboardButton(text="Back ↩️", callback_data=str(COD))]
                ]
        reply_markup = InlineKeyboardMarkup(keyboard) 
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_comprobar) 
        query.edit_message_text(
            text="¡Oops!, looks like you haven't sent any code❗️\n\n<b> Be sure to <u> FIRST send the message </u> and then press 'Check validity'</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML
        )

        return PRIMERO          
    try:
        dic_events2 = db.find_one({"id":1})[cod2]
        cods2 = dic_events2.keys() 
    except:
        pass    
    try:
        dic_events4 = db.find_one({"id":1})[cod4]
        cods4 = dic_events4.keys() 
    except:
        pass    
    try:
        dic_events6 = db.find_one({"id":1})[cod6]
        cods6 = dic_events6.keys()  
    except:
        pass    
    try:
        dic_events7 = db.find_one({"id":1})[ala1]
        alas1 = dic_events7.keys() 
    except:
        pass
    try:
        dic_events8 = db.find_one({"id":1})[ala2]
        alas2 = dic_events8.keys() 
    except:
        pass
    try:
        dic_events9 = db.find_one({"id":1})[ala3]
        alas3 = dic_events9.keys()  
    except:
        pass
    if codigo_usuario in cods2 or codigo_usuario in alas1:
                
        print("Enviando links de acceso")
        ##Aqui se envían el/los links
        actualizarBD(usuario, "Plan", 1) 

        dias = 30
        avisos =alarma(dias)
        context.job_queue.run_once(alarm1, avisos[0], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm2, avisos[1], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm3, avisos[2], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm4, avisos[3], context=chat_id, name=str(chat_id))    
                        
        estatus = "Estatus"
        estatus_mode = True
        actualizarBD(usuario, estatus, estatus_mode)
        ahora = datetime.now()
        fecha_plan = ahora + timedelta(days=30)# ejemplo -> timedelta(days=10) para 10 días
        actualizarBD(usuario, "Fecha", fecha_plan) 
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_comprobar) 
        except:
            pass
        if codigo_usuario in cods2:
            nom = cod2 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="Show links ➡️", callback_data=str(LINK_TODO))]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)            
            query.edit_message_text(
                text="The Access Code is correct!✅\n\nSubscription valid for 30 days.", reply_markup=reply_markup)
        elif codigo_usuario in alas1:
            nom = ala1 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="On-demand Channels➡️", callback_data=str(ALA_EN))],
                ] 
            codigo_ala = True    
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="The Access Code is correct!✅\n\nSubscription valid for 30 days.", reply_markup=reply_markup)      
       
    if codigo_usuario in cods4 or codigo_usuario in alas2:
                
        print("Enviando links de acceso")
        ##Aqui se envían el/los links
        actualizarBD(usuario, "Plan", 2) 

        dias = 60
        avisos =alarma(dias)
        context.job_queue.run_once(alarm1, avisos[0], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm2, avisos[1], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm3, avisos[2], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm4, avisos[3], context=chat_id, name=str(chat_id))    
                        
        estatus = "Estatus"
        estatus_mode = True
        actualizarBD(usuario, estatus, estatus_mode)
        ahora = datetime.now()
        fecha_plan = ahora + timedelta(days=60)# ejemplo -> timedelta(days=10) para 10 días
        actualizarBD(usuario, "Fecha", fecha_plan) 
        if codigo_usuario in cods4:
            nom = cod4 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="Show links ➡️", callback_data=str(LINK_TODO))]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)            
            query.edit_message_text(
                text="The Access Code is correct!✅\n\nSubscription valid for 60 days.", reply_markup=reply_markup)
        elif codigo_usuario in alas2:
            nom = ala2 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="On-demand Channels➡️", callback_data=str(ALA_EN))],
                ] 
            codigo_ala = True    
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="The Access Code is correct!✅\n\nSubscription valid for 60 days.", reply_markup=reply_markup)        
      
    if codigo_usuario in cods6 or codigo_usuario in alas3:
        
        print("Enviando links de acceso")
        ##Aqui se envían el/los links
        actualizarBD(usuario, "Plan", 2) 

        dias = 90
        avisos =alarma(dias)
        context.job_queue.run_once(alarm1, avisos[0], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm2, avisos[1], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm3, avisos[2], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm4, avisos[3], context=chat_id, name=str(chat_id))    
                        
        estatus = "Estatus"
        estatus_mode = True
        actualizarBD(usuario, estatus, estatus_mode)
        ahora = datetime.now()
        fecha_plan = ahora + timedelta(days=90)# ejemplo -> timedelta(days=10) para 10 días
        actualizarBD(usuario, "Fecha", fecha_plan) 
        if codigo_usuario in cods6:
            nom = cod6 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="Show links ➡️", callback_data=str(LINK_TODO))]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)            
            query.edit_message_text(
                text="The Access Code is correct!✅\n\nSubscription valid for 90 days.", reply_markup=reply_markup)
        elif codigo_usuario in alas3:
            nom = ala3 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="On-demand Channels➡️", callback_data=str(ALA_EN))],
                ] 
            codigo_ala = True    
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="The Access Code is correct!✅\n\nSubscription valid for 90 days.", reply_markup=reply_markup)        
        else:            
            query.edit_message_text(
                text="Sorry, the Access Code is incorrect or has expired.🚫", reply_markup=reply_markup
            )        
    else:
        keyboard = [
                [InlineKeyboardButton(text="Back ↩️", callback_data=str(COD))]
                ]
        reply_markup = InlineKeyboardMarkup(keyboard) 

        query.edit_message_text(
            text="Sorry, the Access Code is incorrect or has expired.🚫", reply_markup=reply_markup
        )
        codigo_usuario = "" 
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje)
    except:
        pass
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_comprobar)
    except:
        pass
    return PRIMERO

def paquetes(update: Update, context: CallbackContext) -> int:
    global eleccion, eleccionRed_bool, plan_todo, texto_canales_esp, texto_canales_ing
    query = update.callback_query
    eleccionRed_bool, plan_todo = False, False

    query.answer()
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=mensaje_id_elecciones)  
    except:
        pass 
    try:
        context.bot.delete_message(chat_id=chat_id_, message_id=mensaje1)
    except:
        pass
    try:
        context.bot.delete_message(chat_id=chat_id_, message_id=mensaje2)
    except:
        pass
    try:
        context.bot.delete_message(chat_id=chat_id_, message_id=mensaje3)
    except:
        pass
    try:
        context.bot.delete_message(chat_id=chat_id_, message_id=mensaje4)
    except:
        pass  
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_continuar) 
    except:
        pass        
    eleccion = []

    
    keyboard = [
        [InlineKeyboardButton(text="All Channels - $20", callback_data=str(PLAN_IN))],
        [InlineKeyboardButton(text="On-demand Channels🧾 - $9", callback_data=str(ALA))],
        [InlineKeyboardButton(text="Back ↩️", callback_data=str(START))]]
    reply_markup = InlineKeyboardMarkup(keyboard) 
    canales_lista_esp = []
    canales_lista_ing = []
    for canal_esp in nombre_de_canales_esp_html:
        canales_esp = "<b>-"+ canal_esp+ "\n\n"
        canales_lista_esp.append(canales_esp)  

    for canal_ing in nombre_de_canales_ing_html:
        canales_ing = "<b>-"+ canal_ing+ "\n\n"
        canales_lista_ing.append(canales_ing)

    texto_canales_esp = "".join(canales_lista_esp)
    texto_canales_ing = "".join(canales_lista_ing)
    
    query.edit_message_text(
        text="<b> You can choose between all the channels or choose the channels on demand:</b>\n\n\n<u><b>Plan with all channels🌐</b></u>\n\nPrice: <b> ONLY $20/month </b>\nChannels in this plan:\n\n" + texto_canales_ing + "\n\n<i>ℹ️ If you are interested in only one channel, You can subscribe for only $9/month in 'On-demand Channels'📋</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    
    return SEGUNDO

#Cuando apriestas canales a la carta
def a_la_carta (update: Update, context: CallbackContext) -> int:
    global eleccion_a_la_carta, eleccion_a_la_carta_bool
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_continuar)  
    except:
        pass    
    query = update.callback_query
    query.answer()
    eleccion_a_la_carta = []
    eleccion_a_la_carta_bool = False
    try:
        context.bot.deleteMessage (message_id = mensaje_unirse_id, chat_id = update.message.chat_id) 
    except:
        pass  
     
    keyboard = [
        [InlineKeyboardButton(text="Show On-demand Channels", callback_data=str(ALA_EN))],
        [InlineKeyboardButton(text="Back ↩️", callback_data=str(PACKS))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="If you are only interested in one or two channels, your best option is the<b> On-demand channels</b>📋", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return SEGUNDO


def a_la_carta_EN(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones, eleccion_a_la_carta_bool
    query = update.callback_query
    query.answer()
    eleccion_a_la_carta_bool = True
    canales_lista_ing = []        
    for canal_ing in nombre_de_canales_ing_html:
        canales_ing = "<b>-"+ canal_ing+ "\n\n"
        canales_lista_ing.append(canales_ing)

    texto_canales_ing = "".join(canales_lista_ing)
    if codigo_ala == False:
        keyboard = [[
                InlineKeyboardButton("Back ↩️", callback_data=str(ALA)),
                InlineKeyboardButton("Continue ➡️", callback_data =str(PLAN_ALA))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="<u><b>On-demand Channels</b></u>\n\nPrice: <b>ONLY $9/month</b>\nChannels:\n\n" + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        reply_keyboard = []
    if codigo_ala == True:

                
        keyboard = [[
                InlineKeyboardButton("Back ↩️", callback_data=str(ALA)),
                InlineKeyboardButton("Continue ➡️", callback_data =str(LINK_ALA))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="<u><b>On-demand Channels</b></u>\n\nPrice: <b>ONLY $9/month</b>\nChannels:\n\n" + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        reply_keyboard = []
            
    for canal in nombre_de_canales_eng_texto:
        lista_canal = []
        lista_canal.append(canal)
        reply_keyboard.append(lista_canal)
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="DO NOT WRITE", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="After choosing the channel, press continue👆", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id 
    return SEGUNDO 

#sección donde se muestran los planes disponibles
def verPlanesIngles(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones, eleccionCantidad_bool, plan_ing
    query = update.callback_query
    query.answer()
    keyboard = [[
            InlineKeyboardButton("Back ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Continue ➡️", callback_data =str(TIPO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="<u><b>Plan with all channels</b></u>\n\nPrice: <b>ONLY $20/month</b>\nChannels in this plan:\n\n" + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    reply_keyboard = [['1 month subscription, $20.00/1 month'], ['2 month subscription, $38.00/2 month'], ['1 month subscription, $55.00/3 month']]
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="DO NOT WRITE", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="After choosing the duration, press continue👆", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id 
    eleccionCantidad_bool = True
    plan_ing = True
    return SEGUNDO

#sección donde se muestran los planes disponibles
def verPlanes_a_la_carta(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones, eleccionCantidad_bool, data_eleccion, plan_a_la
    query = update.callback_query
    query.answer()
    data_eleccion = update.callback_query.data 
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_continuar) 
    except:
        pass     
    print(data_eleccion)
    keyboard = [[
            InlineKeyboardButton("Back ↩️", callback_data=str(ALA)),
            InlineKeyboardButton("Continue ➡️", callback_data =str(TIPO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(
        text="You have chosen channel "+eleccion_a_la_carta[0]+"\n\nAfter choosing the duration of your plan, press continue", reply_markup=reply_markup)
    reply_keyboard = [['1 month subscription, $9.00/1 month'], ['2 month subscription, $16.00/2 month'], ['3 month subscription, $22.00/3 month']]
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="DO NOT WRITE", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="After choosing the duration, press continue👆", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id
    eleccionCantidad_bool = True 
    plan_a_la = True
    return SEGUNDO

def tipoDePago(update: Update, context: CallbackContext) -> int:
    global duracion, mensaje_id_elecciones, eleccionCantidad_bool
    query = update.callback_query
    query.answer()
    eleccionCantidad_bool = False
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_continuar)  
    except:
        pass
    keyboard = [
            [InlineKeyboardButton("CoinPayments", callback_data=str(RED))],
            [InlineKeyboardButton("BinancePay (No commissions)", callback_data =str(PAY))],
            [InlineKeyboardButton("Back ↩️", callback_data=str(PACKS))]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        if "1 month" in eleccion[0]:
            query.edit_message_text(
                text="<b><u> Choose the payment method:</u>\n\nCoinPayments</b>\nPayment by CoinPayments is automatically managed by the platform.\n\commissions: $1 aprox.\n\n<b>Binance Pay</b>\nPayments by Binance Pay are WITHOUT COMMISSIONS.\n⚠️<i>The verification of the payment is done MANUALLY, so it can take from a few minutes to a few hours (*depending on the time availability of the admin).</i>"
, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        else:
            query.edit_message_text(
                text="<b><u> Choose the payment method:</u>\n\nCoinPayments</b>\nPayment by CoinPayments is automatically managed by the platform.\n\commissions: $1 aprox.\n\n<b>Binance Pay</b>\nPayments by Binance Pay are WITHOUT COMMISSIONS.\n⚠️<i>The verification of the payment is done MANUALLY, so it can take from a few minutes to a few hours (*depending on the time availability of the admin).</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except:
        pass
    return PRIMERO
    
def tipoDeRed(update: Update, context: CallbackContext) -> int:
    global duracion, mensaje_id_elecciones, eleccionCantidad_bool, eleccionRed_bool
    query = update.callback_query
    query.answer()
    eleccionRed_bool = True
    keyboard = [[
            InlineKeyboardButton("Back ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Continue ➡️", callback_data =str(TRAN))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Payments are made through the Coinpayments platform in the currency USDT (Tether USD, ¡NO BUSD!) in any of the available Blockchain networks.", reply_markup=reply_markup)
    reply_keyboard = [['⚡️ USDT.BEP20 - Theter USD (BEP20 / BSC)'], ['⚡️ USDT.TRC20 - Theter USD (TRC20 / Tron Chain)']]
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="DO NOT WRITE", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="Choose the network you prefer, press continue and wait for your order to be generated.", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id
    return PRIMERO
  
def BinancePay(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones, mensaje_id_elecciones2
    query = update.callback_query
    query.answer()
    try:
        if "1 month subscription" in eleccion[0]:
            if plan_todo == True: 
                mensaje = context.bot.send_photo(chat_id, photo="https://i.imgur.com/VukS1tk.jpg", caption="<b><u>1 month plan cost: $20\n\nInstructions:</u></b>\n\n1.- Download the image to your gallery to be able to access it from the Binance app.\n\n2.-Scan the image with the Binance app and send the funds.\n\n3.-Take a screenshot and send it via chat to @HispanLeaksAdmin\n\n4.-Wait for the administrator to verify your payment and they will give you a code.\n\n5.-Restart this bot with the /start command and enter the access code given to you by the administrator on the button\n'🔑Access code'.\n\n<i> If you have doubts about how to make the payment by Binance Pay we have made a detailed guide. <a href='https://t.me/+H80QNFwyiCFjNTMx'></a></i>", parse_mode=ParseMode.HTML)
            elif plan_a_la == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/etOMw12.jpg", caption="<b><u>1 month channel cost: $9\n\nInstructions:</u></b>\n\n1.- Download the image to your gallery to be able to access it from the Binance app.\n\n2.-Scan the image with the Binance app and send the funds.\n\n3.-Take a screenshot and send it via chat to @HispanLeaksAdmin\n\n4.-Wait for the administrator to verify your payment and they will give you a code.\n\n5.-Restart this bot with the /start command and enter the access code given to you by the administrator on the button\n'🔑Access code'.\n\n<i> If you have doubts about how to make the payment by Binance Pay we have made a detailed guide. <a href='https://t.me/+H80QNFwyiCFjNTMx'></a></i>", parse_mode=ParseMode.HTML)
            else:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/VukS1tk.jpg", caption="<b><u>1 month plan cost: $20\n\nInstructions:</u></b>\n\n1.- Download the image to your gallery to be able to access it from the Binance app.\n\n2.-Scan the image with the Binance app and send the funds.\n\n3.-Take a screenshot and send it via chat to @HispanLeaksAdmin\n\n4.-Wait for the administrator to verify your payment and they will give you a code.\n\n5.-Restart this bot with the /start command and enter the access code given to you by the administrator on the button\n'🔑Access code'.\n\n<i> If you have doubts about how to make the payment by Binance Pay we have made a detailed guide. <a href='https://t.me/+H80QNFwyiCFjNTMx'></a></i>", parse_mode=ParseMode.HTML)
        
        if "2 month subscription" in eleccion[0]:
            if plan_todo == True: 
                mensaje = context.bot.send_photo(chat_id, photo="https://i.imgur.com/fTUtdsO.jpg", caption="<b><u>2 month plan cost: $38\n\nInstructions:</u></b>\n\n1.- Download the image to your gallery to be able to access it from the Binance app.\n\n2.-Scan the image with the Binance app and send the funds.\n\n3.-Take a screenshot and send it via chat to @HispanLeaksAdmin\n\n4.-Wait for the administrator to verify your payment and they will give you a code.\n\n5.-Restart this bot with the /start command and enter the access code given to you by the administrator on the button\n'🔑Access code'.\n\n<i> If you have doubts about how to make the payment by Binance Pay we have made a detailed guide. <a href='https://t.me/+H80QNFwyiCFjNTMx'></a></i>", parse_mode=ParseMode.HTML)
            elif plan_a_la == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/bIHXmkt.jpg", caption="<b><u>2 month channel cost: $16\n\nInstructions:</u></b>\n\n1.- Download the image to your gallery to be able to access it from the Binance app.\n\n2.-Scan the image with the Binance app and send the funds.\n\n3.-Take a screenshot and send it via chat to @HispanLeaksAdmin\n\n4.-Wait for the administrator to verify your payment and they will give you a code.\n\n5.-Restart this bot with the /start command and enter the access code given to you by the administrator on the button\n'🔑Access code'.\n\n<i> If you have doubts about how to make the payment by Binance Pay we have made a detailed guide. <a href='https://t.me/+H80QNFwyiCFjNTMx'></a></i>", parse_mode=ParseMode.HTML)
            else:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/fTUtdsO.jpg", caption="<b><u>2 month plan cost: $38\n\nInstructions:</u></b>\n\n1.- Download the image to your gallery to be able to access it from the Binance app.\n\n2.-Scan the image with the Binance app and send the funds.\n\n3.-Take a screenshot and send it via chat to @HispanLeaksAdmin\n\n4.-Wait for the administrator to verify your payment and they will give you a code.\n\n5.-Restart this bot with the /start command and enter the access code given to you by the administrator on the button\n'🔑Access code'.\n\n<i> If you have doubts about how to make the payment by Binance Pay we have made a detailed guide. <a href='https://t.me/+H80QNFwyiCFjNTMx'></a></i>", parse_mode=ParseMode.HTML)      

        if "3 month subscription" in eleccion[0]:
            if plan_todo == True: 
                mensaje = context.bot.send_photo(chat_id, photo="https://i.imgur.com/fuWGNJ8.jpg", caption="<b><u>3 month plan cost: $55\nInstructions:</u></b>\n\n1.- Download the image to your gallery to be able to access it from the Binance app.\n\n2.-Scan the image with the Binance app and send the funds.\n\n3.-Take a screenshot and send it via chat to @HispanLeaksAdmin\n\n4.-Wait for the administrator to verify your payment and they will give you a code.\n\n5.-Restart this bot with the /start command and enter the access code given to you by the administrator on the button\n'🔑Access code'.\n\n<i> If you have doubts about how to make the payment by Binance Pay we have made a detailed guide. <a href='https://t.me/+H80QNFwyiCFjNTMx'></a></i>", parse_mode=ParseMode.HTML)
            elif plan_a_la == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/1QvRkhZ.jpeg", caption="<b><u>3 month channel cost: $22\nInstructions:</u></b>\n\n1.- Download the image to your gallery to be able to access it from the Binance app.\n\n2.-Scan the image with the Binance app and send the funds.\n\n3.-Take a screenshot and send it via chat to @HispanLeaksAdmin\n\n4.-Wait for the administrator to verify your payment and they will give you a code.\n\n5.-Restart this bot with the /start command and enter the access code given to you by the administrator on the button\n'🔑Access code'.\n\n<i> If you have doubts about how to make the payment by Binance Pay we have made a detailed guide. <a href='https://t.me/+H80QNFwyiCFjNTMx'></a></i>", parse_mode=ParseMode.HTML)
            else:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/fuWGNJ8.jpg", caption="<b><u>3 month plan cost: $55\nInstructions:</u></b>\n\n1.- Download the image to your gallery to be able to access it from the Binance app.\n\n2.-Scan the image with the Binance app and send the funds.\n\n3.-Take a screenshot and send it via chat to @HispanLeaksAdmin\n\n4.-Wait for the administrator to verify your payment and they will give you a code.\n\n5.-Restart this bot with the /start command and enter the access code given to you by the administrator on the button\n'🔑Access code'.\n\n<i> If you have doubts about how to make the payment by Binance Pay we have made a detailed guide. <a href='https://t.me/+H80QNFwyiCFjNTMx'></a></i>", parse_mode=ParseMode.HTML)
    except:
        context.bot.send_message(chat_id, text="There was an error choosing the value of the package, please restart the bot choosing the price of the package you want.\n\nIf you continue to experience problems please contact the admin @CryptoVIPLeaks and we will solve it as soon as possible.")

    mensaje_id_elecciones = mensaje.message_id
    return ConversationHandler.END

def transaccion(update: Update, context: CallbackContext) -> int:
    global plan, eleccionRed_bool
    query = update.callback_query
    query.answer()
    eleccionRed_bool = False
    context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_continuar)  
    nombre = usuario
    if "1 month subscription" in eleccion[0]:
        if plan_todo == True:
            plan = 1
            cantidad = 20
        elif plan_a_la == True:
            plan = 1
            cantidad = 9
        else:
            plan = 1
            cantidad = 20
    
    if "2 month subscription" in eleccion[0]:
        if plan_todo == True:
            plan = 2
            cantidad = 38
        elif plan_a_la == True:
            plan = 2
            cantidad = 16             
        else:
            plan = 2
            cantidad = 38
        

    if "3 month subscription" in eleccion[0]:
        if plan_todo == True:
            plan = 3
            cantidad = 55
        elif plan_a_la == True:
            plan = 3
            cantidad = 22             
        else:
            plan = 3
            cantidad = 55
        
    if "USDT.BEP20" in eleccion[1]:
        moneda = "USDT.BEP20"  
    if "USDT.TRC20" in eleccion[1]:
        moneda = "USDT.TRC20"          

    actualizarBD(usuario, "Plan", plan) 

    #generar un pago
    crearTransaccion(cantidad, moneda, nombre)

    keyboard = [
        [
            InlineKeyboardButton("Back ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Check your subscription 🔄", callback_data=str(COMP))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(text='To ensure that the transaction does not fail, we recommend that you send at least $0.05c extra. \n<a href="'+qrcode+'">&#8205;</a>', reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    query.edit_message_text(
        text="Payment by CoinPayments\n\n<b> wallet address:</b>\n<code>" + address + "</code>\n\n<b> Amount of USDT to send:</b>\n$" + str(amount) + " (" + moneda + ")\n\n⚠️The Coinpayments platform will only consider the transaction approved when the TOTAL amount of the payment is covered.\n❗️ Payment link expires in 1 day\n\n If you have any problem with the payment, contact to @Admin, we will assist you as soon as possible.\n\n<a href='"+link+"'>Check the status of the transaction on Coinpayments.net </a>" , parse_mode="HTML")
 
    return SEGUNDO       

def alarma(num):    
    dias = num + fecha_temprana
    aviso3_dias = dias-1
    aviso2_dias = dias-2
    aviso1_dias = dias-3
    aviso1_fecha = timedelta(days=aviso1_dias)
    aviso2_fecha = timedelta(days=aviso2_dias)
    aviso3_fecha = timedelta(days=aviso3_dias)
    aviso4_fecha = timedelta(days=dias)
    return aviso1_fecha, aviso2_fecha, aviso3_fecha, aviso4_fecha
    
#comprobar el estado de la transacción   
def comp(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    nombre = "Plan"
    name = "Status"
    status = comprobarTransaccion()
    #status = 1  #<- Modo prueba de "comprobarTransaccion()" -Pasa 1 para representar una transacción de pago confirmada
    try:
        print(status)
    except:
        status = 0
    try:    
        plan = db.find_one({"id":usuario})["events"]["Plan"]
    except:
        pass    
    if status == 0:
        keyboard = [[
            InlineKeyboardButton("Back ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Check your subscription 🔄", callback_data=str(COMP))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            query.edit_message_text(
                text="<b>Payment has not been received. The approximate time of the transaction is 30 min.</b>\n\nIf you have any problem with the transaction, contact to @CryptoVIPLeaks, we will assist you as soon as possible.\n\n<a href='"+link+"'>See the status of the transaction in Coinpayments </a>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except:
            query.edit_message_text(
                text="Payment has not been received. The approximate time of the transaction is 30 min.</b>\n\nIf you have any problem with the transaction, contact to @CryptoVIPLeaks, we will assist you as soon as possible.", reply_markup=reply_markup)  

    if status == 1:
        keyboard = [[
            InlineKeyboardButton("Back ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Check your subscription 🔄", callback_data=str(COMP))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            query.edit_message_text(
                text="<b>The transaction has been detected, waiting for 10 confirmations. Try again after a few minutes.</b>\n\nIf you have any problems with the transaction, contact to @CryptoVIPLeaks, we will assist you as soon as possible.\n\n<a href='"+link+"'> See the status of the transaction in Coinpayments</a>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except:
            query.edit_message_text(
                text="No payment received.\n\nIf you have any problems with the transaction, contact to @Admin, we will assist you as soon as possible.", reply_markup=reply_markup)  
 

    if status == 100:
        remove(str(chat_id), context)   
        if plan == 1: 
            actualizarBD(usuario, nombre, plan) 
            dias = 30
            avisos =alarma(dias)
            context.job_queue.run_once(alarm1, avisos[0], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm2, avisos[1], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm3, avisos[2], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm4, avisos[3], context=chat_id, name=str(chat_id))    
                    

            if plan_ing == True:
                keyboard = [[
                    InlineKeyboardButton("Show links 🔗", callback_data=str(LINK_ING))]]

            if eleccion_a_la_carta_bool == True:
                keyboard = [[
                    InlineKeyboardButton("Show links 🔗", callback_data=str(LINK_ALA))]]                        

            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="<b>¡Payment received!✅.\n<i>Your membership is active for 1 month 🎉</i></b>\n\nPress the button<i>'Ver links🔗'</i> just once and wait for the links to load.\n\n⚠️<i>If you join VIP channels too quickly Telegram will temporarily block the feature, in that case just wait a few minutes and try again</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            ahora = datetime.now()
            
            fecha_plan = ahora + timedelta(days=dias)
            dic_event = "Fecha"
            actualizarBD(usuario, dic_event, fecha_plan)
            estatus = "Estatus"
            estatus_mode = True
            actualizarBD(usuario, estatus, estatus_mode)
            os.system('python3 pyroCVL.py')


        if plan == 2:
            actualizarBD(usuario, nombre, plan) 
            dias = 60
            avisos =alarma(dias)
            context.job_queue.run_once(alarm1, avisos[0], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm2, avisos[1], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm3, avisos[2], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm4, avisos[3], context=chat_id, name=str(chat_id))    
                    

            if plan_ing == True:
                keyboard = [[
                    InlineKeyboardButton("Show links 🔗", callback_data=str(LINK_ING))]]
   
            if eleccion_a_la_carta_bool == True:
                keyboard = [[
                    InlineKeyboardButton("Show links 🔗", callback_data=str(LINK_ALA))]]   

            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="<b>¡Payment received!✅.\n<i>Your membership is active for 1 month 🎉</i></b>\n\nPress the button<i>'Ver links🔗'</i> just once and wait for the links to load.\n\n⚠️<i>If you join VIP channels too quickly Telegram will temporarily block the feature, in that case just wait a few minutes and try again</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            ahora = datetime.now()
            fecha_plan = ahora + timedelta(days=60)
            dic_event = "Fecha"
            actualizarBD(usuario, dic_event, fecha_plan) 
            estatus = "Estatus"
            estatus_mode = True
            actualizarBD(usuario, estatus, estatus_mode)
            os.system('python3 pyroCVL.py')  

        if plan == 3:
            actualizarBD(usuario, nombre, plan) 
            dias = 90
            avisos =alarma(dias)
            context.job_queue.run_once(alarm1, avisos[0], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm2, avisos[1], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm3, avisos[2], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm4, avisos[3], context=chat_id, name=str(chat_id))    
                    
            if plan_ing == True:
                keyboard = [[
                    InlineKeyboardButton("Show links 🔗", callback_data=str(LINK_ING))]]

            if eleccion_a_la_carta_bool == True:
                keyboard = [[
                    InlineKeyboardButton("Show links 🔗", callback_data=str(LINK_ALA))]]               
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="<b>¡Payment received!✅.\n<i>Your membership is active for 1 month 🎉</i></b>\n\nPress the button<i>'Ver links🔗'</i> just once and wait for the links to load.\n\n⚠️<i>If you join VIP channels too quickly Telegram will temporarily block the feature, in that case just wait a few minutes and try again</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            ahora = datetime.now()
            fecha_plan = ahora + timedelta(days=dias)
            dic_event = "Fecha"
            actualizarBD(usuario, dic_event, fecha_plan) 
            estatus = "Estatus"
            estatus_mode = True
            actualizarBD(usuario, estatus, estatus_mode)
    os.system('python3 pyroCVL.py')           

    return PRIMERO
#función para activar la prueba gratuita
def activarPrueba(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    #Buscar en la BD si el usuario ya utilizó la prueba y si es que si mira la fecha para comprobar su vencimiento
    try:
        date_ahora = datetime.now()
        fecha = db.find_one({"id":usuario})["events"]["Fecha"]
        print("Se encontró la fecha en la base de datos, comprobando dia de vencimiento")
        if fecha  < date_ahora: 
            keyboard = [[InlineKeyboardButton("⚜ See our plans ⚜", callback_data=str(PACKS))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text="Your free trial has ended⌛️\n\nHire a plan to continue on the channels", reply_markup=reply_markup)
        else:
            keyboard = [[InlineKeyboardButton("Back ↩️", callback_data=str(PACKS))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="Your trial is not yet due⏳", reply_markup=reply_markup)
    except:
        date_ahora = datetime.now()
        #Establecer cantidad de tiempo de prueba
        dias = 10
        avisos =alarma(dias)
        context.job_queue.run_once(alarm1, avisos[0], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm2, avisos[1], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm3, avisos[2], context=chat_id, name=str(chat_id)) 
        context.job_queue.run_once(alarm4, avisos[3], context=chat_id, name=str(chat_id))    
                
        print("No se encontró fecha en la base de datos, activando prueba gratuita ")
        fecha_de_vencimiento = timedelta(days=dias)
        fecha = date_ahora + fecha_de_vencimiento        
        dic_event = "Fecha"
        actualizarBD(usuario, dic_event, fecha)
        estatus = "Estatus"
        estatus_mode = True
        actualizarBD(usuario, estatus, estatus_mode)
        keyboard = [[
            InlineKeyboardButton("Show links 🔗", callback_data=str(LINK_ING))]]     
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="🎉 <b>¡Congratulations! your trial of <u>10 days with access to all channels</u>has been activated!</b> 🎁\n\nPress the button once and wait for the links to load👇<i>\n(Patience, it may take a few seconds⏳)\n\n⚠️If you join VIP channels too quickly Telegram will temporarily block the feature, in that case just wait a few minutes and try again</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        os.system('pyro.py')

    return SEGUNDO

def email(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton(text="1 month subscription, $10.00/1 month", callback_data=str(RED))],
        [InlineKeyboardButton(text="3 month subscription, $30.00/3 month", callback_data=str(MES2))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Introduce tu email si quieres que se incluya en la transacción:", reply_markup=reply_markup)
    return SEGUNDO 

def help(update: Update, context: CallbackContext) -> int:
    
    context.bot.send_message(chat_id, text="To restart the bot just type or click on-> /start <-\n\nIf the error is not solved by rebooting, please contact the administrator to @CryptoVIPLeaks")
    return ConversationHandler.END


def links_ing(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    dic_events = db.find_one({"id":0})["events"]
    enlaces = dic_events["link_grupos_ing"]
    canal = 0          
    for grup in enlaces:
        keyboard = [
            [InlineKeyboardButton(text="⚜ Join to VIP Channel ⚜", url=grup),
            InlineKeyboardButton(text="Learn more about this Trader 🔎", url=grup)],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text=nombre_de_canales_ing[canal], reply_markup=reply_markup) 
        canal +=1    
    keyboard = [
        [InlineKeyboardButton("⚜ See our plans", callback_data=str(PACKS))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.message.reply_text(text="⏰We will inform you when your membership is about to expire.⚠️ <b>The links are valid for a single use and will be active for 3 days</b>\n\n<u><i>ℹ️ If you have any problem, doubt, suggestion, want to collaborate in the referral system or if you pay for one or several Premium channels and want to be a member, contact us through the only official contact @CryptoVIPLeaks, we will answer you as soon as possible🙂ℹ️</i></u>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return SEGUNDO
def links_a_la_carta(update: Update, context: CallbackContext) -> int:
    global eleccion_a_la_carta_bool, codigo_ala, eleccion_a_la_carta, mensaje_unirse_id
    query = update.callback_query
    query.answer()
    num_canal_esp = 0
    eng_or_esp = ""
    print(eleccion_a_la_carta[0])
    enlace = "Hubo un error, contacte al administrador"
    for canal in nombre_de_canales_esp_texto:
        if canal == eleccion_a_la_carta[0]:
            eng_or_esp = "ESP"
            break
        num_canal_esp +=1    
    num_canal_eng = 0
    for canal in nombre_de_canales_eng_texto:
        if canal == eleccion_a_la_carta[0]:
            eng_or_esp = "ENG"
            break
        num_canal_eng +=1

    if eng_or_esp == "ESP":
        dic_events = db.find_one({"id":0})["events"]
        enlaces_esp = dic_events["link_grupos_esp"]
        enlace = enlaces_esp[num_canal_esp] 
        print(enlace)
    elif eng_or_esp == "ENG":
        dic_events = db.find_one({"id":0})["events"]
        enlaces_eng = dic_events["link_grupos_ing"]
        enlace = enlaces_eng[num_canal_eng]
        print(enlace)         
    else:
        print("No se activo eng_or_esp")
             
    keyboard = [
        [InlineKeyboardButton(text="⚜ Únete al canal VIP ⚜", url=enlace)
        ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=mensaje_id_elecciones) 
    except:
        pass 
    mensaje_unirse = query.message.reply_text(text="Puedes unirte a "+ eleccion_a_la_carta[0] +" en el boton de abajo👇. Para volver a activar el bot usa el comando /start", reply_markup=reply_markup)
    mensaje_unirse_id = mensaje_unirse.message_id
       
    eleccion_a_la_carta_bool = False 
    codigo_ala = False
    eleccion_a_la_carta = []
    return SEGUNDO


#funcion para quitar los avisos programados
def remove(name: str, context: CallbackContext) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    for job in current_jobs:
        job.schedule_removal()
    return True    
#escuchar todo lo que teclea el usuario
def main_handler(update: Update, context: CallbackContext) -> None:
    global input_usuario, id_mensaje, id_mensaje_continuar, codigo_usuario
    input_usuario= update.message.text
    id_mensaje = update.message.message_id
    
    
    if eleccionCantidad_bool == True:
        ids.append(id_mensaje) 
        eleccion.append(input_usuario)

    if eleccionRed_bool == True:
        ids.append(id_mensaje) 
        eleccion.append(input_usuario) 
    if '1 month subscription' in input_usuario or '2 month subscription' in input_usuario or '3 month subscription' in input_usuario or input_usuario == '⚡️ USDT.BEP20 - Theter USD (BEP20 / BSC)' or input_usuario == '⚡️ USDT.TRC20 - Theter USD (TRC20 / Tron Chain)':  
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje) 
        context.bot.delete_message(chat_id=chat_id, message_id=mensaje_id_elecciones) 
        mensaje_continuar = context.bot.send_message(chat_id =chat_id, text="Press continue 👆") 
        id_mensaje_continuar = mensaje_continuar.message_id
      
    if eleccion_a_la_carta_bool == True:
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje) 
            context.bot.delete_message(chat_id=chat_id, message_id=mensaje_id_elecciones)         
        except:
            pass  
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_continuar)  
        except:
            pass     
        ids.append(id_mensaje)
        eleccion_a_la_carta.append(input_usuario) 
        print("Se registro en la variable la eleccion " + input_usuario)
        mensaje_continuar = context.bot.send_message(chat_id =chat_id, text="Press continue 👆") 
        id_mensaje_continuar = mensaje_continuar.message_id
    if codigo_escrito == True:
        codigo_usuario = input_usuario

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5342854757:AAGhL0uidihNAOHUadSPFKsfW587EgOdlxA")
    j = updater.job_queue
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states PRIMERO and SEGUNDO
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "help of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        allow_reentry = True,
        states={
            PRIMERO: [
                CommandHandler('help', help),
                CallbackQueryHandler(paquetes, pattern='^' + str(PACKS) + '$'),
                CallbackQueryHandler(activarPrueba, pattern='^' + str(ACTIVARPRUEBA) + '$'),
                CallbackQueryHandler(comp, pattern='^' + str(COMP) + '$'),
                CallbackQueryHandler(transaccion, pattern='^' + str(TRAN) + '$'), 
                MessageHandler(Filters.text, main_handler),
                CallbackQueryHandler(start2, pattern='^' + str(START) + '$'),
                CallbackQueryHandler(saber_mas, pattern='^' + str(SABER) + '$'),
                CallbackQueryHandler(tipoDePago, pattern = '^' + str(TIPO) + '$'),
                CallbackQueryHandler(BinancePay, pattern = '^' + str(PAY) + '$'),
                CallbackQueryHandler(tipoDeRed, pattern='^' + str(RED) + '$'),
                CallbackQueryHandler(codigo_acceso, pattern='^' + str(COD) + '$'),
                CallbackQueryHandler(comprobar_codigo, pattern='^' + str(COD_COMP) + '$'),
                CallbackQueryHandler(a_la_carta_EN, pattern='^' + str(ALA_EN) + '$'),                
            ],
            SEGUNDO: [
                CommandHandler('help', help),
                CallbackQueryHandler(paquetes, pattern='^' + str(PACKS) + '$'),
                CallbackQueryHandler(tipoDeRed, pattern='^' + str(RED) + '$'),
                CallbackQueryHandler(tipoDePago, pattern = '^' + str(TIPO) + '$'),
                CallbackQueryHandler(comp, pattern='^' + str(COMP) + '$'),
                CallbackQueryHandler(links_ing, pattern='^' + str(LINK_ING) + '$'),                 
                CallbackQueryHandler(transaccion, pattern='^' + str(TRAN) + '$'),
                MessageHandler(Filters.text, main_handler),
                CallbackQueryHandler(start2, pattern='^' + str(START) + '$'), 
                CallbackQueryHandler(verPlanesIngles, pattern='^' + str(PLAN_IN) + '$'),    
                CallbackQueryHandler(a_la_carta, pattern='^' + str(ALA) + '$'), 
                CallbackQueryHandler(a_la_carta_EN, pattern='^' + str(ALA_EN) + '$'),
                CallbackQueryHandler(verPlanes_a_la_carta, pattern='^' + str(PLAN_ALA) + '$'), 
                CallbackQueryHandler(links_a_la_carta, pattern='^' + str(LINK_ALA) + '$'),           
            ],
        },
        fallbacks=[CommandHandler('start', start)],  
    )
    dispatcher.add_handler(conv_handler)
    
    # Arrancar el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()