from pyrogram import filters,Client
import wikipedia
wikipedia.set_lang("it")
cprefix="/"

@Client.on_message(filters.command("wiki",cprefix))
async def my_handler(client, message):
    send = await message.reply_text("Cercando...")
    try:
        await send.edit_text(str(wikipedia.summary(message.text.split(" ",1)[1])))
    except Exception as e:
        await send.edit_text(e)
@Client.on_message(filters.command("wikilang",cprefix))
async def lingua(client, message):

    try:
        wikipedia.set_lang(message.command[1])
        await message.reply_text("Lingua cambiata con successo!")
    except:
        await message.reply_text("Mi sa... che hai inserito una lingua che non esiste")
