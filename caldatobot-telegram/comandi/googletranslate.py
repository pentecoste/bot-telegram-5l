from pyrogram import Client,filters
from googletrans import Translator
translator=Translator()
cprefix="/"
@Client.on_message(filters.command("traduci",cprefix))
async def my_handler(client, message):
    send = await message.reply_text("Traducendo...")
    mess=message.text.split(" ",2)
    try:
        opt=mess[1]
    except:
        opt=-1
    try:
        arg=mess[2]
    except:
        arg=opt
    if message.reply_to_message!=None:
        arg=message.reply_to_message.text
    res=""
    try:
        if opt[0]=="-":
            if len(opt)==7:
                trad=translator.translate(arg,src=opt[1:3],dest=opt[5:7])
            elif len(opt)==5:
                if opt[1:3]=="to":
                    trad=translator.translate(arg,dest=opt[3:5])
                else:
                    trad=translator.translate(arg,src=opt[1:3])
            else:
                trad=translator.translate(arg,dest="it")
        else:
            if arg!=opt:
                arg=opt+" "+arg
            trad=translator.translate(arg,dest="it")
    except:
        trad=translator.translate(arg,dest="it")
    try:
        res+="**Input:**\n```"+trad.origin+"```\n"
        res+="**Da:** "+trad.src+"\n"
        res+="**A:** "+trad.dest+"\n"
        res+="**Output:**\n```"+trad.text+"```\n"
    #res+="**Pronuncia:**\n```"+str(trad.pronunciation)+"```"
        await send.edit_text(res)
    except:
        await send.edit_text("Non mi hai fatto tradurre niente...")
