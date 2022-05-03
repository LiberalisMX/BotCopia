
from pyrogram import Client, filters
import time
import pymongo
from datetime import datetime, timedelta

#configuracion telegram
phone_number ='525610830260'
api_id = '3705733'
api_hash = 'a7d61b5602ca8e692b93d408b894d306'
## setup db
mongodb_key = "mongodb+srv://Xicano22:CiudadDelSolG20@cluster0.jt7sg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
db_name = "CVL"
collection_name = "CVLCol"
client = pymongo.MongoClient(mongodb_key)
db = client[db_name][collection_name]
link_canales_esp = [
    "https://t.me/TradingLatinoInformacion", #1 Trading Latino
    "https://t.me/GranMagoInfo", #2 Gran Mago
    "https://t.me/BitLoboInfo", #3 BitLobo
    "https://t.me/InvestClubInfo", #4 Invest Club
    "https://t.me/CryptoNovaInfo", #5 CryptoNova
    "https://t.me/CryptoNovaInfo", #6 CryptoNova
    "https://t.me/CTIBlackInfo", #7 CTI BLACK
    "https://t.me/CTIBlackInfo", #8 CTI BLACK
    "https://t.me/TeamCamiloInfo",#9 Team Camilo
    "https://t.me/MaverickTradingInfo", #10 Maverick
    "https://t.me/ozzyInfo", #11 OZZY VIP
    "https://t.me/ozzyInfo", #12 OZZY VIP

]

link_canales_ing =[
    "https://t.me/AlwaysWinInfo", #1 Always Win
    "https://t.me/TheBullInfo", #2 The Bull
    "https://t.me/KimCryptoInfo", #3 KimCrypto
    "https://t.me/InnerCircleInfo", #4 Inner Circle
    "https://t.me/KillMexInfo", #5 KillMex
    "https://t.me/TheHavenInfo", #6 HAVEN
    "https://t.me/TheHavenInfo", #7 HAVEN
    "https://t.me/TheHavenInfo", #8 HAVEN
    "https://t.me/TheHavenInfo", #9 HAVEN
    "https://t.me/AlexClayInfo", #10 Alex Clay
    "https://t.me/AlexClayInfo", #11 Alex Clay
    "https://t.me/AlexClayInfo", #12 Alex Clay
    "https://t.me/KryptonWolfInfo", #13 Krypton Wolf
    "https://t.me/BirbNestInfo", #14 Birb Nest Info
    "https://t.me/ElonTradesInfo_esp",#15 ElonTrades
    "https://t.me/raticoinInfo_esp", #16 Raticoin
    "https://t.me/raticoinInfo_esp", #17 Raticoin
    "https://t.me/BitcoinBulletsInfo", #18 Bitcoin Bullets
    "https://t.me/MarginWhalesInfo", #19 Margin Whales
    "https://t.me/RosePremiumSignalsInfo", #20 Rose
    "https://t.me/FatPigSignalsInfo", #21 Fat Pig
    "https://t.me/BinanceKillersInfo", #22 Binance Killers
    "https://t.me/FedRussianInsidersInfo", #23 FED Russian Insiders
    "https://t.me/APILeakersInfo", #24 API Leakers
    "https://t.me/APILeakersInfo", #25 API Leakers
    "https://t.me/APILeakersInfo", #26 API Leakers
    "https://t.me/", #27 Walsh Wealth
    "https://t.me/", #28 Credible Crypto
    "https://t.me/", #29 Heisenberg Signals
    "https://t.me/", #30 Universal Crypto
]

id_canales_esp = [
    -1001547496469, #1 Trading Latino
    -1001709442538, #2 Gran Mago
    -1001659852190, #3 BitLobo
    -1001663559207, #4 Invest Club
    -1001531100744, #5 Crypto Nova Premiun Indicators
    -1001665404502, #6 Crypto Nova Challenge
    -1001758172813, #7 CTI Black Spot
    -1001387678838, #8 CTI Black Futuros
    -1001162354519, #9 Team Camilo
    -1001505802921,  #10 Maverick
    -1001772371866, #11 Ozzy Spot
    -1001724972314, #12 Ozzy Futuros
    #-1001441798693, #13 APILeakers - Binance
    #-1001766334668, #14 APILeakers - CoinGecko
    #-1001252203928, #15 APILeakers - CoinMarketCap
    ]

