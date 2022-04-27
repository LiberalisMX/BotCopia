#!/usr/bin/env python
# pylint: disable=C0116,W0613

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
db_name = "Bote"
collection_name = "BoteCol"
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
nombre_de_canales_ing = ["Always Win VIP\n\nConoce a este Trader👇\nhttps://t.me/AlwaysWinInfo", "The Bull\n\nConoce a este Trader👇\nhttps://t.me/TheBullInfo", "Kim Crypto\n\nConoce a este Trader👇\nhttps://t.me/KimCryptoInfo", "Inner Circle\n\nConoce a este Trader👇\nhttps://t.me/InnerCircleInfo", "KilMex\n\nConoce a este Trader👇\nhttps://t.me/KillMexInfo", "Haven CBS\n\nConoce a este Trader👇\nhttps://t.me/TheHavenInfo", "Haven Loma\n\nConoce a este Trader👇\nhttps://t.me/TheHavenInfo", "Haven Krillin\n\nConoce a este Trader👇\nhttps://t.me/TheHavenInfo", "Haven Pierre\n\nConoce a este Trader👇\nhttps://t.me/TheHavenInfo", "Alex Clay Alts\n\nConoce a este Trader👇\nhttps://t.me/AlexClayInfo", "Alex Clay Margin\n\nConoce a este Trader👇\nhttps://t.me/AlexClayInfo", "Alex Clay Scalping\n\nConoce a este Trader👇\nhttps://t.me/AlexClayInfo", "Krypton Wolf\n\nConoce a este Trader👇\nhttps://t.me/KryptonWolfInfo", "Birb Nest\n\nConoce a este Trader👇\nhttps://t.me/BirbNestInfo", "Elon Trades\n\nConoce a este Trader👇\nhttps://t.me/ElonTradesInfo_esp", "Raticoin Alts\n\nConoce a este Trader👇\nhttps://t.me/raticoinInfo_esp", "Raticoin MArgin\n\nConoce a este Trader👇\nhttps://t.me/raticoinInfo_esp", "Bitcoin Bullets\n\nConoce a este Trader👇\nhttps://t.me/BitcoinBulletsInfo", "Margin Whales\n\nConoce a este Trader👇\nhttps://t.me/MarginWhalesInfo", "Rose Premium Signal 2022\n\nConoce a este Trader👇\nhttps://t.me/RosePremiumSignalsInfo", "Fat Pig Signals\n\nConoce a este Trader👇\nhttps://t.me/FatPigSignalsInfo", "Binance Killers\n\nConoce a este Trader👇\nhttps://t.me/BinanceKillersInfo", "FED Russian Insiders\n\nConoce a este Trader👇\nhttps://t.me/FedRussianInsidersInfo", "APILeakers - Binance Announcements\n\nConoce a este Trader👇\nhttps://t.me/APILeakersInfo", "APILeakers - Coin Gecko Listing\n\nConoce a este Trader👇\nhttps://t.me/APILeakersInfo" , "APILeakers  -CoinMArketCap Listing\n\nConoce a este Trader👇\nhttps://t.me/APILeakersInfo"]
nombre_de_canales_esp = ["Trading Latino\n\nConoce a este Trader👇\nhttps://t.me/TradingLatinoInformacion", "Gran Mago VIP\n\nConoce a este Trader👇\nhttps://t.me/GranMagoInfo", "BitLobo\n\nConoce a este Trader👇\nhttps://t.me/BitLoboInfo", "InvestClub\n\nConoce a este Trader👇\nhttps://t.me/InvestClubInfo", "Crypto Nova Premium Indicators\n\nConoce a este Trader👇\nhttps://t.me/CryptoNovaInfo", "CryptoNova Challenge\n\nConoce a este Trader👇\nhttps://t.me/CryptoNovaInfo", "CTI BLACK Spot\n\nConoce a este Trader👇\nhttps://t.me/CTIBlackInfo", "CTI BLACK Futuros\n\nConoce a este Trader👇\nhttps://t.me/CTIBlackInfo", "Team Camilo VIP\n\nConoce a este Trader👇\nhttps://t.me/TeamCamiloInfo", "Maverick Trading\n\nConoce a este Trader👇\nhttps://t.me/MaverickTradingInfo", "Ozzy Master Spot(Miami Trading)\n\nConoce a este Trader👇\nhttps://t.me/ozzyInfo", "Ozzy Master Futuros(Miami Trading)\n\nConoce a este Trader👇\nhttps://t.me/ozzyInfo", "APILeakers - Binance Announcements\n\nConoce a este Trader👇\nhttps://t.me/APILeakersInfo", "APILeakers - Coin Gecko Listing\n\nConoce a este Trader👇\nhttps://t.me/APILeakersInfo" , "APILeakers  -CoinMArketCap Listing\n\nConoce a este Trader👇\nhttps://t.me/APILeakersInfo"]
nombre_de_canales_ing_html = ["Always Win VIP</b>\n<i><a href='https://t.me/AlwaysWinInfo'>Conoce a este Trader</a></i>🔎", "The Bull</b>\n<i><a href='https://t.me/TheBullInfo'>Conoce a este Trader</a></i>🔎", "Kim Crypto</b>\n<i><a href='https://t.me/KimCryptoInfo'>Conoce a este Trader</a></i>🔎", "Inner Circle</b>\n<i><a href='https://t.me/InnerCircleInfo'>Conoce a este Trader</a></i>🔎", "KilMex</b>\n<i><a href='https://t.me/KillMexInfo'>Conoce a este Trader</a></i>🔎", "Haven CBS\n-Haven Loma\n-Haven Krillin\n-Haven Pierre</b>\n<i><a href='https://t.me/TheHavenInfo'>Conoce a este Trader</a></i>🔎", "Alex Clay Alts\n-Alex Clay Margin\n-Alex Clay Scalping</b>\n<i><a href='https://t.me/AlexClayInfo'>Conoce a este Trader</a></i>🔎", "Krypton Wolf</b>\n<i><a href='https://t.me/KryptonWolfInfo'>Conoce a este Trader</a></i>🔎", "Birb Nest</b>\n<i><a href='https://t.me/BirbNestInfo'>Conoce a este Trader</a></i>🔎", "Elon Trades</b>\n<i><a href='https://t.me/ElonTradesInfo_esp'>Conoce a este Trader</a></i>🔎", "Raticoin Alts\n-Raticoin Margin</b>\n<i><a href='https://t.me/raticoinInfo_esp'>Conoce a este Trader</a></i>🔎", "Bitcoin Bullets</b>\n<i><a href='https://t.me/BitcoinBulletsInfo'>Conoce a este Trader</a></i>🔎", "Margin Whales</b>\n<i><a href='https://t.me/MarginWhalesInfo'>Conoce a este Trader</a></i>🔎", "Rose Premium Signal 2022</b>\n<i><a href='https://t.me/RosePremiumSignalsInfo'>Conoce a este Trader</a></i>🔎", "Fat Pig Signals</b>\n<i><a href='https://t.me/FatPigSignalsInfo'>Conoce a este Trader</a></i>🔎", "Binance Killers</b>\n<i><a href='https://t.me/BinanceKillersInfo'>Conoce a este Trader</a></i>🔎", "FED Russian Insiders</b>\n<i><a href='https://t.me/FedRussianInsidersInfo'>Conoce a este Trader</a></i>🔎", "APILeakers - Binance Announcements</b>\n<i><a href='https://t.me/APILeakersInfo'>Conoce a este Trader</a></i>🔎", "APILeakers - CoinGecko Listing</b>\n<i><a href='https://t.me/APILeakersInfo'>Conoce a este Trader</a></i>🔎", "APILeakers - CoinMarketCap Listing</b>\n<i><a href='https://t.me/APILeakersInfo'>Conoce a este Trader</a></i>🔎"]
nombre_de_canales_esp_html = ["Trading Latino</b>\n<i><a href='https://t.me/TradingLatinoInformacion'>Conoce a este Trader</a></i>🔎", "BitLobo</b>\n<i><a href='https://t.me/BitLoboInfo'>Conoce a este Trader</a></i>🔎", "InvestClub</b>\n<i><a href='https://t.me/InvestClubInfo'>Conoce a este Trader</a></i>🔎", "CryptoNova Premium Indicators\n-CryptoNova Challenge</b>\n<i><a href='https://t.me/CryptoNovaInfo'>Conoce a este Trader</a></i>🔎", "CTI BLACK Spot\n-CTI BLACK Futuros</b>\n<i><a href='https://t.me/CTIBlackInfo'>Conoce a este Trader</a></i>🔎", "TeamCamilo</b>\n<i><a href='https://t.me/TeamCamiloInfo'>Conoce a este Trader</a></i>🔎", "Maverick Trading</b>\n<i><a href='https://t.me/MaverickTradingInfo'>Conoce a este Trader</a></i>🔎", "Ozzy VIP Spot</b>\n<i><a href='https://t.me/ozzyInfo'>Conoce a este Trader</a></i>🔎","Ozzy VIP Spot</b>\n<i><a href='https://t.me/ozzyInfo'>Conoce a este Trader</a></i>🔎", "APILeakers</b>\n<i><a href='https://t.me/APILeakersInfo'>Conoce a este Trader</a></i>🔎", "APILeakers - Anuncios de Binance</b>\n<i><a href='https://t.me/APILeakersInfo'>Conoce a este Trader</a></i>🔎", "APILeakers - CoinGecko Listing</b>\n<i><a href='https://t.me/APILeakersInfo'>Conoce a este Trader</a></i>🔎", "APILeakers - Nuevos Listados CoinMarketCap</b>\n<i><a href='https://t.me/APILeakersInfo'>Conoce a este Trader</a></i>🔎"]
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
    text = "<b><u>Faltan 3 días para que acabe tu plan ⏳</u></b>\n\n<i>SI RENUEVAS HOY TE REGALAMOS 2 DÍAS 🎁</i>.\n\n(Tus 3 días que faltan + 2 días de regalo + 1 mes de suscripción = <b>35 días/$6</b>)\n¡Esta promoción caduca en 24h!\n(aplica a cualquier paquete)"
    mensaje = context.bot.send_message(job.context, text=text, parse_mode=ParseMode.HTML)
    mensaje1 = mensaje.message_id
    chat_id_ = mensaje.chat_id
    fecha_temprana = 5
