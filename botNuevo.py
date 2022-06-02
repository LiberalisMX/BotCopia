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
codigo_ala = False
eleccion_a_la_carta_bool = False
codigo_escrito = False
codigo_usuario = ""
fecha_temprana = 0
nombre_de_canales = [
    "Trading Latino",#1 
    "Gran Mago VIP",#2 
    "BitLobo", #3
    "InvestClub",#4 
    "Crypto Nova Premium Indicators",#5
    "Bruno Crypto",#6
    "Always Win VIP",#7 
    "Suho_Kun - FuturesMaxLeverage125x",#8 
    "Team Camilo VIP", #9
    "CTI BLACK Spot",#10
    "CTI BLACK Futuros",#11 
    "Rose Premium Signal 2022",#12 
    "Special Leverage Capital", #13
    "Ozel Clup 1.0", #14
    "Binance 360",#15
    "Crypto Future", #16
    "Maverick Trading", #17
    "Elon Trades", #18
    "Elliott Wave VIP",#19 
    "Bitcoin Bullets", #20
    "Walsh Wealth Discord",#21 
    "Krypton Wolf", #22
    "Fat Pig Signals", #23
    "Binance Killers", #24
    "FED Russian Insiders",#25 
    "Universal Crypto",#26
    #CT Leaks
    "Lady Market", #27
    "NinjaScalp",#28
    "Crypto Feras",#29 
    "TraderSZ", #30
    "Crypto Dude", #31
    "Trader_XO", #32
    "Crypto_Chase",#33
    #Herramientas 
    "Anuncios de Binance filtrados(3-5 minutos antes)", #34
    "Listados de CoinMarketCap filtrados (10-30min antes)",#35
    "Listados de CoinGecko filtrados (5-10min antes)" , #36
    #"Nuevos Listados de Coinbase",
    #"Nuevos Listados de Kucoin",
    ] 

nombre_de_canales_ing_html = [
    "<b>🤖Trading Latino</b> <i><a href='https://t.me/TradingLatinoInformacion'>Saber +</a></i>🔎",
    "<b>🤖Trading Latino Alertas</b> <i><a href='https://t.me/TradingLatinoAlertasInfo'>Saber +</a></i>🔎", 
    "<b>🤖Gran Mago VIP</b> <i><a href='https://t.me/GranMagoInfo'>Saber +</a></i>🔎",
    "<b>🤖BitLobo</b> <i><a href='https://t.me/BitLoboInfo'>Saber +</a></i>🔎", 
    "<b>🤖InvestClub</b> <i><a href='https://t.me/InvestClubInfo'>Saber +</a></i>🔎",
    "<b>🤖Crypto Tommey</b> <i><a href='https://t.me/+3rQ2k-uv66w0Mzdh'>Saber +</a></i>🔎", 
    "<b>🤖CryptoNova Premium</b> <i><a href='https://t.me/CryptoNovaInfo'>Saber +</a></i>🔎",
    "<b>🤖Bruno Crypto</b> <i><a href='https://t.me/BrunoCryptoInfo'>Saber +</a></i>🔎",
    "<b>🤖Always Win VIP</b> <i><a href='https://t.me/+ETvC93B1rBdlNmVh'>Saber +</a></i>🔎",
    "<b>🤖FuturesMaxLeverage125x</b> <i><a href='https://t.me/ozzyInfo'>Saber +</a></i>🔎",
    "<b>🤖TeamCamilo</b> <i><a href='https://t.me/TeamCamiloInfo'>Saber +</a></i>🔎", 
    "<b>🤖CTI BLACK Spot\n🤖CTI BLACK Futuros</b> <i><a href='https://t.me/CTIBlackInfo'>Saber +</a></i>🔎",
    "<b>🤖Rose Premium Signal 2022</b> <i><a href='https://t.me/+M7gRLkXTgQE2ODM5'>Saber +</a></i>🔎", 
    "<b>🤖Special Leverage Capital</b> <i><a href='https://t.me/ozzyInfo'>Saber +</a></i>🔎",
    "<b>🤖Ozel Clup 1.0</b> <i><a href='https://t.me/+WOXMSKqox6g1YzYx'>Saber +</a></i>🔎", 
    "<b>🤖Binance 360</b> <i><a href='https://t.me/+VmRX1TF9dCQ3MzQx'>Saber +</a></i>🔎", 
    "<b>🤖Crypto Future</b> <i><a href='https://t.me/+Jl8st7zvSeBhZjBh'>Saber +</a></i>🔎", 
    "<b>🤖Maverick Trading</b> <i><a href='https://t.me/MaverickTradingInfo'>Saber +</a></i>🔎",
    "<b>🤖Elon Trades</b> <i><a href='https://t.me/+-oc1qfrnsl85M2Zh'>Saber +</a></i>🔎", 
    "<b>🤖Elliott Wave VIP</b> <i><a href='https://t.me/+RZj_VjxNSoZlOTM5'>Saber +</a></i>🔎",
    "<b>🤖Bitcoin Bullets</b> <i><a href='https://t.me/+K3yey0-GRdxlMjIx'>Saber +</a></i>🔎", 
    "<b>🤖Walsh Wealth Discord</b> <i><a href='https://t.me/crearcanal'>Saber +</a></i>🔎", 
    "<b>🤖Krypton Wolf</b> <i><a href='https://t.me/+OQJKeH6iVNM3ZjRh'>Saber +</a></i>🔎", 
    "<b>🤖Fat Pig Signals</b> <i><a href='https://t.me/+dhHbAecrLnQxMzRh'>Saber +</a></i>🔎", 
    "<b>🤖Binance Killers</b> <i><a href='https://t.me/+H9IRck2X2vgzNGMx'>Saber +</a></i>🔎", 
    "<b>🤖FED Russian Insiders</b> <i><a href='https://t.me/+ZhZCS5ABjZQyYTMx'>Saber +</a></i>🔎", 
    "<b>🤖Universal Crypto</b> <i><a href='https://t.me/crearcanal'>Saber +</a></i>🔎",
    "\n<u>CT Leaks</u>\n",
    #CT Leaks
    "<b>🤖Lady Market</b> <i><a href='https://t.me/+JYZut02RqGA5ZmQx'>Saber +</a></i>🔎", 
    "<b>🤖NinjaScalp</b> <i><a href='https://t.me/+IIVqmmZOfIdjNTUx'>Saber +</a></i>🔎", 
    "<b>🤖CryptoFeras</b> <i><a href='https://t.me/+x2bds4pk8ZU4NjNh'>Saber +</a></i>🔎", 
    "<b>🤖TraderSZ</b> <i><a href='https://t.me/+85zpHRHWMB01ODk5'>Saber +</a></i>🔎", 
    "<b>🤖CryptoDude</b> <i><a href='https://t.me/+L91Og9qMB3w1MTFh'>Saber +</a></i>🔎",
    "<b>🤖Trader_XO</b> <i><a href='https://t.me/+HKyRXEQjKnJiYTE5'>Saber +</a></i>🔎", 
    "<b>🤖Crypto Chase</b> <i><a href='https://t.me/+L91Og9qMB3w1MTFh'>Saber +</a></i>🔎",
    "\n<u>Herramientas</u>\n",  
    #Herramientas
    "<b>🤖Anuncios de Binance filtrados(3-5 minutos antes)</b> <i><a href='https://t.me/+UfzkVt2Y99s4ZjAx'>Saber +</a></i>🔎", 
    "<b>🤖Listados de CoinMarketCap filtrados (10-30min antes)</b> <i><a href='https://t.me/+UfzkVt2Y99s4ZjAx'>Saber +</a></i>🔎", 
    "<b>🤖Listados de CoinGecko filtrados (5-10min antes)</b> <i><a href='https://t.me/+UfzkVt2Y99s4ZjAx'>Saber +</a></i>🔎", 
    #"Nuevos listados de Coinbase</b> <i><a href='https://t.me/crearcanal'>Saber +</a></i>🔎", 
    #"Nuevos Listados de Kucoin</b> <i><a href='https://t.me/crearcanal'>Saber +</a></i>🔎"
    ]
