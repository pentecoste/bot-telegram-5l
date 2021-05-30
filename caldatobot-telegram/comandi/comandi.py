import json
from datetime import datetime, timedelta
import random
import math
from pyrogram import filters,Client
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
API_TOKEN = ""
path = "/home/botwht/dav-syncer-compiti/"
path_comunicati = "/home/botwht/dav-syncer-comunicati/"
path_botwht = "/home/"
admin_id = 186728021

orario = [["lun", "Notari\nNotari\nNegroni\nSimonetto\nVicari\n\nAggiornato al 18 ottobre 2020"], ["mar", "Simonetto\nUcci\nLa Rosa\nVicari\nNotari\n\nAggiornato al 18 ottobre 2020"], ["mer", "Negroni\nNotari\nZoppelli\nNotari\nCaporin\n\nAggiornato al 18 ottobre 2020"], ["gio", "Vicari\nVicari\nNotari\nNotari\nNegroni\n\nAggiornato al 18 ottobre 2020"], ["ven", "Tonolo\nZoppelli\nZoppelli\nSimonetto\nVicari\n\nAggiornato al 18 ottobre 2020"], ["sab", "La Rosa\nSimonetto\nCaporin\nZoppelli\nUcci\n\nAggiornato al 18 ottobre 2020"]]

comunicati = []


