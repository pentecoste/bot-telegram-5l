import wolframalpha
from pyrogram import Client,filters
from pyrogram.types import InputMediaPhoto
app_id = "R3KUL5-G92Q9T59AE"
cprefix = "/"
alpha = wolframalpha.Client(app_id)



@Client.on_message(filters.command("alpha",cprefix))
async def my_handler(client, message):
    send = await message.reply_photo("https://writings.stephenwolfram.com/data/uploads/2018/12/wolfram-alpha-spikey-original-official-logo.png",caption = "Calcolando...")
    result=""
    try:
        res=alpha.query(message.text.split(" ",1)[1])
    except:
        await send.edit_caption("**El xè ndà en timeout dio bueo**")
    if res.success!="false":
        for pod in res.pods:
            result+="**"+pod.title+":**\n"
            for sub in pod.subpods:
                result+=str(sub["plaintext"])+"\n"
        if int(res.numpods)<=1:
            result+="\n**Me par che el xè ndà en timeout...**"
        image=False
        conta=0
        for pod in res:
            if image!=False and conta==2:
                break
            for sub in pod.subpods:
                if "img" in sub:
                    image=sub["img"]["@src"]
                    conta+=1
                    break
        if len(result)>=1000:
            result=result[:980]+"\n\n **El resto no ghe stà...**"
        if image==False:
            try:
                await send.edit_caption(result)
            except Exception as e:
                await send.edit_caption(e)
        else:
            try:
                await send.edit_media(InputMediaPhoto(image))
                if len(result)<=1:
                    await send.edit_caption("**Ghe xe un eror col tuo query, boia dii**")
                else:
                    await send.edit_caption(result)
            except Exception as e:
                await send.edit_caption(e)
    else:
        try:
            result="**Problemi col query, forse te intedevi dir:**\n"
            if int(res.didyoumeans["@count"])>1:
                for i in res.didyoumeans["didyoumean"]:
                    result+="\n"+i["#text"]
            else:
                result+="\n"+res.didyoumeans["didyoumean"]["#text"]
            await send.edit_caption(result)
            return
        except Exception as e:
            try:
                result="**Problemi col query, forse te ga da:**\n"
                result+="\n"+res.tips["tip"]["@text"]
                await send.edit_caption(result)
            except:
                await send.edit_caption("Ghe xe un error col tuo query")
