from pyrogram import *
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import json
import random
path = "/home/botwht/dav-syncer-compiti/"
path_botwht = "/usr/local/bin/BotWht/"

weekdays = ["lun", "mar", "mer", "gio", "ven", "sab"]

@Client.on_message(filters.command(['compiti']))
async def compiti(client, message):
    with open(path+"compiti.json", "r") as openfile:
        try:
            data = openfile.read()
            compiti = json.loads(data)
        except:
            print("UDDIO! Cannot load JSON file compiti.json")
            return
    compiti_richiesti = []
    date_current = datetime.now()
    if "dom" in message.text.lower() or len(message.command) == 1:
        date_current = date_current+timedelta(1)
        if "dopo" in message.text.lower():
            date_current = date_current + timedelta(1)
        date = date_current.strftime("%Y-%m-%d")
        giorno = date
        for compito in compiti:
            if compito[len(compito)-1] == date:
                compiti_richiesti.append(compito)
    elif "oggi" in message.text.lower():
        if "dopo" in message.text.lower():
            date_current = date_current + timedelta(1)
        date = date_current.strftime("%Y-%m-%d")
        giorno = date
        for compito in compiti:
            if compito[len(compito)-1] == date:
                compiti_richiesti.append(compito)
    elif "ieri" in message.text.lower():
        if "dopo" in message.text.lower():
            date_current = date_current + timedelta(1)
        date_current = date_current-timedelta(1)
        date = date_current.strftime("%Y-%m-%d")
        giorno = date
        for compito in compiti:
            if compito[len(compito)-1] == date:
                compiti_richiesti.append(compito)
    else:
        possible_dates = message.command[1:]
        text = message.text.lower()
        times = 0
        if "prossimo" in text:
            times += 1
        ind = 0
        today = date_current.weekday()
        for wkd in weekdays:
            if wkd in text: 
                for i in range(7):
                    if (date_current + timedelta(i+(7*times))).weekday() == ind:
                        possible_dates.append(datetime.strftime(date_current + timedelta(i+(7*times)), "%Y-%m-%d"))
                        date_current = (date_current + timedelta(i+(7*times)))
            ind += 1
        giorno = ""
        for d in message.command[1:]:
            giorno += d + " "
        for compito in compiti:
            for p_date in possible_dates:
                if p_date in compito[len(compito)-1] or compito[len(compito)-1] in p_date:
                    compiti_richiesti.append(compito)
                    date_current = datetime.strptime(p_date, "%Y-%m-%d")
    compiti_string = ""
    for compito in compiti_richiesti:
        for attributo in compito:
            if attributo == "NOTARI SILVIA":
                if random.randint(0,1):
                    attributo = "SOTARI NILVIA"
            elif attributo == "VICARI SALVATORE":
                if random.randint(0,1):
                    attributo = "SICARI VALVATORE"
            elif attributo == "ZOPPELLI BARBARA":
                if random.randint(0,1):
                    attributo = "BOPPELLI ZARBARA"
            if type(attributo) != int:
                compiti_string += str(attributo) + "\n"
        compiti_string += "\n\n"
    compiti_string = compiti_string[0:(len(compiti_string)-3)]
    giornoprima = (date_current - timedelta(1)).strftime("%Y-%m-%d")
    giornodopo = (date_current + timedelta(1)).strftime("%Y-%m-%d")
    if len(compiti_string):
        if "buttons=off" in message.command or "buttons:off" in message.command or "b-off" in message.command or "buttons-off" in message.command:
            await message.reply_text(compiti_string)
        else:
            send = await message.reply_text(compiti_string,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️",callback_data="compiti "+giornoprima),InlineKeyboardButton("➡️",callback_data="compiti "+giornodopo)]]))
    else:
        if "buttons=off" in message.command or "buttons:off" in message.command or "b-off" in message.command or "buttons-off" in message.command:
            await message.reply_text("Non ci sono compiti per il giorno " + str(giorno) + "!")
        else:
            await  message.reply_text("Non ci sono compiti per il giorno " + str(giorno) + "!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️",callback_data="compiti "+giornoprima),InlineKeyboardButton("➡️",callback_data="compiti "+giornodopo)]]))

@Client.on_callback_query(filters.regex("compiti"))
async def compi(client, callback_query):
    giorno = callback_query.data.split(" ")[1]
    with open(path+"compiti.json", "r") as openfile:
        try:
            data = openfile.read()
            compiti = json.loads(data)
        except:
            print("UDDIO! Cannot load JSON file compiti.json")
            return
    compiti_richiesti = []
    for compito in compiti:
        if giorno in compito[len(compito)-1] or compito[len(compito)-1] in giorno:
            compiti_richiesti.append(compito)
    compiti_string = ""
    for compito in compiti_richiesti:
        for attributo in compito:
            if attributo == "NOTARI SILVIA":
                if random.randint(0,1):
                    attributo = "SOTARI NILVIA"
            elif attributo == "VICARI SALVATORE":
                if random.randint(0,1):
                    attributo = "SICARI VALVATORE"
            elif attributo == "ZOPPELLI BARBARA":
                if random.randint(0,1):
                    attributo = "BOPPELLI ZARBARA"
            if type(attributo) != int:
                compiti_string += str(attributo) + "\n"
        compiti_string += "\n\n"
    compiti_string = compiti_string[0:(len(compiti_string)-3)]
    giornoprima = str(datetime.strptime(giorno,'%Y-%m-%d')-timedelta(days=1))[:10]
    giornodopo = str(datetime.strptime(giorno,'%Y-%m-%d')+timedelta(days=1))[:10]
    message=callback_query.message
    if len(compiti_string):
        send = await message.edit_text(compiti_string,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️",callback_data="compiti "+giornoprima),InlineKeyboardButton("➡️",callback_data="compiti "+giornodopo)]]))
    else:
        await  message.edit_text("Non ci sono compiti per il giorno " + str(giorno) + "!",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️",callback_data="compiti "+giornoprima),InlineKeyboardButton("➡️",callback_data="compiti "+giornodopo)]]))