enlaces = [
    "https://t.me/+nEFX5E9q1NNjYmQ5", #1 Trading Latino
    "https://t.me/+hgRvxI4ZngxjZWUx", #38 Trading Latino Alertas 
    "https://t.me/+_fNQaHoqw103Njcx", #2 Gran Mago
    "https://t.me/+S1kVQB5ODk0yMDBh", #3 Bitlobo
    "https://t.me/+Ef8EqYqGdac1Yzcx", #4 Invest Club
    "https://t.me/+SlvJMtSLz9s0MDU5", #37 Crypto Tommey
    "https://t.me/+rGEW-Iy3lGE4NGMx", #5 Crypto Nova
    "https://t.me/+O5uRMmrYtL42MzQx", #6 Bruno Crypto
    "https://t.me/+92lYOtf7bTIyYmFh", #7 Always Win
    "https://t.me/+64bHxp0jdXllOTYx", #8 FuturesMaxLeverage
    "https://t.me/+9uJehlRnAK1iZjA5", #9 Team Camilo
    "https://t.me/+cc0tTISol9E4NDgx", #10 CTI Black Spot
    "https://t.me/+RiBsVADrieExYTk5", #11 CTI Black Futuros
    "https://t.me/+GqcpfJJWER5lM2Ex", #12 Rose Premium
    "https://t.me/+vPStihQ3VrEwMGQx", #13 Special Leverage Capital
    "https://t.me/+H83hZxrAJFEzZTBh", #14 Ozel clup 1.0
    "https://t.me/+Vcvqc0zRASwxNzEx", #15 Binance 360
    "https://t.me/+LbDNpY1D46BkZGQ5", #16 Crypto Future
    "https://t.me/+ZYJ8dJSknIA1YmYx", #17 Maverick
    "https://t.me/+5qgnXfXeodpmMWE5", #18 Elon Trades
    "https://t.me/+AAmqr55-nSRhZTVh", #19 Elliott Wave
    "https://t.me/+AcfJAsPWQpJhYzYx", #20 Bitcoin Bullets
    "https://t.me/+T7ENtbSHlvA4YWQx", #21 Walsh Wealth
    "https://t.me/+r3MAfqsVDB9lZTdh", #22 Krypton Wolf
    "https://t.me/+x3gwUDfHwj1hOTY5", #23 Fat Pig
    "https://t.me/+glw7R_snlLo4OTQx", #24 Binance Killers
    "https://t.me/+_l5Ry4UpacpiNzYx", #25 Russian Insiders
    "https://t.me/+2jZnaEC0zuRhMzRh", #26 Universal Crypto
    "https://t.me/+UcvT98QKqg85NzQx", #27 Lady Market
    "https://t.me/+wjMrtUL5LmFkMDc5", #28 NinjaScalp
    "https://t.me/+r_ixc8ebSGpmYzNh", #29 Cypto Feras
    "https://t.me/+xmt6u-VzCb4zMzIx", #30 Trader SZ
    "https://t.me/+LS9JeVK2Ym9iYmE5", #31 Crypto Dude
    "https://t.me/+eV77A3Slsd1iZGMx", #32 Trader_XO
    "https://t.me/+Utzd3man6OwxZGQx", #33 Crypto Chase
    "https://t.me/+0yPIFr91fnVmYmI5", #34 Binance Announcements
    "https://t.me/+ky36Z8gCIfI5Y2I5", #35 Coinmarketcap
    "https://t.me/+ukkrt1-Huzk1ZWYx", #36 Coingecko
    #"https://t.me/+SNVHEqGaSqljNTAx", #20 Haven Loma
    #"https://t.me/+3zxoqUrU844yYTJh", #23 AlexClayAlts
    #"https://t.me/+JIte7WjruXVjYzFh", #24 AlexClay Margin
    #"https://t.me/+v_cKapbuT9I3MjMx", #25 AlexClay Scalping
    #"https://t.me/+gU5l8OnzH4pkZmQx", #27 Birb Nest
    #"https://t.me/+6xxK1ENSDJEwNjNh", #29 Raticoin Alts
    ]

id_canales = [
-1001547496469, #1 Trading Latino
-1001691907243, # Trading Latino alertas
-1001709442538, #2 Gran Mago
-1001659852190, #3 BitLobo
-1001663559207, #4 Invest Club
-1001506072700, #37 Crypto Tommey
-1001531100744, #5 Crypto Nova Premiun Indicators
-1001665404502, #6 Bruno Crypto
-1001657550513, #7 Always Win
-1001724972314, #8 FuturesMaxLeverage125x
-1001162354519, #9 Team Camilo
-1001758172813, #10 CTI Black Spot
-1001387678838, #11 CTI Black Futuros
-1001735482090, #12 Rose Premium
-1001772371866, #13 Special Leverage Capital
-1001616457923, #14 Ozel Clup 1.0
-1001750708220, #15 Binance 360
-1001758730481, #16 CryptoFuture
-1001505802921, #17 Maverick
-1001510193991, #18 Elon Trades
-1001721176771, #19 Elliott Wave
-1001797830280, #20 Bitcoin Bullets
-1001756517355, #21 Walsh Wealth
-1001751711077, #22 Krypton Wolf
-1001739439895, #23 Fat Pigs
-1001637115099, #24 Binance Killers
-1001648519939, #25 Russian Insiders
-1001778738386, #26 Universal Crypto
-1001772377787, #27 Lady Market
-1001627813158, #28 NinjaScalp
-1001724876054, #29 Crypto Feras
-1001687280253, #30 TraderSZ
-1001796272923, #31 CryptoDude
-1001632283508, #32 Trader_XO
-1001603430632, #33 Crypto_chase
-1001441798693, #34 APILeakers - Binance
-1001795095388, #35 APILeakers - CoinMarketCap 
-1001766334668, #36 APILeakers - CoinGecko
]
links_info = [
    "https://t.me/TradingLatinoInformacion", #1 Trading Latino
    "https://t.me/TradingLatinoAlertasInfo", #31 Trading Latino Alertas
    "https://t.me/GranMagoInfo", #2 Gran Mago
    "https://t.me/BitLoboInfo", #3 BitLobo
    "https://t.me/InvestClubInfo", #4 Invest Club
    "https://t.me/+3rQ2k-uv66w0Mzdh", #30 Raticoin
    "https://t.me/CryptoNovaInfo", #5 CryptoNova
    "https://t.me/+5GyfVHubnLE0ZTQx", #14 Always Win
    "https://t.me/ozzyInfo", #11 FuturesMaxLeverage
    "https://t.me/TeamCamiloInfo",#9 Team Camilo
    "https://t.me/CryptoNovaInfo", #6 Bruno Crypto
    "https://t.me/CTIBlackInfo", #7 CTI BLACK Spot
    "https://t.me/CTIBlackInfo", #8 CTI BLACK Futuros
    "https://t.me/+6kCjNndwG8A5MGQx", #33 Rose
    "https://t.me/ozzyInfo", #12 Scpecial Leverage
    "https://t.me/+ciguQXRbGw0wMjIx", #17 Ozel Clup
    "https://t.me/+9EtTG5pPkcc3OTlh", #15 Binance 360
    "https://t.me/+Jl8st7zvSeBhZjBh", #16 CryptoFuture
    "https://t.me/MaverickTradingInfo", #10 Maverick
    "https://t.me/+5MjzpwgnL9JmYjEx", #28 ElonTrades
    "https://t.me/+RZj_VjxNSoZlOTM5", #13 Elliott Wave 
    "https://t.me/+bj2Sgo7gguo1N2Mx", #31 Bitcoin Bullets
    "https://t.me/+z6f8pEFrtYg5MWMx", #40 Walsh Wealth
    "https://t.me/+wjniEYxVsFo0YjEx", #26 Krypton Wolf
    "https://t.me/+cnBLcfLat1RhYzcx", #34 Fat Pig
    "https://t.me/+6F_4ue0Kp-E5Y2Ix", #35 Binance Killers
    "https://t.me/+-o7BNRxKETBlYWUx", #36 FED Russian Insiders
    "https://t.me/+u2K_zCYfc1ljNDFh", #43 Universal Crypto        
    "https://t.me/+Ro_Ugnj_AjtjZGIx", #18 Lady Market
    "https://t.me/+UnwS2MVlcyozOGYx", #19 NinjaScalp
    "https://t.me/+JdUJIxua1P0yNDc5", #41 Crypto Feras
    "https://t.me/+eDChQRux2-JjYTlh", #32 Trader Sz
    "https://t.me/+5sQ79XUgCE04Zjgx", #42 Cryptodude
    "https://t.me/+UnwS2MVlcyozOGYx", #20 Trader_XO
    "https://t.me/+UnwS2MVlcyozOGYx", #21 Crypto_chase
    "https://t.me/+UfzkVt2Y99s4ZjAx", #37 API Leakers
    "https://t.me/+UfzkVt2Y99s4ZjAx", #38 API Leakers
    "https://t.me/+UfzkVt2Y99s4ZjAx", #39 API Leakers
    
    
    #"https://t.me/+UnwS2MVlcyozOGYx", #22 HAVEN
    #"https://t.me/+VqIEXbx84twxOTZh", #23 Alex Clay
    #"https://t.me/+VqIEXbx84twxOTZh", #24 Alex Clay
    #"https://t.me/+VqIEXbx84twxOTZh", #25 Alex Clay
    #"https://t.me/+lyTr5IHrsYdmY2Vh", #27 Birb Nest Info
    #"https://t.me/+3rQ2k-uv66w0Mzdh", #29 Raticoin

] 
API_KEY = "00db512a379e25fc7ed3b3ae6338733fcf156edb81c48af1d51aa56305c95b9f"
API_SECRET = "543318F264b2374bF484d2193fd8237C5c1B6ac201e343957A23CBAF10D4983C"
IPN_SECRET = "http://laguiadigital.mx/coinpayments.php"
# Estados
PRIMERO, SEGUNDO = range(2)
# Callback data
ACTIVARPRUEBA, RED, COMP, TRAN, END, START, PACKS, PLAN_TOTAL, COD, COD_COMP, SABER, ALA, ALA_EN, PLAN_ALA, LINKS, LINK_ALA, TIPO, PAY, UN_MES, DOS_MESES, TRES_MESES, COIN1, COIN2, COIN3, USDT, BUSD, TRAN_CRYPTO = range(27)

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