def alarm2(context: CallbackContext) -> None:
    global mensaje2, fecha_temprana
    job = context.job
    text = "<b><u>Faltan 2 días para que acabe tu plan ⏳</u></b>\n\n<i>SI RENUEVAS HOY TE REGALAMOS 1 DÍA 🎁</i>.\n\n(Tus 2 días que faltan + 1 días de regalo + mes de suscripción = <b>33 días/$6</b>)\n¡Esta promoción caduca en 24h!\n(aplica a cualquier paquete)"
    mensaje = context.bot.send_message(job.context, text=text, parse_mode=ParseMode.HTML)
    mensaje2 = mensaje.message_id
    context.bot.delete_message(chat_id=mensaje.chat_id, message_id=mensaje1)
    fecha_temprana = 3
def alarm3(context: CallbackContext) -> None:
    global mensaje3, fecha_temprana
    job = context.job
    text = "<b>❗️Tu plan está muy próximo a vencer! ⌛️.\n\n<i>Serás expulsado de los canales dentro de las próximas 24h</i></b>. Puedes contratar un plan desde $6 con el botón de arriba 👆"
    mensaje = context.bot.send_message(job.context, text=text, parse_mode=ParseMode.HTML)
    mensaje3 = mensaje.message_id
    context.bot.delete_message(chat_id=mensaje.chat_id, message_id=mensaje2)
    fecha_temprana = 1
