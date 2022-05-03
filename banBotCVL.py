
from telegram.ext import Updater, CommandHandler
import pymongo
from datetime import datetime, timedelta
import time

updater = Updater('5397521781:AAEx4KnPvEbS8b9qKgIac1wxNXx5TRMfMt4')

## setup db
mongodb_key = "mongodb+srv://Xicano22:CiudadDelSolG20@cluster0.jt7sg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongodb_key)
db_name = "CVL"
collection_name = "CVLCol"
db = client[db_name][collection_name]

id_canales_copia_esp =      [-1001547496469, -1001709442538, -1001659852190, -1001663559207, -1001531100744, -1001659852190, -1001665404502, -1001758172813, -1001387678838, -1001162354519, -1001772371866, -1001724972314]
id_canales_copia_ing =      [-1001657550513, -1001750708220, -1001758730481, -1001616457923, -1001772377787, -1001627813158, -1001251261245, -1001632283508, -1001603430632, -1001638187563, -1001575574586, -1001770679920, -1001751711077, -1001530644292, -1001510193991, -1001592557882, -1001506072700, -1001797830280, -1001687280253, -1001735482090, -1001739439895, -1001637115099, -1001648519939, -1001505802921, -1001756517355, -1001724876054, -1001796272923, -1001778738386] #-1001637115099
canales_espejo_todos = id_canales_copia_esp + id_canales_copia_ing

def actualizarBD(usuario, name, date):
    dic_events = db.find_one({"id":usuario})["events"]
    dic_events.update({name:date})
    db.update_one({"id":usuario}, {"$set":{"events":dic_events}})

def callback_minute(context):
    id_list = {}
    error = False
    expulsado = False
    cursor = db.find({})
    print("Buscando si hay usuarios con fecha expirada...")
    for document in cursor:
        ident = document['id']
        print(ident)
        dic_events = db.find_one({"id":ident})["events"] 
        user_id = ident
        ahora = datetime.now()
        if int(user_id) > 5:
            try:
                fecha = dic_events['Fecha']
                expulsado = dic_events['Estatus']
                fecha_expirada = ahora - timedelta(days=999)
                name = 'Fecha'
                
                if fecha < ahora and expulsado == True:
                    print("Venció el plan")
                    for grupo in id_canales_copia_ing:
                        ahora = datetime.now()
                        try:
                            context.bot.ban_chat_member(
                                chat_id=grupo, 
                                user_id=user_id,
                                until_date =ahora + timedelta(minutes=3))      
                            print("Se expulsó al usuario")
                        except:
                            print("hubo un error echando al usuario")
                    for grupo in id_canales_copia_ing:
                        time.sleep(1)
                        try:
                            context.bot.unban_chat_member(
                                chat_id=grupo, 
                                user_id=user_id)      
                            print("Se desbaneó al usuario")
                        except:
                            print("hubo un error desbaneando al usuario")        
                            
                           
                    estatus = "Estatus"
                    estatus_mode = False
                    actualizarBD(ident, estatus, estatus_mode)   
                    actualizarBD(ident, name, fecha_expirada)
                else:
                    print("Este usuario tiene el plan activo")   
            except:
                pass
        else:
            print("No coincide con un ID de Telegram")
           
    #context.bot.send_message(chat_id='my_chat_id', text='One message every minute')

def set_timer(update,context):
    due= 43200 
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(callback_minute, due, context=chat_id, name=str(chat_id))

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", set_timer))
updater.start_polling()
updater.idle()