#función inicial cuando el usuario le da a "iniciar"
def start(update: Update, context: CallbackContext) -> int:
    global name, user, nuevo_usuario
    global usuario, chat_id, plan_a_la
    plan_a_la = False
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
        db.find_one({"id":usuario})["events"]
        print("Se encontró al usuario " + name + " en la base de datos")
        nuevo_usuario = False
    except:
        dic_event = "User_id"
        instertarBD(usuario, dic_event, name)
        print("No se encontró al ususario y se ha registrado la nueva entrada")
        nuevo_usuario = True

    keyboard = [
        [InlineKeyboardButton("🎁 PRUEBA GRATUITA 🎁", callback_data=str(ACTIVARPRUEBA))],
        [InlineKeyboardButton("⚜ Contratar un plan ⚜", callback_data=str(PACKS))],
        [InlineKeyboardButton("Código de acceso 🔑", callback_data=str(COD))],
        [InlineKeyboardButton("Saber más ❔", callback_data=str(SABER))]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Enviar mensaje de text junto con el teclado
    user = update.message.from_user
    context.bot.send_photo(chat_id, "https://imgur.com/a/UbPkNHP")
    if nuevo_usuario == True:
        texto = "Hola " + user.first_name + '! Bienvenido a HispanLeaks ⚜\n\nSomos una cooperativa de amigos y apasionados de las criptomonedas que un día nos juntamos para compartir los grupos VIP de los que éramos miembros, rápidamente vimos el potencial:\n\n<i>"Disfrutar de los mejores grupos VIP sin tener que pagar miles de dólares"</i>.\n\nCon esta idea nació HispanLeaks ⚜ y esa es la esencia que mantenemos, y por eso <u>hemos conseguido tener los mejores canales VIP del mundo, sin diferencias, al instante y por un precio ultra reducido!</u>\n\n<b><i>✅OFERTA HASTA QUE OFICIALEMENTE ACABE EL BEARMARKET🐻 ✅</i>\n\n🎁 Puedes activar tu prueba gratuita de 7 días para TODOS los canales sin compromiso.🎁\n\n\n\nPrecio pack TODOS los canales:\n1 MES      - $8 <s>   $12</s> (-35% OFF)\n2 MESES - $14 <s> $20</s> (-30% OFF)\n3 MESES - $20 <s> $29</s> (-30% OFF)\n\nPrecio canales a la carta:\n1 MES      - $5  <s>  $8</s>    (-35% OFF)\n2 MESES - $9  <s>  $14</s>  (-35% OFF)\n3 MESES - $13 <s> $18</s>  (-35% OFF)</b>\n\n\n<u>Canales en el Servicio:</u>\n\n🤖Trading Latino Canal VIP 🇪🇸\n🤖Trading Latino Alertas 🇪🇸\n🤖Gran Mago 🇪🇸\n🤖InvestClub 🇪🇸\n🤖BitLobo 🇪🇸\n🤖Crypto Tommey 🇪🇸\n🤖CryptoNova 🇪🇸\n🤖Bruno Crypto 🇪🇸\n🤖Always Win 🇺🇸\n🤖Suho_Kun - FuturesMaxLeverage125x 🇺🇸\n🤖Team Camilo VIP 🇪🇸\n🤖CTI BLACK Spot 🇪🇸\n🤖CTI BLACK Futuros 🇪🇸\n🤖Team Camilo 🇪🇸\n🤖Rose Premium Signals 🇺🇸\n🤖Special Leverage Capital 🇺🇸\n🤖Ozel Clup 1.0 🇺🇸\n🤖Binance 360 🇺🇸\n🤖Crypto Future 🇺🇸\n🤖Maverick Trding 🇪🇸\n🤖ElonTrades VIP 🇺🇸\n🤖Elliott Wave VIP 🇪🇸\n🤖Bitcoin Bullets 🇺🇸\n🤖Whalsh Wealth 🇺🇸\n🤖Krypton Wolf 🇺🇸\n🤖Fat Pig Signals 🇺🇸\n🤖Binance Killers 🇺🇸\n🤖FED Russian Insiders 🇺🇸\n\n<i>CT Leaks:</i>\n\n🤖Universal Crypto 🇺🇸\n🤖Lady Market 🇪🇸\n🤖NinjaScalp 🇺🇸\n🤖Crypto Feras 🇺🇸\n🤖Trader SZ 🇺🇸\n🤖Crypto Dude 🇺🇸\n🤖Trader_XO 🇺🇸\n🤖Crypto_Chase 🇺🇸\n\n<i>Herramientas: </i>\n\n🤖Anuncios de Binance filtrados (3-5 minutos antes) 🇺🇸\n🤖Listados de CoinMarketCap filtrados (10-30min antes) 🇺🇸\n🤖Listados de CoinGecko filtrados (5-10min antes) 🇺🇸\n🤖Libros y Cursos 🇪🇸🇺🇸📚\n🤖Canal de Noticias 🇪🇸🌐'
    if nuevo_usuario == False:
        texto = "Hola " + user.first_name + '!\n\n🎁 Si tu prueba ha finalizado por favor elige un paquete.👍\n\n<b><i>✅OFERTA HASTA QUE OFICIALEMENTE ACABE EL BEARMARKET🐻 ✅</i>\n\nPrecio pack TODOS los canales:\n1 MES      - $8 <s>   $12</s> (-35% OFF)\n2 MESES - $14 <s> $20</s> (-30% OFF)\n3 MESES - $20 <s> $29</s> (-30% OFF)\n\nPrecio canales a la carta:\n1 MES      - $5  <s>  $8</s>    (-35% OFF)\n2 MESES - $9  <s>  $14</s>  (-35% OFF)\n3 MESES - $13 <s> $18</s>  (-35% OFF)</b>\n\n\n<u>Canales en el Servicio:</u>\n\n🤖Trading Latino Canal VIP 🇪🇸\n🤖Trading Latino Alertas 🇪🇸\n🤖Gran Mago 🇪🇸\n🤖InvestClub 🇪🇸\n🤖BitLobo 🇪🇸\n🤖Crypto Tommey 🇪🇸\n🤖CryptoNova 🇪🇸\n🤖Bruno Crypto 🇪🇸\n🤖Always Win 🇺🇸\n🤖Suho_Kun - FuturesMaxLeverage125x 🇺🇸\n🤖Team Camilo VIP 🇪🇸\n🤖CTI BLACK Spot 🇪🇸\n🤖CTI BLACK Futuros 🇪🇸\n🤖Team Camilo 🇪🇸\n🤖Rose Premium Signals 🇺🇸\n🤖Special Leverage Capital 🇺🇸\n🤖Ozel Clup 1.0 🇺🇸\n🤖Binance 360 🇺🇸\n🤖Crypto Future 🇺🇸\n🤖Maverick Trding 🇪🇸\n🤖ElonTrades VIP 🇺🇸\n🤖Elliott Wave VIP 🇪🇸\n🤖Bitcoin Bullets 🇺🇸\n🤖Whalsh Wealth 🇺🇸\n🤖Krypton Wolf 🇺🇸\n🤖Fat Pig Signals 🇺🇸\n🤖Binance Killers 🇺🇸\n🤖FED Russian Insiders 🇺🇸\n\n<i>CT Leaks:</i>\n\n🤖Universal Crypto 🇺🇸\n🤖Lady Market 🇪🇸\n🤖NinjaScalp 🇺🇸\n🤖Crypto Feras 🇺🇸\n🤖Trader SZ 🇺🇸\n🤖Crypto Dude 🇺🇸\n🤖Trader_XO 🇺🇸\n🤖Crypto_Chase 🇺🇸\n\n<i>Herramientas: </i>\n\n🤖Anuncios de Binance filtrados (3-5 minutos antes) 🇺🇸\n🤖Listados de CoinMarketCap filtrados (10-30min antes) 🇺🇸\n🤖Listados de CoinGecko filtrados (5-10min antes) 🇺🇸\n🤖Libros y Cursos 🇪🇸🇺🇸📚\n🤖Canal de Noticias 🇪🇸🌐'
    
    update.message.reply_text(texto, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return PRIMERO 

def start2(update: Update, context: CallbackContext) -> int:
    global plan_a_la
    plan_a_la = False
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("🎁 PRUEBA GRATUITA 🎁", callback_data=str(ACTIVARPRUEBA))],
        [InlineKeyboardButton("⚜ Contratar un plan ⚜", callback_data=str(PACKS))],
        [InlineKeyboardButton("Código de acceso 🔑", callback_data=str(COD))],
        [InlineKeyboardButton("Saber más ❔", callback_data=str(SABER))]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Enviar mensaje de text junto con el teclado
    if nuevo_usuario == True:
        texto = "Hola " + user.first_name + '! Bienvenido a HispanLeaks ⚜\n\nSomos una cooperativa de amigos y apasionados de las criptomonedas que un día nos juntamos para compartir los grupos VIP de los que éramos miembros, rápidamente vimos el potencial:\n\n<i>"Disfrutar de los mejores grupos VIP sin tener que pagar miles de dólares"</i>.\n\nCon esta idea nació HispanLeaks ⚜ y esa es la esencia que mantenemos, y por eso <u>hemos conseguido tener los mejores canales VIP del mundo, sin diferencias, al instante y por un precio ultra reducido!</u>\n\n<b><i>✅OFERTA HASTA QUE OFICIALEMENTE ACABE EL BEARMARKET🐻 ✅</i>\n\n🎁 Puedes activar tu prueba gratuita de 7 días para TODOS los canales sin compromiso.🎁\n\n\n\nPrecio pack TODOS los canales:\n1 MES      - $8 <s>   $12</s> (-35% OFF)\n2 MESES - $14 <s> $20</s> (-30% OFF)\n3 MESES - $20 <s> $29</s> (-30% OFF)\n\nPrecio canales a la carta:\n1 MES      - $5  <s>  $8</s>    (-35% OFF)\n2 MESES - $9  <s>  $14</s>  (-35% OFF)\n3 MESES - $13 <s> $18</s>  (-35% OFF)</b>\n\n\n<u>Canales en el Servicio:</u>\n\n🤖Trading Latino Canal VIP 🇪🇸\n🤖Trading Latino Alertas 🇪🇸\n🤖Gran Mago 🇪🇸\n🤖InvestClub 🇪🇸\n🤖BitLobo 🇪🇸\n🤖Crypto Tommey 🇪🇸\n🤖CryptoNova 🇪🇸\n🤖Bruno Crypto 🇪🇸\n🤖Always Win 🇺🇸\n🤖Suho_Kun - FuturesMaxLeverage125x 🇺🇸\n🤖Team Camilo VIP 🇪🇸\n🤖CTI BLACK Spot 🇪🇸\n🤖CTI BLACK Futuros 🇪🇸\n🤖Team Camilo 🇪🇸\n🤖Rose Premium Signals 🇺🇸\n🤖Special Leverage Capital 🇺🇸\n🤖Ozel Clup 1.0 🇺🇸\n🤖Binance 360 🇺🇸\n🤖Crypto Future 🇺🇸\n🤖Maverick Trding 🇪🇸\n🤖ElonTrades VIP 🇺🇸\n🤖Elliott Wave VIP 🇪🇸\n🤖Bitcoin Bullets 🇺🇸\n🤖Whalsh Wealth 🇺🇸\n🤖Krypton Wolf 🇺🇸\n🤖Fat Pig Signals 🇺🇸\n🤖Binance Killers 🇺🇸\n🤖FED Russian Insiders 🇺🇸\n\n<i>CT Leaks:</i>\n\n🤖Universal Crypto 🇺🇸\n🤖Lady Market 🇪🇸\n🤖NinjaScalp 🇺🇸\n🤖Crypto Feras 🇺🇸\n🤖Trader SZ 🇺🇸\n🤖Crypto Dude 🇺🇸\n🤖Trader_XO 🇺🇸\n🤖Crypto_Chase 🇺🇸\n\n<i>Herramientas: </i>\n\n🤖Anuncios de Binance filtrados (3-5 minutos antes) 🇺🇸\n🤖Listados de CoinMarketCap filtrados (10-30min antes) 🇺🇸\n🤖Listados de CoinGecko filtrados (5-10min antes) 🇺🇸\n🤖Libros y Cursos 🇪🇸🇺🇸📚\n🤖Canal de Noticias 🇪🇸🌐'
    if nuevo_usuario == False:
        texto = "Hola " + user.first_name + '!\n\n🎁 Si tu prueba ha finalizado por favor elige un paquete.👍\n\n<b><i>✅OFERTA HASTA QUE OFICIALEMENTE ACABE EL BEARMARKET🐻 ✅</i>\n\nPrecio pack TODOS los canales:\n1 MES      - $8 <s>   $12</s> (-35% OFF)\n2 MESES - $14 <s> $20</s> (-30% OFF)\n3 MESES - $20 <s> $29</s> (-30% OFF)\n\nPrecio canales a la carta:\n1 MES      - $5  <s>  $8</s>    (-35% OFF)\n2 MESES - $9  <s>  $14</s>  (-35% OFF)\n3 MESES - $13 <s> $18</s>  (-35% OFF)</b>\n\n\n<u>Canales en el Servicio:</u>\n\n🤖Trading Latino Canal VIP 🇪🇸\n🤖Trading Latino Alertas 🇪🇸\n🤖Gran Mago 🇪🇸\n🤖InvestClub 🇪🇸\n🤖BitLobo 🇪🇸\n🤖Crypto Tommey 🇪🇸\n🤖CryptoNova 🇪🇸\n🤖Bruno Crypto 🇪🇸\n🤖Always Win 🇺🇸\n🤖Suho_Kun - FuturesMaxLeverage125x 🇺🇸\n🤖Team Camilo VIP 🇪🇸\n🤖CTI BLACK Spot 🇪🇸\n🤖CTI BLACK Futuros 🇪🇸\n🤖Team Camilo 🇪🇸\n🤖Rose Premium Signals 🇺🇸\n🤖Special Leverage Capital 🇺🇸\n🤖Ozel Clup 1.0 🇺🇸\n🤖Binance 360 🇺🇸\n🤖Crypto Future 🇺🇸\n🤖Maverick Trding 🇪🇸\n🤖ElonTrades VIP 🇺🇸\n🤖Elliott Wave VIP 🇪🇸\n🤖Bitcoin Bullets 🇺🇸\n🤖Whalsh Wealth 🇺🇸\n🤖Krypton Wolf 🇺🇸\n🤖Fat Pig Signals 🇺🇸\n🤖Binance Killers 🇺🇸\n🤖FED Russian Insiders 🇺🇸\n\n<i>CT Leaks:</i>\n\n🤖Universal Crypto 🇺🇸\n🤖Lady Market 🇪🇸\n🤖NinjaScalp 🇺🇸\n🤖Crypto Feras 🇺🇸\n🤖Trader SZ 🇺🇸\n🤖Crypto Dude 🇺🇸\n🤖Trader_XO 🇺🇸\n🤖Crypto_Chase 🇺🇸\n\n<i>Herramientas: </i>\n\n🤖Anuncios de Binance filtrados (3-5 minutos antes) 🇺🇸\n🤖Listados de CoinMarketCap filtrados (10-30min antes) 🇺🇸\n🤖Listados de CoinGecko filtrados (5-10min antes) 🇺🇸\n🤖Libros y Cursos 🇪🇸🇺🇸📚\n🤖Canal de Noticias 🇪🇸🌐'
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
            [InlineKeyboardButton(text="Comprobar validéz 🎟", callback_data=str(COD_COMP))],
            [InlineKeyboardButton(text="Volver ↩️", callback_data=str(COD))]
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
    cod2 = "Ticket 8dls"
    cod4 = "Ticket 14dls"
    cod6 = "Ticket 20dls"
    ala1 = "A la 5dls"
    ala2 = "A la 9dls"
    ala3 = "A la 13dls"   

    if codigo_usuario == "":
        keyboard = [
                [InlineKeyboardButton(text="Comprobar validéz 🎟", callback_data=str(COD_COMP))],
                [InlineKeyboardButton(text="Volver ↩️", callback_data=str(COD))]
                ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_comprobar)
        query.edit_message_text(
            text="¡Vaya!, parece que no has envíado ningún código ❗\n\n<b>Asegurate de <u>PRIMERO envíar el mensaje</u> y luego dale a 'Comprobar validéz'</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML
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
                [InlineKeyboardButton(text="Ver Links ➡️", callback_data=str(LINKS))]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)            
            query.edit_message_text(
                text="¡El Código de acceso es correcto! ✅\n\nSuscripción válida por 30 días", reply_markup=reply_markup)
        elif codigo_usuario in alas1:
            nom = ala1 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}})
            keyboard = [
                [InlineKeyboardButton(text="Entrar a los canales ➡️", callback_data=str(ALA_EN))],
                ] 
            codigo_ala = True    
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 30 días.", reply_markup=reply_markup)
       
    elif codigo_usuario in cods4 or codigo_usuario in alas2:
                
        print("Enviando links de acceso")
        ##Aqui se envían el/los links
        actualizarBD(usuario, "Plan", 2) 
   
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
                [InlineKeyboardButton(text="Mostrar links ➡️", callback_data=str(LINKS))]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)            
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 60 días.", reply_markup=reply_markup)
        elif codigo_usuario in alas2:
            nom = ala2 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="Canales a la carta ➡️", callback_data=str(ALA_EN))],
                ] 
            codigo_ala = True    
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 60 días.", reply_markup=reply_markup)
      
    elif codigo_usuario in cods6 or codigo_usuario in alas3:
        
        print("Enviando links de acceso")
        ##Aqui se envían el/los links
        actualizarBD(usuario, "Plan", 2) 
                        
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
                [InlineKeyboardButton(text="Entrar a los canales ➡️", callback_data=str(LINKS))]
                ]
            reply_markup = InlineKeyboardMarkup(keyboard)            
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 90 días.", reply_markup=reply_markup)
        elif codigo_usuario in alas3:
            nom = ala3 +"." + codigo_usuario 
            db.update_many({"id":1}, { '$unset' : {nom:""}}) 
            keyboard = [
                [InlineKeyboardButton(text="Canales a la carta ➡️", callback_data=str(ALA_EN))],
                ] 
            codigo_ala = True    
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="El Código de acceso es correcto! ✅\n\nSuscripción válida por 90 días.", reply_markup=reply_markup)
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
    global eleccion, eleccionRed_bool, plan_todo, texto_canales_ing, un_mes, dos_meses, tres_meses
    query = update.callback_query
    eleccionRed_bool, plan_todo, un_mes, dos_meses, tres_meses = False, False, False, False, False

    query.answer()
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=mensaje_id_elecciones)  
    except:
        pass 
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_continuar) 
    except:
        pass        
    eleccion = []

    
    keyboard = [
        [InlineKeyboardButton(text="Todos los canales (Desde $8)", callback_data=str(PLAN_TOTAL))],
        [InlineKeyboardButton(text="Canales a la carta (Desde $5)", callback_data=str(ALA))],
        [InlineKeyboardButton(text="Volver ↩️", callback_data=str(START))]]
    reply_markup = InlineKeyboardMarkup(keyboard) 

    canales_lista_ing = []

    for canal_ing in nombre_de_canales_ing_html:
        canales_ing = canal_ing+ "\n"
        canales_lista_ing.append(canales_ing)
    texto_canales_ing = "".join(canales_lista_ing)
    
    query.edit_message_text(
        text="<u>Canales en el pack:</u>\n\n" + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    
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
        [InlineKeyboardButton(text="Ver canales a la carta", callback_data=str(ALA_EN))],
        [InlineKeyboardButton(text="Volver ↩️", callback_data=str(PACKS))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Si sólo estás interesado en un canal tu mejor opción es<b> Canales a la carta</b>📋", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
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
            text="<u><b>Canales a la carta</b></u>\n\nPrecio: <b>SÓLO $5/mes</b>\nCanales:\n\n" + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        reply_keyboard = []
    if codigo_ala == True:

                
        keyboard = [[
                InlineKeyboardButton("Back ↩️", callback_data=str(ALA)),
                InlineKeyboardButton("Continue ➡️", callback_data =str(LINK_ALA))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="<u><b>Canales a la carta</b></u>\n\nPrecio: <b>SÓLO $5/mes</b>\nCanales:\n\n" + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        reply_keyboard = []
            
    for canal in nombre_de_canales:
        lista_canal = []
        lista_canal.append(canal)
        reply_keyboard.append(lista_canal)
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="NO ESCRIBIR", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="Después de elegir el canal dale a continuar👆", reply_markup=reply_markup2)    
    mensaje_id_elecciones = mensaje.message_id 
    return SEGUNDO 

#sección donde se muestran los planes disponibles
def verPlanes(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones, eleccionCantidad_bool, plan_todo
    query = update.callback_query
    query.answer()
    keyboard = [
            [InlineKeyboardButton("1 mes de membresía, $8.00/1 mes", callback_data=str(UN_MES))],
            [InlineKeyboardButton("2 meses de membresía, $14.00/2 meses", callback_data=str(DOS_MESES))],
            [InlineKeyboardButton("3 meses de membresía, $20.00/3 meses", callback_data=str(TRES_MESES))],
            [InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="<u><b>Plan con todos los canales</b></u>\n\nPrecio: <b>SÓLO $8/mes</b>\nCanales en el plan:\n\n" + texto_canales_ing, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    eleccionCantidad_bool = True
    plan_todo = True
    return SEGUNDO
def formaDePago1mes(update: Update, context: CallbackContext) -> int:
    global un_mes, coin_un_mes, coin_dos_meses, coin_tres_meses
    query = update.callback_query
    query.answer()
    keyboard = [
            [InlineKeyboardButton("Transferencia crypto a billetera Binance", callback_data=str(TRAN_CRYPTO))],
            [InlineKeyboardButton("BinancePay", callback_data=str(PAY))],
            [InlineKeyboardButton("CoinPayments", callback_data=str(COIN1))],
            [InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="<u><b>Has elegido 1 mes de membresía.\nCosto: $8</b></u>\n\n<b>Elige el método de pago de tu preferencia</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    coin_un_mes = False
    coin_dos_meses = False
    coin_tres_meses = False
    un_mes = True
    return SEGUNDO
def formaDePago2meses(update: Update, context: CallbackContext) -> int:
    global dos_meses, coin_un_mes, coin_dos_meses, coin_tres_meses
    query = update.callback_query
    query.answer()
    keyboard = [
            [InlineKeyboardButton("Transferencia crypto a billetera Binance", callback_data=str(TRAN_CRYPTO))],
            [InlineKeyboardButton("BinancePay", callback_data=str(PAY))],
            [InlineKeyboardButton("CoinPayments", callback_data=str(COIN1))],
            [InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="<u><b>Has elegido 2 meses de membresía.\nCosto: $14</b></u>\n\n<b>Elige el método de pago de tu preferencia</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    coin_un_mes = False
    coin_dos_meses = False
    coin_tres_meses = False
    dos_meses = True
    return SEGUNDO
def formaDePago3meses(update: Update, context: CallbackContext) -> int:
    global tres_meses, coin_un_mes, coin_dos_meses, coin_tres_meses
    query = update.callback_query
    query.answer()
    keyboard = [
            [InlineKeyboardButton("Transferencia crypto a billetera Binance", callback_data=str(TRAN_CRYPTO))],
            [InlineKeyboardButton("BinancePay", callback_data=str(PAY))],
            [InlineKeyboardButton("CoinPayments", callback_data=str(COIN1))],
            [InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="<u><b>Has elegido 3 meses de membresía.\nCosto: $20</b></u>\n\n<b>Elige el método de pago de tu preferencia</b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    tres_meses = True
    coin_un_mes = False
    coin_dos_meses = False
    coin_tres_meses = False
    return SEGUNDO 
def coinPaymnets1mes(update: Update, context: CallbackContext) -> int:
    global coin_un_mes, usdt, busd, coin_un_mes, coin_dos_meses, coin_tres_meses
    query = update.callback_query
    query.answer()
    keyboard = [
            [InlineKeyboardButton("USDT.TRC20 (Red de TronTRX)", callback_data=str(USDT))],        
            [InlineKeyboardButton("BUSD.BEP20 (Red Binance Smart Chain)", callback_data=str(BUSD))],
            [InlineKeyboardButton("Volver ↩️", callback_data=str(UN_MES))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text= "<b>Elige el tipo de red con el que deseas pagar entre las opciones disponibles.\n\n</b>Elige con cuidado por que las transacciones en una red equivocada no se pueden revertir.\n\n<i>Si deseas pagar con otro tipo de red dale a volver y elige el método de pago 'Transferencia crypto a billetera de Binance' <b>aceptamos todas las redes disponibles en Binance</b></i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    busd = False
    usdt = False    
    coin_un_mes = True
    coin_dos_meses = False
    coin_tres_meses = False    
    return SEGUNDO                         
def coinPaymnets2meses(update: Update, context: CallbackContext) -> int:
    global coin_dos_meses, usdt, busd, coin_un_mes, coin_tres_meses
    query = update.callback_query
    query.answer()
    keyboard = [
            [InlineKeyboardButton("USDT.TRC20 (Red de TronTRX)", callback_data=str(USDT))],        
            [InlineKeyboardButton("BUSD.BEP20 (Red Binance Smart Chain)", callback_data=str(BUSD))],
            [InlineKeyboardButton("Volver ↩️", callback_data=str(UN_MES))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
         text= "<b>Elige el tipo de red con el que deseas pagar entre las opciones disponibles.\n\n</b>Elige con cuidado por que las transacciones en una red equivocada no se pueden revertir.\n\n<i>Si deseas pagar con otro tipo de red dale a volver y elige el método de pago 'Transferencia crypto a billetera de Binance' <b>aceptamos todas las redes disponibles en Binance</b></i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    busd = False
    usdt = False  
    coin_un_mes = False  
    coin_tres_meses = False    
    coin_dos_meses = True
    return SEGUNDO                         
def coinPaymnets3meses(update: Update, context: CallbackContext) -> int:
    global coin_tres_meses, usdt, busd, coin_un_mes, coin_dos_meses
    query = update.callback_query
    query.answer()
    keyboard = [[
            InlineKeyboardButton("USDT.TRC20 (Red de TronTRX)", callback_data=str(USDT)),           
            InlineKeyboardButton("BUSD.BEP20 (Red Binance Smart Chain)", callback_data=str(BUSD)),
            InlineKeyboardButton("Volver ↩️", callback_data=str(TRES_MESES))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
         text= "<b>Elige el tipo de red con el que deseas pagar entre las opciones disponibles.\n\n</b>Elige con cuidado por que las transacciones en una red equivocada no se pueden revertir.\n\n<i>Si deseas pagar con otro tipo de red dale a volver y elige el método de pago 'Transferencia crypto a billetera de Binance' <b>aceptamos todas las redes disponibles en Binance</b></i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    busd = False
    usdt = False
    coin_dos_meses = False
    coin_un_mes = False
    coin_tres_meses = True
    return SEGUNDO                         
def redUSDT(update: Update, context: CallbackContext) -> int:
    global usdt
    query = update.callback_query
    query.answer()
    keyboard = [[
            InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Continuar ✅", callback_data=str(TRAN))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if coin_un_mes:
        query.edit_message_text(
            text= "<b>Has elegido:\n\nSuscripción: 1 MES\nMétodo: Coinpayments\nRed: USDT.TRC20</b>\n\nSi la información es correcta, por favor dale a continuar ✅.", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    if coin_dos_meses:
        query.edit_message_text(
            text= "<b>Has elegido:\n\nSuscripción: 2 MESES\nMétodo: Coinpayments\nRed: USDT.TRC20</b>\n\nSi la información es correcta, por favor dale a continuar ✅.", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    
    if coin_tres_meses:
        query.edit_message_text(
            text= "<b>Has elegido:\n\nSuscripción: 3 MESES\nMétodo: Coinpayments\nRed: USDT.TRC20</b>\n\nSi la información es correcta, por favor dale a continuar ✅.", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        
    usdt = True
    return SEGUNDO                   
def redBUSD(update: Update, context: CallbackContext) -> int:
    global busd
    query = update.callback_query
    query.answer()
    keyboard = [[
            InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS)),
            InlineKeyboardButton("Continuar ✅", callback_data=str(TRAN))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if coin_un_mes:
        query.edit_message_text(
            text= "<b>Has elegido:\n\nSuscripción: 1 MES\nMétodo: Coinpayments\nRed: BUSD.BEP20</b>\n\nSi la información es correcta, por favor dale a continuar ✅.", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

    if coin_dos_meses:
        query.edit_message_text(
            text= "<b>Has elegido:\n\nSuscripción: 2 MESES\nMétodo: Coinpayments\nRed: BUSD.BEP20</b>\n\nSi la información es correcta, por favor dale a continuar ✅.", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    
    if coin_tres_meses:
        query.edit_message_text(
            text= "<b>Has elegido:\n\nSuscripción: 3 MESES\nMétodo: Coinpayments\nRed: BUSD.BEP20</b>\n\nSi la información es correcta, por favor dale a continuar ✅.", reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        
    busd = True
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
        text="Elegiste el canal "+eleccion_a_la_carta[0]+"\n\nDespués de elegir la duración del plan dale a continuar", reply_markup=reply_markup)
    reply_keyboard = [['1 mes de membresía, $5.00/1 mes'], ['2 meses de membresía, $9.00/2 meses'], ['3 meses de membresía, $13.00/3 meses']]
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
            [InlineKeyboardButton("CoinPayments", callback_data=str(RED))],
            [InlineKeyboardButton("BinancePay (Sin comisiones)", callback_data =str(PAY))],
            [InlineKeyboardButton("Back ↩️", callback_data=str(PACKS))]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        if "1 mes" in eleccion[0]:
            query.edit_message_text(
                text="<b><u>Elige el método de Pago:</u>\n\nCoinPayments</b>\nEl pago por CoinPayments es gestionado autmomáticamente por la plataforma.\n\Comisiones: $1 aprox.\n\n⚠️ <i>Algunos exchanges como Binance no permiten transferencias menores a $10 por lo que te recomendamos contratar un paquete de 2 meses, utilizar Binance Pay como fomra de pago o elegir otro exchange como Kucoin que no tenga monto mínimo de transferencia.</i>\n\n<b>Binance Pay</b>\nLos pagos por Binance Pay son SIN COMISIONES.\n⚠️<i> La comprobación del pago se hace de manera MANUAL, por lo qué puede demorar desde unos minutos hasta unas horas (*según disponiblidad horaria del administrador).</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        else:
            print("Se activo el except")
            query.edit_message_text(
                "<b><u>Elige el método de Pago:</u>\n\nCoinPayments</b>\nEl pago por CoinPayments es gestionado autmomáticamente por la plataforma.\n\Comisiones: $1 aprox.\n\n⚠️ <i>Algunos exchanges como Binance no permiten transferencias menores a $10 por lo que te recomendamos contratar un paquete de 2 meses, utilizar Binance Pay como fomra de pago o elegir otro exchange como Kucoin que no tenga monto mínimo de transferencia.</i>\n\n<b>Binance Pay</b>\nLos pagos por Binance Pay son SIN COMISIONES.\n⚠️<i> La comprobación del pago se hace de manera MANUAL, por lo qué puede demorar desde unos minutos hasta unas horas (*según disponiblidad horaria del administrador).</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
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
    reply_keyboard = [['⚡ USDT.BEP20 - Theter USD (BEP20 / BSC)'], ['⚡ USDT.TRC20 - Theter USD (TRC20 / Tron Chain)']]
    reply_markup2 = ReplyKeyboardMarkup(reply_keyboard, input_field_placeholder="NO ESCRIBIR", one_time_keyboard=True)
    mensaje = context.bot.send_message(chat_id =chat_id, text="Elige la red que prefieras, presiona continuar y espera aque se genere tu órden.", reply_markup=reply_markup2)
    mensaje_id_elecciones = mensaje.message_id
    return PRIMERO
  
def BinancePay(update: Update, context: CallbackContext) -> int:
    global mensaje_id_elecciones
    query = update.callback_query
    query.answer()
    try:
        if "1 mes de membresía," in eleccion[0]:
            if plan_todo == True:
                mensaje = context.bot.send_photo(chat_id, photo="https://imgur.com/a/pVSzmtI", caption="<b><u>Costo del paquete: $8\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)

            elif plan_a_la == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://imgur.com/a/pVSzmtI", caption="<b><u>Costo del canal: $5\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)

        if "2 meses de membresía" in eleccion[0]:
            if plan_todo == True:
                mensaje = context.bot.send_photo(chat_id, photo="https://imgur.com/a/pVSzmtI", caption="<b><u>Costo del paquete por 2 meses: $14\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)

            elif plan_a_la == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://imgur.com/a/pVSzmtI", caption="<b><u>Costo del canal por 2 meses: $7\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)

        if "3 meses de membresía" in eleccion[0]:
            if plan_todo == True:
                mensaje = context.bot.send_photo(chat_id, photo="https://imgur.com/a/pVSzmtI", caption="<b><u>Costo del paquete por 3 meses: $18\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
            elif plan_a_la == True:
                mensaje =  context.bot.send_photo(chat_id, photo="https://imgur.com/a/pVSzmtI", caption="<b><u>Costo del canal por 3 meses: $10\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
    except:
        #context.bot.send_message(chat_id, text="Hubo un error eligiendo el valor del paquete, por favor reinicia el bot eligiendo el precio del paquete que deseas.\n\nSi sigues experimentando problemas por favor contacta al admin @HispanLeaksAdmin y lo resolveremos a la brevedad posible.")
        pass
    try:
        if un_mes:
            mensaje = context.bot.send_photo(chat_id, photo="https://imgur.com/a/pVSzmtI", caption="<b><u>Costo del paquete: $7\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
        elif dos_meses:
            mensaje = context.bot.send_photo(chat_id, photo="https://imgur.com/a/pVSzmtI", caption="<b><u>Costo del paquete por 2 meses: $13\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
        elif tres_meses:
            mensaje = context.bot.send_photo(chat_id, photo="https://imgur.com/a/pVSzmtI", caption="<b><u>Costo del paquete por 3 meses: $18\n\nInstrucciones:</u></b>\n\n1.-Descarga la imagen a tu galería para poder acceder a ella desde la app de Binance.\n\n2.-Escanea la imagen con la app de Binance y envía los fondos.\n\n3.-Ház una captura de pantalla y envíala por chat a @HispanLeaksAdmin\n\n4.-Espera a que el administrador haga la comprobación de tu pago y te devolverá un código.\n\n5.-Vuelve a iniciar este bot con el comando /start e introduce el código de acceso que te dio el administrador en el botón\n'🔑 Código de acceso'.\n\n<i>Si tienes dudas de como hacer el pago por Binance Pay hemos hecho una guía detalla. <a href='https://t.me/+H80QNFwyiCFjNTMx'>Ver guía detallada</a></i>", parse_mode=ParseMode.HTML)
    except:
        print("Hubo un error")
    mensaje_id_elecciones = mensaje.message_id
    return ConversationHandler.END

def transaccion(update: Update, context: CallbackContext) -> int:
    global plan, eleccionRed_bool
    query = update.callback_query
    query.answer()
    eleccionRed_bool = False
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_continuar)
    except:
        pass    
    nombre = usuario
    try:
        if "1 mes de membresía" in eleccion[0]:
            if plan_a_la:
                plan, cantidad = 1, 5
        if "2 meses de membresía" in eleccion[0]:
            if plan_a_la:
                plan, cantidad = 2, 9
        if "3 meses de membresía" in eleccion[0]:
            if plan_a_la:
                plan, cantidad = 3, 13
    except:
        pass
    try:
        if "USDT.BEP20" in eleccion[1]:
            moneda = "USDT.BEP20"
        if "USDT.TRC20" in eleccion[1]:
            moneda = "USDT.TRC20"
    except:
        pass    

    try:
        if un_mes and plan_todo:
            plan, cantidad = 1, 8
        if dos_meses and plan_todo:
            plan, cantidad = 2, 14
        if tres_meses and plan_todo:
            plan, cantidad = 3, 20
    except:
        pass 

    try:
        if usdt:
            moneda = "USDT.TRC20"    
        if busd:
            moneda = "BUSD.BEP20"
    except:
        pass        



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
        text="Pago por CoinPayments\n\n<b>Dirección de la billetera:</b>\n<code>" + address + "</code>\n\n<b>Cantidad a envíar:</b>\n$" + str(amount) + " (" + moneda + ")\n\n⚠️La plataforma Coinpayments solo dará por arpobada la transacción cuando se cubra el monto TOTAL del pago\n❗️El enlace de pago caduca en 1 día\n\nSi tienes algún problema con el pago contacta a @HispanLeaksAdmin, te atenderemos lo antes posible.\n\n<a href='"+link+"'>Comprueba el estado de la transacción en Coinpayments.net</a>", parse_mode=ParseMode.HTML)

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
                text="<b>Se ha detectado la transacción, esperando 10 confirmaciones. Vuelve a probar tras unos minutos.</b>\n\nSi tienes algún problema con la transacción contacta a @HispanLeaksAdmin, te atenderemos lo antes posible.\n\n<a href='"+link+"'>Mira el estatus de la transacción en Coinpayments</a>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except:
            query.edit_message_text(
                text="No se ha recibido ningún pago.\n\nSi tienes algun problema con la transacción contacta a @HispanLeaksAdmin, te atenderemos lo antes posible.", reply_markup=reply_markup)


    if status == 100:
        remove(str(chat_id), context)   
        if plan == 1: 
            actualizarBD(usuario, nombre, plan) 
            dias = 30 
            if plan_todo == True:
                keyboard = [[
                    InlineKeyboardButton("Entrat a los canales 🔗", callback_data=str(LINKS))]]

            if eleccion_a_la_carta_bool == True:
                keyboard = [[
                    InlineKeyboardButton("Entrat a los canales 🔗", callback_data=str(LINK_ALA))]]                        

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


        if plan == 2:
            actualizarBD(usuario, nombre, plan) 
            dias = 60   

            if plan_todo == True:
                keyboard = [[
                    InlineKeyboardButton("Entrat a los canales 🔗", callback_data=str(LINKS))]]
   
            if eleccion_a_la_carta_bool == True:
                keyboard = [[
                    InlineKeyboardButton("Entrat a los canales 🔗", callback_data=str(LINK_ALA))]]   

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

        if plan == 3:
            actualizarBD(usuario, nombre, plan) 
            dias = 90           
            if plan_todo == True:
                keyboard = [[
                    InlineKeyboardButton("Entrat a los canales 🔗", callback_data=str(LINKS))]]

            if eleccion_a_la_carta_bool == True:
                keyboard = [[
                    InlineKeyboardButton("Entrat a los canales 🔗", callback_data=str(LINK_ALA))]]               
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="<b>¡Pago recibido!✅.\n<i>Tu membresía está activa por 3 meses 🎉</i></b>\n\nPresiona el botón <i>'Ver links🔗'</i> sólo una vez y espera a que carguen los enlaces.\n\n⚠️<i>Si te unes a los canales VIP demasiado rápido Telegram bloqueará temporalmente la función, en ese caso solo debes esperar unos minutos y volver a intentarlo</i>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
            ahora = datetime.now()
            fecha_plan = ahora + timedelta(days=dias)
            dic_event = "Fecha"
            actualizarBD(usuario, dic_event, fecha_plan) 
            estatus = "Estatus"
            estatus_mode = True
            actualizarBD(usuario, estatus, estatus_mode)        

    return PRIMERO
#función para activar la prueba gratuita
def activarPrueba(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    text = "<b>🤖Trading Latino</b> <i><a href='https://t.me/+nEFX5E9q1NNjYmQ5'>Unirme al canal</a></i>⚜️\n\
<b>🤖Trading Latino Alertas</b> <i><a href='https://t.me/+hgRvxI4ZngxjZWUx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Gran Mago VIP</b> <i><a href='https://t.me/+_fNQaHoqw103Njcx'>Unirme al canal</a></i>⚜️\n\
<b>🤖BitLobo</b> <i><a href='https://t.me/+S1kVQB5ODk0yMDBh'>Unirme al canal</a></i>⚜️\n\
<b>🤖InvestClub</b> <i><a href='https://t.me/+Ef8EqYqGdac1Yzcx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Crypto Tommey</b> <i><a href='https://t.me/+SlvJMtSLz9s0MDU5'>Unirme al canal</a></i>⚜️\n\
<b>🤖CryptoNova Premium</b> <i><a href='https://t.me/+rGEW-Iy3lGE4NGMx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Bruno Crypto</b> <i><a href='https://t.me/+O5uRMmrYtL42MzQx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Always Win VIP</b> <i><a href='https://t.me/+92lYOtf7bTIyYmFh'>Unirme al canal</a></i>⚜️\n\
<b>🤖FuturesMaxLeverage125x</b> <i><a href='https://t.me/+64bHxp0jdXllOTYx'>Unirme al canal</a></i>⚜️\n\
<b>🤖TeamCamilo</b> <i><a href='https://t.me/+9uJehlRnAK1iZjA5'>Unirme al canal</a></i>⚜️\n\
<b>🤖CTI BLACK Spot</b> <i><a href='https://t.me/+cc0tTISol9E4NDgx'>Unirme al canal</a></i>⚜️\n\
<b>🤖CTI BLACK Futuros</b> <i><a href='https://t.me/+RiBsVADrieExYTk5'>Unirme al canal</a></i>⚜️\n\
<b>🤖Rose Premium Signal 2022</b> <i><a href='https://t.me/+GqcpfJJWER5lM2Ex'>Unirme al canal</a></i>⚜️\n\
<b>🤖Special Leverage Capital</b> <i><a href='https://t.me/+vPStihQ3VrEwMGQx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Ozel Clup 1.0</b> <i><a href='https://t.me/+H83hZxrAJFEzZTBh'>Unirme al canal</a></i>⚜️\n\
<b>🤖Binance 360</b> <i><a href='https://t.me/+Vcvqc0zRASwxNzEx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Crypto Future</b> <i><a href='https://t.me/+LbDNpY1D46BkZGQ5'>Unirme al canal</a></i>⚜️\n\
<b>🤖Maverick Trading</b> <i><a href='https://t.me/+ZYJ8dJSknIA1YmYx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Elon Trades</b> <i><a href='https://t.me/+5qgnXfXeodpmMWE5'>Unirme al canal</a></i>⚜️\n\
<b>🤖Elliott Wave VIP</b> <i><a href='https://t.me/+AAmqr55-nSRhZTVh'>Unirme al canal</a></i>⚜️\n\
<b>🤖Bitcoin Bullets</b> <i><a href='https://t.me/+AcfJAsPWQpJhYzYx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Walsh Wealth Discord</b> <i><a href='https://t.me/+T7ENtbSHlvA4YWQx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Krypton Wolf</b> <i><a href='https://t.me/+r3MAfqsVDB9lZTdh'>Unirme al canal</a></i>⚜️\n\
<b>🤖Fat Pig Signals</b> <i><a href='https://t.me/+x3gwUDfHwj1hOTY5'>Unirme al canal</a></i>⚜️\n\
<b>🤖Binance Killers</b> <i><a href='https://t.me/+glw7R_snlLo4OTQx'>Unirme al canal</a></i>⚜️\n\
<b>🤖FED Russian Insiders</b> <i><a href='https://t.me/+_l5Ry4UpacpiNzYx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Universal Crypto</b> <i><a href='https://t.me/+2jZnaEC0zuRhMzRh'>Unirme al canal</a></i>⚜️\n\
\n<u>CT Leaks</u>\n\
<b>🤖Lady Market</b> <i><a href='https://t.me/+UcvT98QKqg85NzQx'>Unirme al canal</a></i>⚜️\n\
<b>🤖NinjaScalp</b> <i><a href='https://t.me/+wjMrtUL5LmFkMDc5'>Unirme al canal</a></i>⚜️\n\
<b>🤖CryptoFeras</b> <i><a href='https://t.me/+r_ixc8ebSGpmYzNh'>Unirme al canal</a></i>⚜️\n\
<b>🤖TraderSZ</b> <i><a href='https://t.me/+xmt6u-VzCb4zMzIx'>Unirme al canal</a></i>⚜️\n\
<b>🤖CryptoDude</b> <i><a href='https://t.me/+LS9JeVK2Ym9iYmE5'>Unirme al canal</a></i>⚜️\n\
<b>🤖Trader_XO</b> <i><a href='https://t.me/+eV77A3Slsd1iZGMx'>Unirme al canal</a></i>⚜️\n\
<b>🤖Crypto Chase</b> <i><a href='https://t.me/+Utzd3man6OwxZGQx'>Unirme al canal</a></i>⚜️\n\
\n<u>Herramientas</u>\n\
<b>🤖Anuncios de Binance filtrados(3-5 minutos antes)</b> <i><a href='https://t.me/+0yPIFr91fnVmYmI5'>Unirme al canal</a></i>⚜️\n\
<b>🤖Listados de CoinMarketCap filtrados (10-30min antes)</b> <i><a href='https://t.me/+ky36Z8gCIfI5Y2I5'>Unirme al canal</a></i>⚜️\n\
<b>🤖Listados de CoinGecko filtrados (5-10min antes)</b> <i><a href='https://t.me/+ukkrt1-Huzk1ZWYx'>Unirme al canal</a></i>⚜️\n"
    #Buscar en la BD si el usuario ya utilizó la prueba y si es que si mira la fecha para comprobar su vencimiento
    try:
        date_ahora = datetime.now()
        fecha = db.find_one({"id":usuario})["events"]["Fecha"]
        print("Se encontró la fecha en la base de datos, comprobando dia de vencimiento")
        if fecha  < date_ahora:
            keyboard = [
                        [InlineKeyboardButton("⚜ Contratar un plan ⚜", callback_data=str(PACKS))]
                        ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text="Tu prueba gratuita terminó ⌛\n\nContrata un plan para seguir en los canales", reply_markup=reply_markup)
        else:
            keyboard = [[InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="<b>Tu prueba no vence todavía ⏳</b>\n\n" + text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    except:
        date_ahora = datetime.now()
        #Establecer cantidad de tiempo de prueba
        dias = 7

        print("No se encontró fecha en la base de datos, activando prueba gratuita ")
        fecha_de_vencimiento = timedelta(days=dias)
        fecha = date_ahora + fecha_de_vencimiento
        dic_event = "Fecha"
        actualizarBD(usuario, dic_event, fecha)
        estatus = "Estatus"
        estatus_mode = True
        actualizarBD(usuario, estatus, estatus_mode)
        keyboard = [[
            InlineKeyboardButton("Volver ↩️", callback_data=str(START))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text="🎉 <b>¡Felicidades! tu prueba de <u>10 días con acceso a todos los canales</u> ha sido activada!</b> 🎁\n\n" + text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    return SEGUNDO

def email(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton(text="1 month subscription, $10.00/1 month", callback_data=str(RED))],
        [InlineKeyboardButton(text="3 month subscription, $30.00/3 month", callback_data=str(RED))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Introduce tu email si quieres que se incluya en la transacción:", reply_markup=reply_markup)
    return SEGUNDO 
def trans_crypto(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Enviar comprobante al Admin 📩", url="t.me/HispanLeaksAdmin")],
                [InlineKeyboardButton("Elegir otro método de pago 🔄", callback_data=str(PACKS))],
                [InlineKeyboardButton("Volver ↩️", callback_data=str(PACKS))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="<b>Para realizar una transacción crypto envía los fondos a cualquiera de las billeteras disponibles:</b>\n\n<u>⚡️USDT TRC20 - Red de TRON:</u>\n<code>TKif4Htsz5UBGcfzF3hz5Vwc8azSzzmfCP</code>\n\n<u>⚡️USDT BEP20 - Red Binance Smart Chain:</u>\n<code>0x028c662fdf7f3c1b4b743a15d007712b5227f39e</code>\n\n<u>⚡️BUSD BEP20 - Red Binance Smart Chain:</u>\n<code>0x028c662fdf7f3c1b4b743a15d007712b5227f39e</code>\n\n<u>⚡️BTC Red de Bitcoin:</u>\n<code>1FN8dsq243yzFjsddBoz9MdMYfGodVBtYr</code>\n\n<u>⚡️BTC Red Binance Smart Chain:</u>\n<code>0x028c662fdf7f3c1b4b743a15d007712b5227f39e</code>\n\n<u>⚡️LTC Red de Litecoin:</u>\n<code>Lb9aoTJvWJ6yMan9WTNaqdvfXvdHA49ut2</code>\n\n<u>⚡️XRP red de Ripple:</u>\n<code>rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh</code>\nMemo: <code>421723936</code>\n\n\n<b><i>Una vez realizado el pago envía el comprobante al Administrador para que te brinde acceso.(t.me/HispanLeaksAdmin).</i></b>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return SEGUNDO
def help(update: Update, context: CallbackContext) -> int:

    context.bot.send_message(chat_id, text="Para reiniciar el bot sólo escribe o presiona en -> /start <-\n\nSi el fallo no se soluciona reiniciando, por favor contacta con el administrador @HispanLeaksAdmin")
    return ConversationHandler.END


def links_todo(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    for i in range(len(enlaces)):
        keyboard = [
            [InlineKeyboardButton(text="⚜ Únete al canal VIP ⚜", url=enlaces[i]),
            InlineKeyboardButton(text="Saber más de este trader 🔎", url=links_info[i])],
            ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text=nombre_de_canales[i], reply_markup=reply_markup)
    keyboard = [
        [InlineKeyboardButton("⚜ Contratar un plan", callback_data=str(PACKS))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.message.reply_text(text="⏰ Te informaremos cuando esté por vencer tu membresía. ⚠️ <b>Los links son válidos para un sólo uso y estarán activos por 3 días</b>\n\n<u><i>ℹ️Si tienes algún problema, duda, sugerencia, quieres colaborar en el sistema de referidos o si bien pagas por uno o varios canales Premium y quieres ser socio, comunícate con nosotros a través del único contacto oficial @HispanLeaksAdmin, te responderemos lo antes posible🙂ℹ️</i></u>", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return SEGUNDO

def links_a_la_carta(update: Update, context: CallbackContext) -> int:
    global eleccion_a_la_carta_bool, codigo_ala, eleccion_a_la_carta, mensaje_unirse_id
    query = update.callback_query
    query.answer()
    eng_or_esp = ""
    print(eleccion_a_la_carta[0])
    enlace = "Hubo un error, contacte al administrador"
  
    num_canal_eng = 0
    for canal in nombre_de_canales:
        if canal == eleccion_a_la_carta[0]:
            eng_or_esp = "ENG"
            break
        num_canal_eng +=1

    if eng_or_esp == "ENG":

        try:
            canales_contratados = "Canales"
            ids_canales = []
            ids_canales.append(id_canales[num_canal_eng])
            actualizarBD(usuario, canales_contratados, ids_canales)
        except:
            db.insert_one({"id":usuario, "events":{"Canales":ids_canales}}) 

        enlace = enlaces[num_canal_eng]
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
    mensaje_unirse = query.message.reply_text(text="Puedes unirte al canal "+ eleccion_a_la_carta[0] +" con el botón de abajo👇. Para reactivar el bot usa el comando /start", reply_markup=reply_markup)
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
    if '1 mes de membresía' in input_usuario or '2 meses de membresía' in input_usuario or '3 meses de membresía' in input_usuario or input_usuario == '⚡ USDT.BEP20 - Theter USD (BEP20 / BSC)' or input_usuario == '⚡ USDT.TRC20 - Theter USD (TRC20 / Tron Chain)':
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
        try:
            context.bot.delete_message(chat_id=chat_id, message_id=id_mensaje_continuar)  
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
    updater = Updater("5239051961:AAGc9Yo9LT4x8sgaC5ydLtzFemQCDiQQaBc")
    j = updater.job_queue
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

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
                CallbackQueryHandler(links_todo, pattern='^' + str(LINKS) + '$'),                                
            ],
            SEGUNDO: [
                CommandHandler('help', help),
                CallbackQueryHandler(paquetes, pattern='^' + str(PACKS) + '$'),
                CallbackQueryHandler(tipoDeRed, pattern='^' + str(RED) + '$'),
                CallbackQueryHandler(tipoDePago, pattern = '^' + str(TIPO) + '$'),
                CallbackQueryHandler(comp, pattern='^' + str(COMP) + '$'),
                CallbackQueryHandler(links_todo, pattern='^' + str(LINKS) + '$'),                 
                CallbackQueryHandler(transaccion, pattern='^' + str(TRAN) + '$'),
                MessageHandler(Filters.text, main_handler),
                CallbackQueryHandler(start2, pattern='^' + str(START) + '$'), 
                CallbackQueryHandler(verPlanes, pattern='^' + str(PLAN_TOTAL) + '$'),    
                CallbackQueryHandler(a_la_carta, pattern='^' + str(ALA) + '$'), 
                CallbackQueryHandler(a_la_carta_EN, pattern='^' + str(ALA_EN) + '$'),
                CallbackQueryHandler(verPlanes_a_la_carta, pattern='^' + str(PLAN_ALA) + '$'), 
                CallbackQueryHandler(links_a_la_carta, pattern='^' + str(LINK_ALA) + '$'),
                CallbackQueryHandler(formaDePago1mes, pattern='^' + str(UN_MES) + '$'),
                CallbackQueryHandler(formaDePago2meses, pattern='^' + str(DOS_MESES) + '$'), 
                CallbackQueryHandler(formaDePago3meses, pattern='^' + str(TRES_MESES) + '$'),
                CallbackQueryHandler(coinPaymnets1mes, pattern='^' + str(COIN1) + '$'),
                CallbackQueryHandler(coinPaymnets2meses, pattern='^' + str(COIN2) + '$'), 
                CallbackQueryHandler(coinPaymnets3meses, pattern='^' + str(COIN3) + '$'), 
                CallbackQueryHandler(redUSDT, pattern='^' + str(USDT) + '$'), 
                CallbackQueryHandler(redBUSD, pattern='^' + str(BUSD) + '$'),
                CallbackQueryHandler(BinancePay, pattern = '^' + str(PAY) + '$'), 
                CallbackQueryHandler(trans_crypto, pattern = '^' + str(TRAN_CRYPTO) + '$'),                    

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