def alarm4(context: CallbackContext) -> None:
    global mensaje4
    job = context.job
    text = "<b>Lo sentimos, tu plan venció y ya no puedes entrar a los canales</b> 😔\n\n<u>Puedes contratar un plan con el botón de arriba</u> 👆"
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
        [InlineKeyboardButton("🎁 PRUEBA GRATUITA 🎁", callback_data=str(ACTIVARPRUEBA))],
        [InlineKeyboardButton("⚜ Canales y Paquetes ⚜", callback_data=str(PACKS))],
        [InlineKeyboardButton("Código de acceso 🔑", callback_data=str(COD))],        
        [InlineKeyboardButton("Saber más ❔", callback_data=str(SABER))]        
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Enviar mensaje de text junto con el teclado
    user = update.message.from_user
    context.bot.send_photo(chat_id, "https://i.postimg.cc/Kb9gJMyr/photo-2022-03-06-08-30-05.jpg?dl=1")
    if nuevo_usuario == True:
        texto = "Hola " + user.first_name + "!\n\n🎁 Puedes activar tu prueba gratuita de 10 días para TODOS los canales sin compromiso.🎁\n\n<b>⚠️OFERTA POR TIEMPO LIMITADO⚠️</b>\n\nSabemos lo dificil que está siendo para algunos este Bear Market 🐻 y por eso queremos ayudar a nuestros actuales y futuros usuarios con esta SUPER PROMOCIÓN ❤️\n\nSi ya estás suscrito o te suscribes antes de que termine la promoción📆 <i>(max. 120 personas)</i> tendrás TODOS LOS CANALES A MITAD DE PRECIO <u>50%OFF</u> durante todo el tiempo que se alargue el Bear Market.📉\n\nY si aguantaste con nosotros hasta que acaben estos malos momentos 🤝 te premiaremos manteniendo la misma tarifa <u>DE POR VIDA</u> 🤜🤛\n\n"
    if nuevo_usuario == False:
        texto = "Hola " + user.first_name + "!\n\n🎁 Si tu prueba ha finalizado por favor elige un paquete.👍\n\n<b>⚠️OFERTA POR TIEMPO LIMITADO⚠️</b>\n\nSabemos lo dificil que está siendo para algunos este Bear Market 🐻 y por eso queremos ayudar a nuestros actuales y futuros usuarios con esta SUPER PROMOCIÓN ❤️\n\nSi ya estás suscrito o te suscribes antes de que termine la promoción📆 <i>(max. 120 personas)</i> tendrás TODOS LOS CANALES Y PAQUETES A MITAD DE PRECIO <u>50%OFF</u> durante todo el tiempo que se alargue el Bear Market.📉\n\nY si aguantaste con nosotros hasta que acaben estos malos momentos 🤝 te premiaremos manteniendo la misma tarifa <u>DE POR VIDA</u> 🤜🤛\n\n"
        
    
    update.message.reply_text(texto, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return PRIMERO 

def start2(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("🎁 PRUEBA GRATUITA 🎁", callback_data=str(ACTIVARPRUEBA))],
        [InlineKeyboardButton("⚜ Canales y Paquetes ⚜", callback_data=str(PACKS))],
        [InlineKeyboardButton("Código de acceso 🔑", callback_data=str(COD))],        
        [InlineKeyboardButton("Saber más ❔", callback_data=str(SABER))]        
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Enviar mensaje de text junto con el teclado
    if nuevo_usuario == True:
        texto = "Hola " + user.first_name + "!\n\n🎁 Puedes activar tu prueba gratuita de 10 días para TODOS los canales sin compromiso.🎁\n\n<b>⚠️OFERTA POR TIEMPO LIMITADO⚠️</b>\n\nSabemos lo dificil que está siendo para algunos este Bear Market 🐻 y por eso queremos ayudar a nuestros actuales y futuros usuarios con esta SUPER PROMOCIÓN ❤️\n\nSi ya estás suscrito o te suscribes antes de que termine la promoción📆 <i>(max. 120 personas)</i> tendrás TODOS LOS CANALES A MITAD DE PRECIO <u>50%OFF</u> durante todo el tiempo que se alargue el Bear Market.📉\n\nY si aguantaste con nosotros hasta que acaben estos malos momentos 🤝 te premiaremos manteniendo la misma tarifa <u>DE POR VIDA</u> 🤜🤛\n\n"
    if nuevo_usuario == False:
        texto = "Hola " + user.first_name + "!\n\n🎁 Si tu prueba ha finalizado por favor elige un paquete.👍\n\n<b>⚠️OFERTA POR TIEMPO LIMITADO⚠️</b>\n\nSabemos lo dificil que está siendo para algunos este Bear Market 🐻 y por eso queremos ayudar a nuestros actuales y futuros usuarios con esta SUPER PROMOCIÓN ❤️\n\nSi ya estás suscrito o te suscribes antes de que termine la promoción📆 <i>(max. 120 personas)</i> tendrás TODOS LOS CANALES Y PAQUETES A MITAD DE PRECIO <u>50%OFF</u> durante todo el tiempo que se alargue el Bear Market.📉\n\nY si aguantaste con nosotros hasta que acaben estos malos momentos 🤝 te premiaremos manteniendo la misma tarifa <u>DE POR VIDA</u> 🤜🤛\n\n"
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
        [InlineKeyboardButton(text="Volver ↩️", callback_data=str(START))],
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
        [InlineKeyboardButton(text="Comprobar validéz 🎟", callback_data=str(COD_COMP))],
        [InlineKeyboardButton(text="Volver ↩️", callback_data=str(START))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)    

    query.edit_message_text(
        text="<b><u>¿Cómo canjear mi código?</u>\n\n1️⃣ Debes escribir el código y enviárlo</b>,\n2️⃣ Dale al botón 'Comprobar validéz 🎟'", reply_markup=reply_markup, parse_mode=ParseMode.HTML
    )
    mensaje_continuar = context.bot.send_message(chat_id =chat_id, text="Envía tu código y dale a 'Comprobar validéz 🎟' 👆") 
    id_mensaje_comprobar = mensaje_continuar.message_id
    codigo_escrito = True

    return PRIMERO
def comprobar_codigo (update: Update, context: CallbackContext) -> int:
    global codigo_ala, codigo_usuario
    query = update.callback_query
    query.answer()
    cod1 = "Ticket 6dls"
    cod2 = "Ticket 7dls"
    cod3 = "Ticket 12dls"
    cod4 = "Ticket 13dls"
    cod5 = "Ticket 17dls"
    cod6 = "Ticket 18dls"
    ala1 = "A la 4dls"
    ala2 = "A la 7dls"
    ala3 = "A la 10dls"   

    if codigo_usuario == "":
        keyboard = [
                [InlineKeyboardButton(text="Comprobar validéz 🎟", callback_data=str(COD_COMP))],
                [InlineKeyboardButton(text="Volver ↩️", callback_data=str(COD))]
                ]
        reply_markup = InlineKeyboardMarkup(keyboard) 
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_comprobar) 
        query.edit_message_text(
            text="¡Vaya!, parece que no has envíado ningún código ❗️\n\n<b>Asegurate de <u>PRIMERO envíar el mensaje</u> y luego dale a 'Comprobar validéz'</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML
        )

        return PRIMERO          

    dic_events1 = db.find_one({"id":1})[cod1]
    cods1 = dic_events1.keys() 

    dic_events2 = db.find_one({"id":1})[cod2]
    cods2 = dic_events2.keys() 

    dic_events3 = db.find_one({"id":1})[cod3]
    cods3 = dic_events3.keys() 

    dic_events4 = db.find_one({"id":1})[cod4]
    cods4 = dic_events4.keys() 

    dic_events5 = db.find_one({"id":1})[cod5]
    cods5 = dic_events5.keys() 

    dic_events6 = db.find_one({"id":1})[cod6]
    cods6 = dic_events6.keys()  

    dic_events7 = db.find_one({"id":1})[ala1]
    alas1 = dic_events7.keys() 

    dic_events8 = db.find_one({"id":1})[ala2]
    alas2 = dic_events8.keys() 

    dic_events9 = db.find_one({"id":1})[ala3]
    alas3 = dic_events9.keys()  

    if codigo_usuario in cods1 or codigo_usuario in cods2 or codigo_usuario in alas1:
                
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
        if codigo_usuario in cods1:
            nom = cod1 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="Paquete en español ➡️", callback_data=str(LINK_ESP))],
                [InlineKeyboardButton(text="Paquete en inglés ➡️", callback_data=str(LINK_ING))],
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="¡El Código de acceso es correcto! ✅\n\nSuscripción válida por 30 días. Elige el paquete que quieres", reply_markup=reply_markup)
        elif codigo_usuario in cods2:
            nom = cod2 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="Ver links ➡️", callback_data=str(LINK_TODO))]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)            
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 30 días.", reply_markup=reply_markup)
        elif codigo_usuario in alas1:
            nom = ala1 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="A la carta en español ➡️", callback_data=str(ALA_ES))],
                [InlineKeyboardButton(text="A la carta en inglés ➡️", callback_data=str(ALA_EN))],
                ] 
            codigo_ala = True    
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 30 días. Elige el idioma del canal que deseas.", reply_markup=reply_markup)      
       
    elif codigo_usuario in cods3 or codigo_usuario in cods4 or codigo_usuario in alas2:
                
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
        if codigo_usuario in cods3:
            nom = cod3 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="Paquete en español ➡️", callback_data=str(LINK_ESP))],
                [InlineKeyboardButton(text="Paquete en inglés ➡️", callback_data=str(LINK_ING))],
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 60 días. Elige el paquete que quieras.", reply_markup=reply_markup)
        elif codigo_usuario in cods4:
            nom = cod4 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="Ver links ➡️", callback_data=str(LINK_TODO))]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)            
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 60 días.", reply_markup=reply_markup)
        elif codigo_usuario in alas2:
            nom = ala2 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="A la carta en español ➡️", callback_data=str(ALA_ES))],
                [InlineKeyboardButton(text="A la carta en inglés ➡️", callback_data=str(ALA_EN))],
                ] 
            codigo_ala = True    
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 60 días. Elige el idioma del canal que deseas.", reply_markup=reply_markup)        
      
    elif codigo_usuario in cods5 or codigo_usuario in cods6 or codigo_usuario in alas3:
        
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
        if codigo_usuario in cods5:
            nom = cod5 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}})             
            keyboard = [
                [InlineKeyboardButton(text="Paquete en español ➡️", callback_data=str(LINK_ESP))],
                [InlineKeyboardButton(text="Paquete en inglés ➡️", callback_data=str(LINK_ING))],
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 90 días. Elige el paquete que quieras.", reply_markup=reply_markup)
        elif codigo_usuario in cods6:
            nom = cod6 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="Ver links ➡️", callback_data=str(LINK_TODO))]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)            
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 90 días.", reply_markup=reply_markup)
        elif codigo_usuario in alas3:
            nom = ala3 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="A la carta en español ➡️", callback_data=str(ALA_ES))],
                [InlineKeyboardButton(text="A la carta en inglés ➡️", callback_data=str(ALA_EN))],
                ] 
            codigo_ala = True    
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 90 días. Elige el idioma del canal que deseas.", reply_markup=reply_markup)        
        else:            
            query.edit_message_text(
                text="Lo sentimos, el Código de acceso es incorrecto o ya caducó. 🚫", reply_markup=reply_markup
            )        
    else:
        keyboard = [
                [InlineKeyboardButton(text="Volver ↩️", callback_data=str(COD))]
                ]
        reply_markup = InlineKeyboardMarkup(keyboard) 

        query.edit_message_text(
            text="Lo sentimos, el Código de acceso es incorrecto o ya caducó. 🚫", reply_markup=reply_markup
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
        [InlineKeyboardButton(text="Pack Canales VIP en Español 🇪🇸 - $6", callback_data=str(PLAN_ES))],
        [InlineKeyboardButton(text="Pack Canales VIP en Ingles 🇬🇧 - $6", callback_data=str(PLAN_IN))],
        [InlineKeyboardButton(text="Pack Total (TODOS LOS CANALES) 🌐 - $7", callback_data=str(PLAN_TOTAL))],
        [InlineKeyboardButton(text="Canales a la carta 🧾 - $4", callback_data=str(ALA))],
        [InlineKeyboardButton(text="Volver ↩️", callback_data=str(START))]]
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
        text="<b>Puedes elegir entre 3 packs disponibles o elegir los canales a carta:</b>\n\n<i>-Pack de canales en Español🇪🇸\n-Pack de canales en inglés🇬🇧\n-Pack con todos los canales🌐\n-Canales a la carta📋</i>\n\n\n<u><b>Paquete en Español</b></u> 🇪🇸\n\nCosto: <b>SOLO $6/mes</b> <s>$12/mes</s> <b>(*-50%\off oferta limitada)</b> \nCanales en el pack:\n\n" + texto_canales_esp + "\n\n<u><b>Paquete en Inglés</b></u> 🇬🇧\n\nCosto: <b>SOLO $6/mes</b> <s>$12/mes</s> <b>(*-50%\off oferta limitada)</b> \nCanales en el pack:\n\n" + texto_canales_ing + "\n\n<u><b>PAQUETE TOTAL 🌐🔝</b></u>\n<b>(🔥Mejor opción Calidad-Precio🔥)</b>\n\n<i>Costo: </i><b>\nSÓLO $7/mes ✅</b> <s>$15/mes</s> <b>(*-50%\off oferta limitada 🔥)</b> \n\n<i>Canales en el pack:</i><b>\n⚜️ACCESO TOTAL A TODOS LOS CANALES Y HERRAMIENTAS⚜️</b>\n\n\n<i>ℹ️Si te interesa sólamente un canal puedes contratarlo por sólo $4/mes <s>$8/mes</s> en 'Canales a la carta' 📋</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    
    return SEGUNDO