id_canales_ing = [
    -1001657550513, #1 Always Win
    -1001750708220, #2 The Bull
    -1001758730481, #3 KIM Crypto
    -1001616457923, #4 Inner Circle
    -1001772377787, #5 Kilmex
    -1001627813158, #6 Haven CBS
    -1001251261245, #7 Haven Loma
    -1001632283508, #8 Haven Krillin
    -1001603430632, #9 Haven Pierre
    -1001638187563, #10 Alex Clay Alts
    -1001575574586, #11 Alex Clay margin
    -1001770679920, #12 Alex Clay Scalping
    -1001751711077, #13 Krypton Wolf
    -1001530644292, #14 Birb Nest
    -1001510193991, #15 Elon Trades
    -1001592557882, #16 Raticoin Alts
    -1001506072700, #17 Raticoin Margin
    -1001797830280, #18 Bitcoin Bullets
    -1001687280253, #19 Margin Whales
    -1001735482090, #20 Rose Premium
    -1001739439895, #21 Fat Pigs
    -1001637115099, #22 Binance Killers
    -1001648519939,  #23 Russian Insiders
    -1001441798693, #24 APILeakers - Binance
    -1001766334668, #25 APILeakers - CoinGecko
    -1001795095388, #26 APILeakers - CoinMarketCap 
    -1001756517355, #27 Walsh Wealth
    -1001724876054, #28 Credible Crypto
    -1001796272923, #29 Heisenberg Signals
    -1001778738386 #30 Universal Crypto
    ]

#Iniciar cliente de pyrogram
with Client ("Pablo", api_id, api_hash) as app:
    #función para generar links de invitación
    def expires(segundos):
        return int(time.time()+segundos)
    def generate_esp():
        fecha_expiracion = expires(259200)
        grupos_esp = []
        #Itera entre los canales y genera un link por cada uno
        for link in id_canales_esp:
            grupo1 = app.create_chat_invite_link(link, member_limit=1, expire_date=fecha_expiracion)
            link1 = str(grupo1["invite_link"])
            grupos_esp.append(link1)
        return grupos_esp

    def generate_ing():
        grupos_ing = []
        fecha_expiracion = expires(259200)    
        #Itera entre los canales y genera un link por cada uno
        for link in id_canales_ing:
            grupo1 = app.create_chat_invite_link(link, member_limit=1, expire_date=fecha_expiracion)
            link1 = str(grupo1["invite_link"])
            grupos_ing.append(link1)
        return grupos_ing

             

    links_generados_esp = generate_esp() 
    id_links, nombre_links = 0, "link_grupos_esp"
    #intenta enviar los datos a la BD si no existe la entrada la crea
    try:
        dic_events = db.find_one({"id":id_links})["events"]
        dic_events.update({nombre_links:links_generados_esp})
        db.update_one({"id":id_links}, {"$set":{"events":dic_events}})
    except:
        db.insert_one({"id":id_links, "events":{nombre_links:links_generados_esp}})     

    links_generados_ing = generate_ing() 
    id_links, nombre_links = 0, "link_grupos_ing"

    #intenta enviar los datos a la BD si no existe la entrada la crea
    try:
        dic_events = db.find_one({"id":id_links})["events"]
        dic_events.update({nombre_links:links_generados_ing})
        db.update_one({"id":id_links}, {"$set":{"events":dic_events}})
    except:
        db.insert_one({"id":id_links, "events":{nombre_links:links_generados_ing}})  

##### Usar cuando haya que incluir un nuevo grupo en la BD de los canales info
    try:
        dic_events = db.find_one({"id":id_links})["events"]
        dic_events.update({"links_info_ing":link_canales_ing})
        db.update_one({"id":id_links}, {"$set":{"events":dic_events}})
    except:
        db.insert_one({"id":id_links, "events":{"links_info_ing":link_canales_ing}}) 
    
    try:
        dic_events = db.find_one({"id":id_links})["events"]
        dic_events.update({"links_info_esp":link_canales_esp})
        db.update_one({"id":id_links}, {"$set":{"events":dic_events}})
    except:
        db.insert_one({"id":id_links, "events":{"links_info_esp":link_canales_esp}}) 