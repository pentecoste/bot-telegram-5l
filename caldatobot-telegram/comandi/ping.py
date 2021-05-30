from pyrogram import filters,Client
from datetime import datetime
cprefix="/"

@Client.on_message(filters.command("ping",cprefix))
async def my_handler(client, message):
    send = await message.reply_text("🏓 Ping!")
    start = datetime.now()
    await send.edit_text("⚪ Pong!")
    end = datetime.now()
    ms = (end - start).seconds*1000+(end - start).microseconds // 1000
    await send.edit_text("🏓 Pong!\n```{}``` ms".format(ms))
