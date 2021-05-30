#!/usr/bin/python3 -u

import json
from pyrogram import *
from pyromod import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler

path_compiti = "/home/botwht/dav-syncer-compiti/"
path_warning = "/home/botwht/dav-syncer-comunicati/"
path_botwht = "/usr/local/bin/BotWht/"
path_voti = "/home/botwht/dav-syncer-voti/"
token = ""

async def warning():
    with open(path_compiti+"warning.json", "r") as openfile:
        try:
            data = openfile.read()
            warning_arr = json.loads(data)
        except Exception as e:
            print("UDDIO!\n" + str(e))
            return
    with open(path_warning+"warning_comunicati.json", "r") as openfile:
        try:
            data = openfile.read()
            warning_arr_comunicati = json.loads(data)
        except Exception as e:
            print("UDDIO!\n" + str(e))
            return
    with open(path_voti+"warning.json", "r") as openfile:
        try:
            data = openfile.read()
            warning_arr_voti = json.loads(data)
        except Exception as e:
            print("UDDIO!\n" + str(e))
            return

    global app
    if len(warning_arr)>0:
        for warn in warning_arr:
            contenuto = ""
            vecchio_contenuto = ""
            if not warn[len(warn)-1]:
                vecchio_contenuto += str(warn[2][2]) + "\n\n" + str(warn[2][4])
            contenuto += str(warn[1][2]) + "\n\n" + str(warn[1][4])
            await app.send_message("-423298599", "**Attenzione!**\n\n" + ("**Nuovo compito assegnato**" if warn[len(warn)-1] else "**Compito modificato**") + " da " + str(warn[1][0]) + ", " + str(warn[1][1]) + ".\n" + "Da fare per il " + str(warn[0]) + (("\n\n**Contenuto**:\n" + contenuto + "\n\nAzione eseguita alle " + str(warn[2])) if warn[len(warn)-1] else ("\n\n**Vecchio contenuto**:\n" + vecchio_contenuto + "\n\n**Nuovo Contenuto**:\n" + contenuto + "\n\nAzione eseguita alle " + str(warn[3]))))
    if len(warning_arr_comunicati)>0:
        for warn in warning_arr_comunicati:
            await app.send_message("-423298599", "**Attenzione!**\n\nNuovo comunicato: " + warn)
    if len(warning_arr_voti)>0:
        for warn in warning_arr_voti:
            await app.send_message("-423298599", "**Nuovo voto inserito!**\n\n" + warn)

    warning_arr = []
    warning_arr_comunicati = []
    warning_arr_voti = []
    json_warning_comunicati = json.dumps(warning_arr_comunicati, indent = 4)
    json_warning_voti = json.dumps(warning_arr_voti, indent = 4)
    json_warning = json.dumps(warning_arr, indent = 4)
    with open(path_warning + "warning_comunicati.json", "w") as outfile:
        outfile.write(json_warning_comunicati)
    with open(path_voti + "warning.json", "w") as outfile:
        outfile.write(json_warning_voti)
    with open(path_compiti + "warning.json", "w") as outfile:
        outfile.write(json_warning) 
    return

scheduler = AsyncIOScheduler()
scheduler.add_job(warning, "interval", seconds=60)

app = Client(
    "Caldato-bot",
    bot_token=token
)
scheduler.start()
app.run()
