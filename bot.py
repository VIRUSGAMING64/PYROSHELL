from pyrogram import *
from pyrogram.types import *
import time
import Gvar
from datatypes import *
import threading as th
import Handler
import os
import ENV

bot = Client("bot", api_id=Gvar.API_ID, api_hash=Gvar.API_HASH)
Gvar.HAND = ENV.MAIN()


def init():
    while not bot.is_connected:
        time.sleep(0.001)
    for i in Gvar.ADMINS:
        bot.send_message(i, "bot started...")


core1 = th.Thread(target=init)
core1.start()


def QUERY_HANDLER(client: Client, message: Message):
    USER = Handler.FindUser(message.chat.id)
    if USER == None:
        TEMP_USER = [
            message.chat.id,
            message.id,
            0,  # chdir
            0,  # mkdir
            0,  # send
            0,  # GETURL
            Gvar.ROOT + "\\" + str(TEMP_USER[ID]),
            0,  # other vars
            0,  # other vars
            0,  # other vars
            0,  # other vars
            0,  # other vars
            0,  # other vars
            0,  # other vars
            0,  # other vars
            0,  # other vars
            0,  # other vars
            0,  # other vars
            0,  # other vars
        ]
        USER = len(Gvar.DATA)
        Gvar.DATA.append(TEMP_USER)
    try:
        os.chdir(Gvar.DATA[USER][PATH])
    except:
        try:
            os.mkdir(Gvar.DATA[USER][PATH])
            os.chdir(Gvar.DATA[USER][PATH])
        except Exception as e:
            bot.send_message(message.chat.id, "invalid directoy:    " + str(e))
            try:
                Gvar.DATA[USER][PATH] = Gvar.ROOT + "\\" + str(message.chat.id)
                os.mkdir(Gvar.DATA[USER][PATH])
            except:
                pass
            os.chdir(Gvar.DATA[USER][PATH])
    Gvar.QUEUE_DOWNLOAD.append([message, USER])
    RES = Handler.USER_PROCCESS(USER, message)
    message.reply(RES)
    Gvar.DATA[USER][LAST_MESSAGE_ID] = message.id
    Gvar.HAND.save()
    pass


def CORE0():
    while 1:
        if len(Gvar.QUEUE_DIRECT) == 0:
            time.sleep(0.001)
            continue
        QUERY_HANDLER(Gvar.QUEUE_DIRECT[0][0], Gvar.QUEUE_DIRECT[0][1])
        Gvar.QUEUE_DIRECT.pop(0)


def progress(total, cant):
    print(f"{cant} of {total}")
    pass


def DOWN():
    while 1:
        if len(Gvar.QUEUE_DOWNLOAD) < 1:
            time.sleep(1)
            continue
        res = DownloadMedia(Gvar.QUEUE_DOWNLOAD[0])
        if res == 1:
            Gvar.QUEUE_DOWNLOAD.pop(0)


def DownloadMedia(data):
    msg = data[0]
    USER = data[1]
    if Gvar.DOWNLOADING == 0:
        if msg.media != None:
            try:
                Gvar.DOWNLOADING = 1
                bot.download_media(
                    msg,
                    Gvar.DATA[USER][PATH] + "/",
                    progress=progress,
                )
                msg.reply("Downloaded")
            except:
                msg.reply("Error downloading media")
            finally:
                Gvar.DOWNLOADING = 0
                return 1
        return 1
    else:
        return 0


@bot.on_inline_query()
async def on_inline_query(client: Client, message: Message):
    Gvar.QUEUE_INLINE.append([client, message])
    pass


@bot.on_message(filters.private)
async def on_private_message(client: Client, message: Message):
    Gvar.QUEUE_DIRECT.append([client, message])
    pass


@bot.on_edited_message()
async def on_edit_message(client, message):
    await on_private_message(client, message)


"""
DATA[0] = chatid
DATA[1] = LAST_MESSAGE_ID
DATA[2] = chdir
DATA[3] = mkdir
DATA[4] = send
DATA[5] = urlget 
DATA[6] = PATH
"""

DOWNLOADER = th.Thread(target=DOWN)
CORE = th.Thread(target=CORE0)
DOWNLOADER.start()
CORE.start()
bot.run()