#Cuando apriestas canales a la carta
def a_la_carta (update: Update, context: CallbackContext) -> int:
    global eleccion_a_la_carta, eleccion_a_la_carta_bool
    query = update.callback_query
    query.answer()
    eleccion_a_la_carta = []
    eleccion_a_la_carta_bool = False
    try:
        context.bot.deleteMessage (message_id = mensaje_unirse_id, chat_id = update.message.chat_id) 
    except:
        pass  
     
    keyboard = [
        [InlineKeyboardButton(text="Canales en español", callback_data=str(ALA_ES))],
        [InlineKeyboardButton(text="Canales en ingles", callback_data=str(ALA_EN))],
        [InlineKeyboardButton(text="Volver ↩️", callback_data=str(PACKS))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Si sólo estás interesado en uno o dos canales tu mejor opción son los <b>Canales a la carta</b>📋.\n\nElige entre canales en Español🇪🇸 o canales en Inglés🇬🇧:", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return SEGUNDO

def a_la_carta_ES(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones, eleccion_a_la_carta_bool
    query = update.callback_query
    query.answer()
    eleccion_a_la_carta_bool = True
    canales_lista_esp = []      
    for canal_esp in nombre_de_canales_esp_html:
        canales_esp = "<b>-"+ canal_esp+ "\n\n"
        canales_lista_esp.append(canales_esp)  

    texto_canales_esp = "".join(canales_lista_esp)
            
    if codigo_ala == False:
        keyboard = [[
                InlineKeyboardButton("Volver ↩️", callback_data=str(ALA)),
                InlineKeyboardButton("Continuar ➡️", callback_data =str(PLAN_ALA))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="<u><b>A la carta en Español</b></u> 🇪🇸\n\nCosto: <b>SÓLO $4/mes</b> <s>$8/mes</s> <b>(*-50%/off oferta limitada)</b> \nCanales:\n\n" + texto_canales_esp, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        reply_keyboard = []

    if codigo_ala == True:
        keyboard = [[
                InlineKeyboardButton("Volver ↩️", callback_data=str(ALA)),
                InlineKeyboardButton("Continuar ➡️", callback_data =str(LINK_ALA))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="<u><b>A la carta en Español</b></u> 🇪🇸\n\nCosto: <b>SÓLO $4/mes</b> <s>$8/mes</s> <b>(*-50%/off oferta limitada)</b> \nCanales:\n\n" + texto_canales_esp, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        reply_keyboard = []            
    for canal in nombre_de_canales_esp_texto:
        lista_canal = []
        lista_canal.append(canal)
        reply_keyboard.append(lista_canal)
        
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="NO ESCRIBIR", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="Después de elegir el canal dale a continuar 👆", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id 
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
                InlineKeyboardButton("Volver ↩️", callback_data=str(ALA)),
                InlineKeyboardButton("Continuar ➡️", callback_data =str(PLAN_ALA))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="<u><b>A la carta en Inglés</b></u> 🇬🇧\n\nCosto: <b>SÓLO $4/mes</b> <s>$8/mes</s> <b>(*-50%/off oferta limitada)</b> \nCanales:\n\n" + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        reply_keyboard = []
    if codigo_ala == True:

                
        keyboard = [[
                InlineKeyboardButton("Volver ↩️", callback_data=str(ALA)),
                InlineKeyboardButton("Continuar ➡️", callback_data =str(LINK_ALA))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="<u><b>A la carta en Inglés</b></u> 🇬🇧\n\nCosto: <b>SÓLO $4/mes</b> <s>$8/mes</s> <b>(*-50%/off oferta limitada)</b> \nCanales:\n\n" + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        reply_keyboard = []
            
    for canal in nombre_de_canales_eng_texto:
        lista_canal = []
        lista_canal.append(canal)
        reply_keyboard.append(lista_canal)
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="NO ESCRIBIR", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="Después de elegir el canal dale a continuar 👆", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id 
    return SEGUNDO 

#sección donde se muestran los planes disponibles
def verPlanesEspanol(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones, eleccionCantidad_bool, plan_esp
    query = update.callback_query
    query.answer()
    keyboard = [[
            InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Continuar ➡️", callback_data =str(TIPO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="<u><b>Paquete en Español</b></u> 🇪🇸\n\nCosto: <b>SÓLO $6/mes</b> <s>$12/mes</s> <b>(*-50%/off oferta limitada)</b> \nCanales en el pack:\n\n" + texto_canales_esp, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    reply_keyboard = [['1 mes de membresía, $6.00/1 mes'], ['2 meses de membresía, $12.00/2 meses'], ['3 meses de membresía, $17.00/3 meses']]
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="NO ESCRIBIR", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="Después de elegir la duración dale a continuar 👆", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id 
    eleccionCantidad_bool = True
    plan_esp = True
    return SEGUNDO
#sección donde se muestran los planes disponibles
def verPlanesIngles(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones, eleccionCantidad_bool, plan_ing
    query = update.callback_query
    query.answer()
    keyboard = [[
            InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Continuar ➡️", callback_data =str(TIPO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="<u><b>Paquete en Inglés</b></u> 🇬🇧\n\nCosto: <b>SÓLO $6/mes</b> <s>$12/mes</s> <b>(*-50%/off oferta limitada)</b> \nCanales en el pack:\n\n" + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    reply_keyboard = [['1 mes de membresía, $6.00/1 mes'], ['2 meses de membresía, $12.00/2 meses'], ['3 meses de membresía, $17.00/3 meses']]
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="NO ESCRIBIR", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="Después de elegir la duración dale a continuar 👆", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id 
    eleccionCantidad_bool = True
    plan_ing = True
    return SEGUNDO

#sección donde se muestran los planes disponibles
def verPlanesTotal(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones, eleccionCantidad_bool, data_eleccion, plan_todo
    query = update.callback_query
    query.answer()
    data_eleccion = update.callback_query.data 
    print(data_eleccion)
    keyboard = [[
            InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Continuar ➡️", callback_data =str(TIPO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="<u><b>Paquete TOTAL</b></u> 🌐\n\nCosto: <b>SÓLO $7/mes</b> <s>$14/mes</s> <b>(*-50%/off oferta limitada)</b> Con este Pack vienen incluidos TODOS LOS CANALES y son los siguientes:\n\n" + texto_canales_esp + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    reply_keyboard = [['1 mes de membresía, $7.00/1 mes'], ['2 meses de membresía, $13.00/2 meses'], ['3 meses de membresía, $18.00/3 meses']]
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="NO ESCRIBIR", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="Después de elegir la duración dale a continuar 👆", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id    
    eleccionCantidad_bool = True 
    plan_todo = True
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
            InlineKeyboardButton("Volver ↩️", callback_data=str(ALA)),
            InlineKeyboardButton("Continuar ➡️", callback_data =str(TIPO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(
        text="Has elegido el canal "+eleccion_a_la_carta[0]+"\n\nCuando selecciones la duración de tu paquete, dale a continuar", reply_markup=reply_markup)
    reply_keyboard = [['1 mes de membresía, $4.00/1 mes'], ['2 meses de membresía, $7.00/2 meses'], ['3 meses de membresía, $10.00/3 meses']]
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="NO ESCRIBIR", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="Después de elegir la duración dale a continuar 👆", reply_markup=reply_markup2)    
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
            [InlineKeyboardButton("CoinPayments (Automático)", callback_data=str(RED))],
            [InlineKeyboardButton("BinancePay (Manual)", callback_data =str(PAY))],
            [InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS))]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        if "1 mes" in eleccion[0]:
            query.edit_message_text(
                text="<b><u>Elige el método de Pago:</u>\n\nCoinPayments</b>\nEl pago por CoinPayments es gestionado autmomáticamente por la plataforma.\n\Comisiones: $1 aprox.\n\n⚠️ <i>Algunos exchanges como Binance no permiten tranferencias menores a $10 por lo que te recomendamos contratar un paquete de 2 meses, utilizar Binance Pay como fomra de pago o elegir otro exchange como Kucoin que no tenga monto mínimo de transferencia.</i>\n\n<b>Binance Pay</b>\nLos pagos por Binance Pay son SIN COMISIONES.\n⚠️<i> La comprobación del pago se hace de manera MANUAL, por lo qué puede demorar desde unos minutos hasta unas horas (*según disponiblidad horaria del administrador).</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        else:
            print("Se activo el except")
            query.edit_message_text(
                text="<b><u>Elige el método de Pago:</u>\n\nCoinPayments</b>\nEl pago por CoinPayments es gestionado autmomáticamente por la plataforma.\n\Comisiones: $1 aprox.\n\n<b>Binance Pay</b>\nLos pagos por Binance Pay son SIN COMISIONES.\n⚠️<i> La comprobación del pago se hace de manera MANUAL, por lo qué puede demorar desde unos minutos hasta unas horas (*según disponiblidad horaria del administrador).</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except:
        print("Hubo un error")   

    return PRIMERO
    
def tipoDeRed(update: Update, context: CallbackContext) -> int:
    global duracion, mensaje_id_elecciones, eleccionCantidad_bool, eleccionRed_bool
    query = update.callback_query
    query.answer()
    eleccionRed_bool = True
    keyboard = [[
            InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Continuar ➡️", callback_data =str(TRAN))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Los pagos se hacen a través de la plataforma Coinpayments en la moneda USDT (Tether USD, ¡NO BUSD!) en cualquiera de las redes Blockchain disponibles.", reply_markup=reply_markup)
    reply_keyboard = [['⚡️ USDT.BEP20 - Theter USD (BEP20 / BSC)'], ['⚡️ USDT.TRC20 - Theter USD (TRC20 / Tron Chain)']]
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="NO ESCRIBIR", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="Elige la red que prefieras, presiona continuar y espera aque se genere tu órden.", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id
    return PRIMERO
  
def BinancePay(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones, mensaje_id_elecciones2
    query = update.callback_query
    query.answer()
    try:
        if "1 mes de membresía," in eleccion[0]:
            if plan_todo == True: 
                mensaje = context.bot.send_photo(chat_id, photo="https://i.imgur.com/kZlXzfb.jpeg", caption="<b><u>Costo del paquete: $7\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
            elif plan_esp == True or plan_ing == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/X7O2kWL.jpeg", caption="<b><u>Costo del paquete: $6\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
            elif plan_a_la == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/mDGVbkj.jpeg", caption="<b><u>Costo del canal: $4\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
        
        if "2 meses de membresía" in eleccion[0]:
            if plan_todo == True: 
                mensaje = context.bot.send_photo(chat_id, photo="https://i.imgur.com/sKrTfko.jpeg", caption="<b><u>Costo del paquete por 2 meses: $13\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
            elif plan_esp == True or plan_ing == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/BuXJGQ6.jpeg", caption="<b><u>Costo del paquete por 2 meses: $12\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)      
            elif plan_a_la == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/kZlXzfb.jpeg", caption="<b><u>Costo del canal por 2 meses: $7\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)

        if "3 meses de membresía" in eleccion[0]:
            if plan_todo == True: 
                mensaje = context.bot.send_photo(chat_id, photo="https://i.imgur.com/pJLjYy6.jpeg", caption="<b><u>Costo del paquete por 3 meses: $18\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
            elif plan_esp == True or plan_ing == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/o6igYQV.jpeg", caption="<b><u>Costo del paquete por 3 meses: $17\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
            elif plan_a_la == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://i.imgur.com/IsQThAq.jpeg", caption="<b><u>Costo del canal por 3 meses: $10\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
    except:
        context.bot.send_message(chat_id, text="Hubo un error eligiendo el valor del paquete, por favor reinicia el bot eligiendo el precio del paquete que deseas.\n\nSi sigues experimentando problemas por favor contacta al admin @HispanLeaksAdmin y lo resolveremos a la brevedad posible.")

    mensaje_id_elecciones = mensaje.message_id
    return ConversationHandler.END

def transaccion(update: Update, context: CallbackContext) -> int:
    global plan, eleccionRed_bool
    query = update.callback_query
    query.answer()
    eleccionRed_bool = False
    context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_continuar)  
    nombre = usuario
    if "1 mes de membresía" in eleccion[0]:
        if plan_todo == True:
            plan = 1
            cantidad = 7
        elif plan_a_la == True:
            plan = 1
            cantidad = 4 
        else:
            plan = 1
            cantidad = 6
    
    if "2 meses de membresía" in eleccion[0]:
        if plan_todo == True:
            plan = 2
            cantidad = 13
        elif plan_a_la == True:
            plan = 2
            cantidad = 7             
        else:
            plan = 2
            cantidad = 12
        

    if "3 meses de membresía" in eleccion[0]:
        if plan_todo == True:
            plan = 3
            cantidad = 18
        elif plan_a_la == True:
            plan = 3
            cantidad = 10             
        else:
            plan = 3
            cantidad = 17
        
    if "USDT.BEP20" in eleccion[1]:
        moneda = "USDT.BEP20"  
    if "USDT.TRC20" in eleccion[1]:
        moneda = "USDT.TRC20"          

    actualizarBD(usuario, "Plan", plan) 

    #generar un pago
    crearTransaccion(cantidad, moneda, nombre)

    keyboard = [
        [
            InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Comprobar suscripción 🔄", callback_data=str(COMP))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(text='Para asegurarte que la transacción no falle te recomendamos envíar al menos $0.05c extra. \n<a href="'+qrcode+'">&#8205;</a>', reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    query.edit_message_text(
        text="Pago por CoinPayments\n\n<b>Dirección de la billetera:</b>\n<code>" + address + "</code>\n\n<b>Cantidad de USDT a envíar:</b>\n$" + str(amount) + " (" + moneda + ")\n\n⚠️La plataforma Coinpayments solo dará por arpobada la transacción cuando se cubra el monto TOTAL del pago\n❗️El enlace de pago caduca en 1 día\n\nSi tienes algún problema con el pago contacta a @HispanLeaksAdmin, te atenderemos lo antes posible.\n\n<a href='"+link+"'>Comprueba el estado de la transacción en Coinpayments.net</a>" , parse_mode="HTML")
 
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
            InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Comprobar suscripción 🔄", callback_data=str(COMP))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            query.edit_message_text(
                text="<b>No se ha recibido el pago. El tiempo aproximado de la transacción es de 30 min.</b>\n\nSi tienes algun problema con la transacción contacta a @HispanLeaksAdmin, te atenderemos lo antes posible.\n\n<a href='"+link+"'>Mira el estátus de la transacción en Coinpayments</a>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except:
            query.edit_message_text(
                text="No se ha recibido ningún pago. El tiempo aproximado de la transacción es de 30 min.\n\nSi tienes algun problema con la transacción contacta a @HispanLeaksAdmin, te atenderemos lo antes posible.", reply_markup=reply_markup)  

    if status == 1:
        keyboard = [[
            InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Comprobar suscripción 🔄", callback_data=str(COMP))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        try:
            query.edit_message_text(
                text="<b>Se ha detectado la transacción, esperando 10 confirmaciones. Vuelve a probar tras unos minutos.</b>\n\nSi tienes algun problema con la transacción contacta a @HispanLeaksAdmin, te atenderemos lo antes posible.\n\n<a href='"+link+"'>Mira el estátus de la transacción en Coinpayments</a>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except:
            query.edit_message_text(
                text="No se ha recibido ningún pago.\n\nSi tienes algun problema con la transacción contacta a @HispanLeaksAdmin, te atenderemos lo antes posible.", reply_markup=reply_markup)  
 

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
                    
            if plan_esp == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_ESP))]]

            if plan_ing == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_ING))]]
            if plan_todo == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_TODO))]]
            if eleccion_a_la_carta_bool == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_ALA))]]                        

            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="<b>¡Pago recibido!✅.\n<i>Tu membresía está activa por 1 mes 🎉</i></b>\n\nPresiona el botón <i>'Ver links🔗'</i> sólo una vez y espera a que carguen los enlaces.\n\n⚠️<i>Si te unes a los canales VIP demasiado rápido Telegram bloqueará temporalmente la función, en ese caso solo debes esperar unos minutos y volver a intentarlo</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            ahora = datetime.now()
            
            fecha_plan = ahora + timedelta(days=dias)
            dic_event = "Fecha"
            actualizarBD(usuario, dic_event, fecha_plan)
            estatus = "Estatus"
            estatus_mode = True
            actualizarBD(usuario, estatus, estatus_mode)
            os.system('python3 pyro.py')


        if plan == 2:
            actualizarBD(usuario, nombre, plan) 
            dias = 60
            avisos =alarma(dias)
            context.job_queue.run_once(alarm1, avisos[0], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm2, avisos[1], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm3, avisos[2], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm4, avisos[3], context=chat_id, name=str(chat_id))    
                    

            if plan_esp == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_ESP))]]

            if plan_ing == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_ING))]]

            if plan_todo == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_TODO))]]     
            if eleccion_a_la_carta_bool == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_ALA))]]   

            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="<b>¡Pago recibido!✅.\n<i>Tu membresía está activa por 2 meses 🎉</i></b>\n\nPresiona el botón <i>'Ver links🔗'</i> sólo una vez y espera a que carguen los enlaces.\n\n⚠️<i>Si te unes a los canales VIP demasiado rápido Telegram bloqueará temporalmente la función, en ese caso solo debes esperar unos minutos y volver a intentarlo</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            ahora = datetime.now()
            fecha_plan = ahora + timedelta(days=60)
            dic_event = "Fecha"
            actualizarBD(usuario, dic_event, fecha_plan) 
            estatus = "Estatus"
            estatus_mode = True
            actualizarBD(usuario, estatus, estatus_mode)
            os.system('python3 pyro.py')  

        if plan == 3:
            actualizarBD(usuario, nombre, plan) 
            dias = 90
            avisos =alarma(dias)
            context.job_queue.run_once(alarm1, avisos[0], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm2, avisos[1], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm3, avisos[2], context=chat_id, name=str(chat_id)) 
            context.job_queue.run_once(alarm4, avisos[3], context=chat_id, name=str(chat_id))    
                    
            if plan_esp == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_ESP))]]

            if plan_ing == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_ING))]]

            if plan_todo == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_TODO))]]     
            reply_markup = InlineKeyboardMarkup(keyboard)
            if eleccion_a_la_carta_bool == True:
                keyboard = [[
                    InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_ALA))]]               
            query.edit_message_text(
                text="<b>¡Pago recibido!✅.\n<i>Tu membresía está activa por 3 meses 🎉</i></b>\n\nPresiona el botón <i>'Ver links🔗'</i> sólo una vez y espera a que carguen los enlaces.\n\n⚠️<i>Si te unes a los canales VIP demasiado rápido Telegram bloqueará temporalmente la función, en ese caso solo debes esperar unos minutos y volver a intentarlo</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            ahora = datetime.now()
            fecha_plan = ahora + timedelta(days=dias)
            dic_event = "Fecha"
            actualizarBD(usuario, dic_event, fecha_plan) 
            estatus = "Estatus"
            estatus_mode = True
            actualizarBD(usuario, estatus, estatus_mode)
    os.system('python3 pyro.py')           

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
            keyboard = [[InlineKeyboardButton("⚜ Contratar un plan ⚜", callback_data=str(PACKS))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text="Tu prueba gratuita terminó ⌛️\n\nContrata un plan para seguir en los canales", reply_markup=reply_markup)
        else:
            keyboard = [[InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="Tu prueba no vence todavía ⏳", reply_markup=reply_markup)
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
            InlineKeyboardButton("Ver links 🔗", callback_data=str(LINK_TODO))]]     
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="🎉 <b>¡Felicidades! tu prueba de <u>10 días con acceso a todos los canales</u> ha sido activada!</b> 🎁\n\nPresiona el boton una vez y espera a que se carguen los links👇<i>\n(Paciencia, puede demorar unos segundos⏳)\n\n⚠️Si te unes a los canales VIP demasiado rápido Telegram bloqueará temporalmente la función, en ese caso solo debes esperar unos minutos y volver a intentarlo</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        os.system('python3 pyro.py')

    return SEGUNDO

def email(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton(text="1 mes de membresía, $10.00/1 mes", callback_data=str(RED))],
        [InlineKeyboardButton(text="3 meses de membresía, $30.00/3 meses", callback_data=str(MES2))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Introduce tu email si quieres que se incluya en la transacción:", reply_markup=reply_markup)
    return SEGUNDO 

def help(update: Update, context: CallbackContext) -> int:
    
    context.bot.send_message(chat_id, text="Para reiniciar el bot sólo escribe o presiona en -> /start <-\n\nSi el fallo no se soluciona reiniciando, por favor contacta con el administrador @HispanLeaksAdmin")
    return ConversationHandler.END

def links_esp(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    dic_events = db.find_one({"id":0})["events"]
    enlaces = dic_events["link_grupos_esp"]
    canal = 0
    for grup in enlaces:
        keyboard = [
            [InlineKeyboardButton(text="⚜ Únete al canal VIP ⚜", url=grup),
            InlineKeyboardButton(text="Saber más de este trader 🔎", url=grup)],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text=nombre_de_canales_esp[canal], reply_markup=reply_markup) 
        canal +=1 
    keyboard = [
        [InlineKeyboardButton("⚜ Contratar un plan", callback_data=str(PACKS))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.message.reply_text(text="⏰ Te informaremos cuando esté por vencer tu membresía. ⚠️ <b>Los links son válidos para un sólo uso y estarán activos por 3 días</b>\n\n<u><i>ℹ️Si tienes algún problema, duda, sugerencia, quieres colaborar en el sistema de referidos o si bien pagas por uno o varios canales Premium y quieres ser socio, comunícate con nosotros a través del único contacto oficial en Telegram @HispanLeaksAdmin, te responderemos lo antes posible🙂ℹ️</i></u>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return SEGUNDO

def links_ing(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    dic_events = db.find_one({"id":0})["events"]
    enlaces = dic_events["link_grupos_ing"]
    canal = 0          
    for grup in enlaces:
        keyboard = [
            [InlineKeyboardButton(text="⚜ Únete al canal VIP ⚜", url=grup),
            InlineKeyboardButton(text="Saber más de este trader 🔎", url=grup)],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text=nombre_de_canales_ing[canal], reply_markup=reply_markup) 
        canal +=1    
    keyboard = [
        [InlineKeyboardButton("⚜ Contratar un plan", callback_data=str(PACKS))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.message.reply_text(text="⏰ Te informaremos cuando esté por vencer tu membresía. ⚠️ <b>Los links son válidos para un sólo uso y estarán activos por 3 días</b>\n\n<u><i>ℹ️Si tienes algún problema, duda, sugerencia, quieres colaborar en el sistema de referidos o si bien pagas por uno o varios canales Premium y quieres ser socio, comunícate con nosotros a través del único contacto oficial en Telegram @HispanLeaksAdmin, te responderemos lo antes posible🙂ℹ️</i></u>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
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

def links_todo(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    dic_events = db.find_one({"id":0})["events"]
    enlaces_esp = dic_events["link_grupos_esp"]
    enlaces_ing = dic_events["link_grupos_ing"]
    enlaces_info_esp = dic_events["links_info_esp"]
    enlaces_info_ing = dic_events["links_info_ing"]

    canal = 0
    for grup, info in zip(enlaces_esp, enlaces_info_esp):
        keyboard = [
            [InlineKeyboardButton(text="⚜ Únete al canal VIP ⚜", url=grup),
            InlineKeyboardButton(text="Saber más de este trader 🔎", url=info)],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text=nombre_de_canales_esp[canal], reply_markup=reply_markup, disable_web_page_preview = True) 
        canal +=1 

    canal = 0
    for grup, info in zip(enlaces_ing, enlaces_info_ing):

        keyboard = [
            [InlineKeyboardButton(text="⚜ Únete al canal VIP ⚜", url=grup),
            InlineKeyboardButton(text="Saber más de este trader 🔎", url=info)],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text=nombre_de_canales_ing[canal], reply_markup=reply_markup, disable_web_page_preview = True) 
        canal +=1     


    keyboard = [
        [InlineKeyboardButton("⚜ Contratar un plan", callback_data=str(PACKS))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(text="⏰ Te informaremos cuando esté por vencer tu membresía. ⚠️ <b>Los links son válidos para un sólo uso y estarán activos por 3 días</b>\n\n<u><i>ℹ️Si tienes algún problema, duda, sugerencia, quieres colaborar en el sistema de referidos o si bien pagas por uno o varios canales Premium y quieres ser socio, comunícate con nosotros a través del único contacto oficial en Telegram @HispanLeaksAdmin, te responderemos lo antes posible🙂ℹ️</i></u>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
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
    if '1 mes de membresía' in input_usuario or '2 meses de membresía' in input_usuario or '3 meses de membresía' in input_usuario or input_usuario == '⚡️ USDT.BEP20 - Theter USD (BEP20 / BSC)' or input_usuario == '⚡️ USDT.TRC20 - Theter USD (TRC20 / Tron Chain)':  
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje) 
        context.bot.delete_message(chat_id=chat_id, message_id=mensaje_id_elecciones) 
        mensaje_continuar = context.bot.send_message(chat_id =chat_id, text="Dale a continuar 👆") 
        id_mensaje_continuar = mensaje_continuar.message_id
      
    if eleccion_a_la_carta_bool == True:
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje) 
            context.bot.delete_message(chat_id=chat_id, message_id=mensaje_id_elecciones)         
        except:
            pass  
             
        ids.append(id_mensaje)
        eleccion_a_la_carta.append(input_usuario) 
        print("Se registro en la variable la eleccion " + input_usuario)
        mensaje_continuar = context.bot.send_message(chat_id =chat_id, text="Dale a continuar 👆") 
        id_mensaje_continuar = mensaje_continuar.message_id
    if codigo_escrito == True:
        codigo_usuario = input_usuario

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater('5342854757:AAGhL0uidihNAOHUadSPFKsfW587EgOdlxA') #"5239051961:AAGc9Yo9LT4x8sgaC5ydLtzFemQCDiQQaBc")
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
                CallbackQueryHandler(links_esp, pattern='^' + str(LINK_ESP) + '$'),
                CallbackQueryHandler(links_ing, pattern='^' + str(LINK_ING) + '$'),                
                CallbackQueryHandler(links_todo, pattern='^' + str(LINK_TODO) + '$'), 
                MessageHandler(Filters.text, main_handler),
                CallbackQueryHandler(start2, pattern='^' + str(START) + '$'),
                CallbackQueryHandler(saber_mas, pattern='^' + str(SABER) + '$'),
                CallbackQueryHandler(tipoDePago, pattern = '^' + str(TIPO) + '$'),
                CallbackQueryHandler(BinancePay, pattern = '^' + str(PAY) + '$'),
                CallbackQueryHandler(tipoDeRed, pattern='^' + str(RED) + '$'),
                CallbackQueryHandler(codigo_acceso, pattern='^' + str(COD) + '$'),
                CallbackQueryHandler(comprobar_codigo, pattern='^' + str(COD_COMP) + '$'),
                CallbackQueryHandler(a_la_carta_ES, pattern='^' + str(ALA_ES) + '$'), 
                CallbackQueryHandler(a_la_carta_EN, pattern='^' + str(ALA_EN) + '$'),                
            ],
            SEGUNDO: [
                CommandHandler('help', help),
                CallbackQueryHandler(paquetes, pattern='^' + str(PACKS) + '$'),
                CallbackQueryHandler(tipoDeRed, pattern='^' + str(RED) + '$'),
                CallbackQueryHandler(tipoDePago, pattern = '^' + str(TIPO) + '$'),
                CallbackQueryHandler(comp, pattern='^' + str(COMP) + '$'),
                CallbackQueryHandler(links_esp, pattern='^' + str(LINK_ESP) + '$'),
                CallbackQueryHandler(links_ing, pattern='^' + str(LINK_ING) + '$'),
                CallbackQueryHandler(links_todo, pattern='^' + str(LINK_TODO) + '$'),                 
                CallbackQueryHandler(transaccion, pattern='^' + str(TRAN) + '$'),
                MessageHandler(Filters.text, main_handler),
                CallbackQueryHandler(start2, pattern='^' + str(START) + '$'),
                CallbackQueryHandler(verPlanesEspanol, pattern='^' + str(PLAN_ES) + '$'), 
                CallbackQueryHandler(verPlanesIngles, pattern='^' + str(PLAN_IN) + '$'),    
                CallbackQueryHandler(verPlanesTotal, pattern='^' + str(PLAN_TOTAL) + '$'),
                CallbackQueryHandler(a_la_carta, pattern='^' + str(ALA) + '$'), 
                CallbackQueryHandler(a_la_carta_ES, pattern='^' + str(ALA_ES) + '$'), 
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