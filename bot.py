from modules.imports import *
from flask import Flask,request

def WEB():
    web = Flask("vshell")
    @web.route("/",methods = ['POST', 'GET'])
    def main():
        if request.method == "POST":
            Gvar.POST_QUERYS+=1
        else:
            Gvar.GET_QUERYS+=1
        return f"POST: {Gvar.POST_QUERYS}\nGET: {Gvar.GET_QUERYS}"
    web.run("0.0.0.0",80)


def debug(e):
    _debug = open("debug-bot.txt","a")
    _debug.write(str(e) + "\n")
    _debug.close()

bot = Client(
    "virusgaming",
    api_id=Gvar.API_ID,
    api_hash=Gvar.API_HASH,
    workers=Gvar.WORKERS 
)
def DIRECT_REQUEST_HANDLER(client: Client, message: Message):
    try:
        USER = Utils.FindUser(message.chat.id)
    except Exception as e:
        print(e)
        return
    if USER == None:
        TEMP_USER = CreateNewUser(message)
        USER = len(Gvar.DATA)
        Gvar.DATA.append(TEMP_USER)
    try:
        os.chdir(Gvar.DATA[USER][PATH])
    except Exception as e:
        debug(e)
        print('\ndirect message')
        try:
            os.mkdir(Gvar.DATA[USER][PATH])
            os.chdir(Gvar.DATA[USER][PATH])
        except Exception as e:
            debug(e)
            bot.send_message(message.chat.id, "invalid directoy:    " + str(e))
            try:
                Gvar.DATA[USER][PATH] = Gvar.ROOT+ "/" + str(message.from_user.id)+'-'+str(message.from_user.first_name)
                os.mkdir(Gvar.DATA[USER][PATH])
            except Exception as e:
                debug(e)
                return
            os.chdir(Gvar.DATA[USER][PATH])
    Gvar.QUEUE_DOWNLOAD.append([message, USER])
    
    RES = Utils.USER_PROCCESS(USER, message,bot)    
    if not RES:
        return
    T_TO_SEND = []
    if(len(RES) > Gvar.MAX_MESSAGE_LENGTH):
        i = 0
        aux = ""
        while(i < len(RES)):
            for j in range(Gvar.MAX_MESSAGE_LENGTH):
                if(i + j == len(RES)):
                    break
                aux += RES[i+j]
            i += Gvar.MAX_MESSAGE_LENGTH
            T_TO_SEND.append(aux)
            aux = ''
        Gvar.QUEUE_TO_SEND.append([message,T_TO_SEND])
        Gvar.HAND.save()
        return
    Gvar.DATA[USER][BOT_LAST_MESSAGE_ID] = bot.send_message(message.chat.id, RES).id
    Gvar.DATA[USER][LAST_MESSAGE_ID] = message.id
    Gvar.HAND.save()

def INLINE_REQUEST_HANDLER(client, message: InlineQuery):  # this is hard    
    query = message.query
    URL_FINDED = 'https://www.google.com/search?client=firefox-b-d&q=work+in+progress'
    message.answer(
        results=[
            InlineQueryResultArticle(
                title="google",
                url=URL_FINDED,
                input_message_content=InputTextMessageContent(
                    message_text=URL_FINDED,
                    disable_web_page_preview=False,
                ),
            ),
        ],
        cache_time=10,
    )

def DIRECT_MESSAGE_QUEUE_HANDLER():
    while True:
        if len(Gvar.QUEUE_DIRECT) == 0:
            time.sleep(0.01)
            continue
        DIRECT_REQUEST_HANDLER(Gvar.QUEUE_DIRECT[0][0], Gvar.QUEUE_DIRECT[0][1])
        Gvar.QUEUE_DIRECT.pop(0)

def INLINE_MESSAGE_QUEUE_HANDLER():
    while True:
        if len(Gvar.QUEUE_INLINE) == 0:
            time.sleep(0.5)
            continue
        INLINE_REQUEST_HANDLER(Gvar.QUEUE_INLINE[0][0], Gvar.QUEUE_INLINE[0][1])
        Gvar.QUEUE_INLINE.pop(0)

def DOWNLOAD_HANDLER(data):
    msg = data[0]
    USER = data[1]
    if Gvar.DOWNLOADING == 0:
        if msg.media != None:
            try:
                Gvar.DOWNLOADING = 1
                Gvar.DATA[USER][LAST_MESSAGE_DOWNLOAD_ID] = bot.send_message(
                    Gvar.DATA[USER][CHAT_ID], "Donloading..."
                ).id
                bot.download_media(
                    msg,
                    Gvar.DATA[USER][PATH] + "/",
                    progress=Utils.progress,
                    progress_args=[USER,bot],
                )
                msg.reply("Downloaded !!!!")
            except Exception as e:
                debug(e)
                print("in downloads first try")
                msg.reply("Error downloading media")
            finally:
                Gvar.DATA[USER][LAST_MESSAGE_DOWNLOAD_ID] = 0
                Gvar.DOWNLOADING = 0
                return 1
        else:
            return 1
    else:
        return 0
    
def DOWNLOAD_QUEUE_HANDLER():
    while 1:
        if len(Gvar.QUEUE_DOWNLOAD) < 1:
            time.sleep(1)
            continue
        res = DOWNLOAD_HANDLER(Gvar.QUEUE_DOWNLOAD[0])
        if res == 1:
            Gvar.QUEUE_DOWNLOAD.pop(0)
        else:
            time.sleep(1)

@bot.on_inline_query()
async def on_inline_query(client: Client, message: Message):
    Gvar.QUEUE_INLINE.append([client, message])
    pass

@bot.on_message(filters.private)
async def on_private_message(client: Client, message: Message):
    if message.from_user.phone_number in Gvar.MUTED_USERS:
        return
    Gvar.QUEUE_DIRECT.append([client, message])
    pass
@bot.on_message(filters.group)
async def on_group_message(client: Client, message: Message):
    if message.mentioned:
        Gvar.QUEUE_DIRECT.append([client, message])
    pass

@bot.on_edited_message(filters.private)
async def on_edit_private_message(client, message:Message):
    await on_private_message(client, message)

def TO_SEND_QUEUE_HANDLER(): #TODO
    try:
        pass
    except Exception as e:
        debug(e)
def TORRENT_QUEUE_HANDLER(): #TODO
    try:
        pass
    except Exception as e:
        debug(e)

def INIT():
    try:
        while bot.is_connected == None:
            time.sleep(1)
        for i in Gvar.ADMINS:
            bot.send_message(i,"bot online")
    except Exception as e:
        print(e)
def ACTIVATOR():
    while 1:
        time.sleep(1)
        req.get("https://mapi-a2dm.onrender.com/bot")
pool = v_pool(
    [
        ACTIVATOR,
        WEB,
        INIT,
        DIRECT_MESSAGE_QUEUE_HANDLER,
        INLINE_MESSAGE_QUEUE_HANDLER,
        DOWNLOAD_QUEUE_HANDLER,
        TO_SEND_QUEUE_HANDLER,
        TORRENT_QUEUE_HANDLER
    ]
)
pool.start_all()
print("THREADS STARTEDS")
bot.run()