from modules.imports import *
############################################################
def WEB():
    web = Flask("vshell")
    @web.route("/<path:sub_path>")
    def public(sub_path):
        if(sub_path.endswith('.js') or sub_path.endswith('.ts')):
            return Response(route(Gvar.FILEROOT+'/web/'+sub_path), mimetype='application/javascript')
        return route(Gvar.FILEROOT+'/web/'+sub_path)

    @web.route("/debug",methods = ['POST', 'GET'])    
    def web_debug():
        try:
            if request.method == "POST":
                Gvar.POST_QUERYS+=1
            else:
                Gvar.GET_QUERYS+=1
                if __name__ != "__main__":        
                    while bot.is_connected == None:
                        time.sleep(1)
                    bot.send_message(-1001809067914,f"GET: {Gvar.GET_QUERYS} POST: {Gvar.POST_QUERYS}\n"+Utils.stats())
                    pass
            return open(Gvar.FILEROOT+"/web/index.html","rb").read(2**31)        
        except Exception as e:
            for i in Gvar.ADMINS:
                bot.send_message(i,str(e))
        return "nothing"

    def route(url):
        try:
            file = open(url,'rb')
            line = file.read(65535)
            text = b""
            while line:
                text = text + line
                line = file.read(65535)
            return text
        except Exception as e:
            return str(e)
    
    @web.route("/api/users")
    def api_users():
        enc = JSONEncoder()        
        return Response(enc.encode(Gvar.DATA),mimetype="application/json")
    
    @web.route("/api/logs")
    def bot_logs():
        enco = JSONEncoder()
        return Response(enco.encode(Gvar.LOG),mimetype="application/json")
    
    @web.route("/api/stats")
    def bot_stats():
        stats = Utils.stats().split("\n")
        stats.pop()
        for i in range(len(stats)):
            stats[i] = stats[i].split(":")
            try:    
                while stats[i][1][0] == " ":
                    stats[i][1] = stats[i][1].removeprefix(" ")
            except Exception as e:
                print(e)
        enc = JSONEncoder()
        
        stats = enc.encode(stats)
        
        return Response(stats,mimetype="application/json")
    
    @web.route("/api/commands")
    def api_command():
        enc = JSONEncoder()
        BOT_COMMANDS = Gvar.BOT_COMMANDS.copy()
        BOT_COMMANDS.pop(0)        
        return Response(enc.encode(BOT_COMMANDS),mimetype="application/json")
    
    @web.route("/")
    def main():
        return route(Gvar.FILEROOT+"/web/index.html")
        pass
    web.run("0.0.0.0",80)
#############################################################
## FLASK ##
###########

def debug(e):
    _debug = open("debug-bot.txt","a")
    _debug.write(str(e) + "\n")
    _debug.close()

bot = Client(
    "virusgaming",
    api_id=Gvar.API_ID,
    api_hash=Gvar.API_HASH,
    workers=Gvar.WORKERS,
    bot_token=Gvar.TOKEN
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
    try:
        Gvar.DATA[USER][BOT_LAST_MESSAGE_ID] = bot.send_message(message.chat.id, RES).id
    except exceptions.flood_420.FloodWait as err:
        print(err," VALUE::: ",err.value)
        if err.value is str:
            err.value = int(err.value)
        time.sleep(err.value+1)
        pass
    Gvar.DATA[USER][LAST_MESSAGE_ID] = message.id
    Gvar.HAND.save()

def INLINE_REQUEST_HANDLER(client, message: InlineQuery):  # this is hard    
    query = message.query
    id=message.from_user.id
    gemini = GetAI(id)
    text = gemini.query(query)
    message.answer(
        results=[
            InlineQueryResultArticle(
                title="gemini-AI",
                description=text[0:15]+"...",
                input_message_content=InputTextMessageContent(
                    message_text=text
                ),
                
            ),
        ],
        cache_time=1000
    )

def DIRECT_MESSAGE_QUEUE_HANDLER():
    while True:
        try:
            if len(Gvar.QUEUE_DIRECT) == 0:
                time.sleep(0.01)
                continue
            DIRECT_REQUEST_HANDLER(Gvar.QUEUE_DIRECT[0][0], Gvar.QUEUE_DIRECT[0][1])
        except Exception as e:
            Gvar.LOG.append(str(e))
        Gvar.QUEUE_DIRECT.pop(0)

def INLINE_MESSAGE_QUEUE_HANDLER():
    while True:
        try:
            if len(Gvar.QUEUE_INLINE) == 0:
                time.sleep(0.5)
                continue
            INLINE_REQUEST_HANDLER(Gvar.QUEUE_INLINE[0][0], Gvar.QUEUE_INLINE[0][1])
        except Exception  as e:
            Gvar.LOG.append(str(e))
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
        try:
            if len(Gvar.QUEUE_DOWNLOAD) < 1:
                time.sleep(1)
                continue
            res = DOWNLOAD_HANDLER(Gvar.QUEUE_DOWNLOAD[0])
        except Exception as e:
            Gvar.LOG.append(str(e))
            print(e)
            res = 1
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
        try:
            time.sleep(60)
            req.get("https://vshell2.onrender.com/debug")
        except Exception as e:
            print(str(e))

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
pool.start_all(1)
print("THREADS STARTEDS")
try:
    bot.run()
except Exception as e:
    print(str(e))