@Client.on_message(filters.command(["start","help"]))
async def start(client, message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply_text("Ciao! Mi hai startato! Stavo dormendo.")


@Client.on_message(filters.command(["anastrofe"]))
async def anastrofinator(client, message):
    args = message.command[1:]
    if not len(args):
        return
    times = 1
    if args[0] == "-t":
        try:
            times = int(args[1])
            args = args[2:]
        except:
            pass
    if len(args) == 1:
        await message.reply_text(args[0], quote=False)
    for i in range(times):
        r = random.randint(0, len(args)-2)
        temp = args[r]
        args[r] = args[r+1]
        args[r+1] = temp
    args[0] = args[0][0].upper() + args[0][1:].lower()
    anastrofized_string = args[0] + " "
    for x in range(len(args)-1):
        if args[x][len(args[x])-1] == ".":
            try:
                args[x+1] = args[x+1][0].upper() + args[x+1][1:]
            except:
                pass
        else:
            args[x+1] = args[x+1].lower()
        anastrofized_string += args[x+1] + " "
    await message.reply_text(anastrofized_string, quote=False)



@Client.on_message(filters.command(["orario"]))
async def orari(client, message):
    text_lower = message.text.lower()
    orario_richiesto = ""
    print(datetime.now().hour)
    if "dom" in text_lower or (len(message.command) == 1 and datetime.now().hour > 12):
        domani = datetime.now() + timedelta(1)
        weekday_domani = domani.weekday()
        giornoprima = (domani - timedelta(1)).weekday()
        giornodopo = (domani + timedelta(1)).weekday()
        if giornoprima > 5:
            giornoprima = 5
        if giornodopo > 5:
            giornodopo = 0
        try:
            await message.reply_text(orario[weekday_domani][0][0].upper() + orario[weekday_domani][0][1:len(orario[weekday_domani][0])]+ "\n\n" + orario[weekday_domani][1], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️",callback_data="orario "+orario[giornoprima][0]),InlineKeyboardButton("➡️",callback_data="orario "+orario[giornodopo][0])]]))
        except:
            if weekday_domani == 6:
                await message.reply_text("Domani è domenica! La messa è alle " + str(random.randint(0,23)) + ":00")
            return
        return
    if "oggi" in text_lower or (len(message.command) == 1 and datetime.now().hour < 12):
        oggi = datetime.now()
        weekday_oggi = oggi.weekday()
        giornoprima = (oggi - timedelta(1)).weekday()
        giornodopo = (oggi + timedelta(1)).weekday()
        if giornodopo > 5:
            giornodopo = 0
        if giornoprima > 5:
            giornoprima = 5
        try:
            await message.reply_text(orario[weekday_oggi][0][0].upper() + orario[weekday_oggi][0][1:len(orario[weekday_oggi][0])]+ "\n\n" + orario[weekday_oggi][1], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️",callback_data="orario "+orario[giornoprima][0]),InlineKeyboardButton("➡️",callback_data="orario "+orario[giornodopo][0])]]))
        except:
            if weekday_oggi == 6:
                await message.reply_text("Oggi è domenica! la messa è alle " + str(random.randint(0,23)) + ":00")
            return
        return
    settimana = False
    if "settimana" in text_lower:
        settimana = True
    count = 0
    day = 0
    ind = 0
    for x in orario:
        if x[0] in text_lower or settimana:
            orario_richiesto += x[0][0].upper() + x[0][1:len(x[0])] + "\n\n" + x[1] + "\n\n\n"
            day = ind
            count += 1
        ind += 1
    if len(orario_richiesto):
        orario_richiesto = orario_richiesto[0:len(orario_richiesto)-3]
        if count > 1:
            await message.reply_text(orario_richiesto)
        else:
            giornoprima = day - 1
            giornodopo = day + 1
            if day == 5:
                giornodopo = 0
            if day == 0:
                giornoprima = 5
            await message.reply_text(orario_richiesto, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️",callback_data="orario "+orario[giornoprima][0]),InlineKeyboardButton("➡️",callback_data="orario "+orario[giornodopo][0])]]))

@Client.on_message(filters.command("comunicati"))
async def comunicatis(client, message):
    global comunicati
    with open(path_comunicati+"comunicati.json") as openfile:
        try:
            data = openfile.read()
            comunicati = json.loads(data)
        except Exception as e:
            print("UDDIO! Cannot load JSON file comunicati.json\n\n" + str(e))
    await message.reply_text((comunicati[0][0] + "\n\n" + comunicati[0][1]), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️", callback_data="comunicati 1"),InlineKeyboardButton("➡️",callback_data="comunicati 0")]]))

@Client.on_callback_query(filters.regex("comunicati"))
async def comunicat(client, callback_query):
    message = callback_query.message
    try:
        n = int(callback_query.data[-2:].strip())
    except:
        pass
    if n >= len(comunicati)-1:
        try:
            await message.edit_text(comunicati[n][0] + "\n\n" + comunicati[n][1], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️", callback_data="comunicati "+str(n)),InlineKeyboardButton("➡️",callback_data="comunicati "+str(n-1))]])) 
        except:
            pass
    elif n <= 0:
        try:
            await message.edit_text(comunicati[n][0] + "\n\n" + comunicati[n][1], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️", callback_data="comunicati "+str(n+1)),InlineKeyboardButton("➡️",callback_data="comunicati "+str(n))]])) 
        except:
            pass
    else:
        try:
            await message.edit_text(comunicati[n][0] + "\n\n" + comunicati[n][1], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️", callback_data="comunicati "+str(n+1)),InlineKeyboardButton("➡️",callback_data="comunicati "+str(n-1))]])) 
        except:
            pass


@Client.on_callback_query(filters.regex("orario"))
async def orar(client, callback_query):
    message = callback_query.message
    text_lower = callback_query.data 
    orario_richiesto = ""
    giorno = 0
    for x in orario:
        if x[0] in text_lower:
            orario_richiesto += x[0][0].upper() + x[0][1:len(x[0])] + "\n\n" + x[1] + "\n\n\n"
            break
        giorno += 1
    orario_richiesto = orario_richiesto[0:len(orario_richiesto)-3]
    giornoprima = giorno - 1
    giornodopo = giorno + 1
    if giornodopo > 5:
        giornodopo = 0
    if giornoprima < 0:
        giornoprima = 5
    await message.edit_text(orario_richiesto, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️",callback_data="orario "+orario[giornoprima][0]),InlineKeyboardButton("➡️",callback_data="orario "+orario[giornodopo][0])]]))

@Client.on_message(filters.command(["commands"]))
async def echo(client, message):
    await message.reply_text("Ecco qui la lista dei comandi:\n/orario lun/mar/mer/gio/ven/sab\n/help\n/compiti domani/oggi/YYYY-MM-DD\n/anastrofe -t n frase\n/pokedex\n/copypasta")


@Client.on_message(filters.command(["cicciogamer89"]))
async def ciccio(client, message):
    with open(path_botwht+"ciccio.json", "r") as openfile:
        try:
            data = openfile.read()
            cicciogamer = json.loads(data)
        except:
            print("UDDIO! Cannot load JSON file badwords.json")
            return
    await message.reply_text(cicciogamer[random.randint(0, len(cicciogamer)-1)])

@Client.on_message(filters.command(["copypasta"]))
async def copypasta(client, message):
    with open(path_botwht+"copypasta.json", "r") as openfile:
        try:
            data = openfile.read()
            copypasta = json.loads(data)
        except:
            print("UDDIO! Cannot load JSON file badwords.json")
            return
    copypasta_ = copypasta[random.randint(0, len(copypasta)-1)]
    if copypasta_["index"] == -1:
        await message.reply_text(copypasta_["content"])
    else:
        await message.reply_text(copypasta_["content"][:copypasta_["index"]] + message.from_user.first_name + copypasta_["content"][copypasta_["index"]:])

@Client.on_message(filters.command(["addcopypasta"]))
async def addcopypasta(client, message):
    if message.from_user.id == admin_id:
        with open(path_botwht+"copypasta.json", "r") as openfile:
            try:
                data = openfile.read()
                copypasta = json.loads(data)
            except:
                print("UDDIO! Cannot load JSON file badwords.json")
                return
        try:
            copypasta_text = message.text.split(" | ")[1]
            copypasta_index = message.text.split(" | ")[2]
            copypasta.append({"content":copypasta_text, "index":int(copypasta_index)})
        except:
            return
        json_copypasta = json.dumps(copypasta, indent = 4)
        with open(path_botwht+"copypasta.json", "w") as outfile:
            outfile.write(json_copypasta)
        await message.reply_text("Copypasta aggiunto!")
    else:
        await message.reply_text("Solo Vendra può farlo")

@Client.on_message(filters.command(["printlastcopypasta"]))
async def printlastcopypasta(client, message):
    if message.from_user.id == admin_id:
        with open(path_botwht+"copypasta.json", "r") as openfile:
            try:
                data = openfile.read()
                copypasta = json.loads(data)
            except:
                print("UDDIO! Cannot load JSON file badwords.json")
                return
        await message.reply_text(copypasta[-10:])
    else:
        await message.reply_text("Solo Vendra può farlo")

@Client.on_message(filters.command(["removelastcopypasta"]))
async def removelastcopypasta(client, message):
    if message.from_user.id == admin_id:
        with open(path_botwht+"copypasta.json", "r") as openfile:
            try:
                data = openfile.read()
                copypasta = json.loads(data)
            except:
                print("UDDIO! Cannot load JSON file badwords.json")
                return
        copypasta = copypasta[:-1]
        json_copypasta = json.dumps(copypasta, indent = 4)
        with open(path_botwht+"copypasta.json", "w") as outfile:
            outfile.write(json_copypasta)
        await message.reply_text("Copypasta rimosso!")
    else:
        await message.reply_text("Solo Vendra può farlo")

@Client.on_message(filters.command(["pokedex"]))
async def poke(client, message):
    with open(path_botwht+"pokedex.json") as openfile:
        try:
            data = openfile.read()
            pokedex = json.loads(data)
        except:
            print("UDDIO! Cannot load JSON file pokedex.json")
            return
    await message.reply_text(pokedex[random.randint(0,len(pokedex)-1)])
