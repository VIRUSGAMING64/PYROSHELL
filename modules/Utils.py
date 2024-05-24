import urllib.request as uq
import sys
import os
from math import *
import subprocess as subP
import yt_dlp
import requests as rq
from modules.Timer import Timer
from pyrogram.emoji import *
from pyrogram.types import *
import threading as th
import psutil as st
import time
import tarfile
from modules.datatypes import *
import modules.Gvar as Gvar

def prog(cant,total,prec=2):
    por = int((cant/total)*10)
    por2 = round((cant/total)*100)
    res = 10-por
    s = f"{por2}%\n"
    s += f"{round(cant/(1024**2))}MB of {round(total/(1024**2))}MB"
    s += "*"*por+"."*res
    s += "\n"+str(round(Gvar.UPTIME/60))
    return s

def progress(cant, total,USER,bot:pyrogram.client.Client):
    time.sleep(0.75)
    if Gvar.DATA[USER][LAST_MESSAGE_DOWNLOAD_ID] == 0:
        Gvar.DATA[USER][LAST_MESSAGE_DOWNLOAD_ID] = bot.send_message(
            chat_id=Gvar.DATA[USER][CHAT_ID], text=prog(cant,total)
        ).id
    else:
        try:
            bot.edit_message_text(
                chat_id=Gvar.DATA[USER][CHAT_ID],message_id=Gvar.DATA[USER][LAST_MESSAGE_DOWNLOAD_ID], text=prog(cant,total)
            )
        except Exception as e:
            Gvar.LOG.append(str(e))
    pass

class MyDownloader:
    file = ""
    def __init__(self, bot,user):
        self.bot = bot
        self.USER = user
        self.file = None
    def my_hook(self, down):
        curr = 0
        try:
            curr = down["downloaded_bytes"]
            self.file = down["filename"]
        except:
            pass
        total = curr * 2
        try:
            total = down["total_bytes"]
        except Exception as e:
            try:
                total = int(down["total_bytes_estimate"])
            except:
                pass
            e=str(e)
        #Gvar.FUNC_QUEUE.append([progress,[curr,total,self.USER,self.bot]])
        if Gvar.UPTIME % 7 == 0:
            progress(curr,total,self.USER,self.bot)
    def download_video(self, url):
        ydl_opts = {
            'format': 'best',
            'progress_hooks': [self.my_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

def round(fl:float,prec:int=2):
    if prec > 1e3:
        raise prec > 1e3
    r=str(fl)
    if "." in r:
        r=r.split('.')
        r[0] += "."
        for i in range(prec):
            if i >= len(r[1]):
                r[0] += '0'
            else:
                r[0]+=r[1][i]
    else:
        r = [r]
    return float(r[0])

def FindUser(user):
    i = 0
    for users in Gvar.DATA:
        if int(users[0]) == int(user):
            return i
        i += 1
    return None

def mkdir(USER, msg: str):
    if Gvar.DATA[USER][MKDIR] == 1:
        Gvar.DATA[USER][MKDIR] = 0
        try:
            msg = msg.split(" ")
            os.mkdir(msg[0])
        except Exception as e:
            Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
            
            print(e)
            try:
                os.mkdir(msg)
                return "Directory created"
            except Exception as e:
                Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
                
                print(e)
                return "Error on create directory"
            pass
        return "Directory created"
    try:
        msg = msg.split(" ")
        os.mkdir(msg[1])
        return "Directory created"
    except Exception as e:
        print(e)
        Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
        
        Gvar.DATA[USER][3] = 1
        return "Send directory name"
        pass


def __geturl(url,filename,USER):
    ret = "Downloaded..."
    try:
        Dn = uq.urlopen(url)
        D = Dn.read(1024 * 1024)
        file = open(filename,"wb")
        while D:
            file.write(D)
            D = Dn.read(1024 * 1024)
    except Exception as e:
        
        Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
        ret = "Error: " + str(e) 
    finally:
        file.close()
        return ret

def GetParent(url):
    url = list(url)
    parent = ""
    if "/" in url:
        while url[len(url)-1] != "/":
            parent = url[len(url)-1]+parent
            url.pop()
        return parent 
    else:
        Gvar.nulls_parents += 1
        return f"null{Gvar.nulls_parents}"
    
def geturl(USER, msg: str):
    if(os.path.islink(msg)):
        try:
            return __geturl(msg,GetParent(msg),USER)
        except Exception as e:
            return str(e)
    elif msg.startswith("/geturl"):
        try:
            msg = msg.split(' ')
            if len(msg) == 2:
                msg.append(GetParent(msg[1]))
            return __geturl(msg[1],msg[2],USER)
        except Exception as e:
            
            Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
            return "command sintaxis: /geturl URL FILENAME"
    else:
        try:
            msg = msg.split(' ')
            return __geturl(msg[0],msg[1])
        except Exception as e:
            
            Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
            return "incorrect link and filename format"   

def chdir(USER, msg):
    if Gvar.DATA[USER][CHDIR] == 1:
        Gvar.DATA[USER][CHDIR] = 0
        try:
            msg = msg.split(" ")
            msg = msg[0]
            try:
                msg = msg[1]
            except Exception as e:
                Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
                
                print(e, " one message")
        except Exception as e:
            print(e)
            Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
            
            pass
        if msg == "..":
            if os.path.dirname(os.getcwd()) == Gvar.ROOT:
                return "Impossible"
            os.chdir(os.path.dirname(os.getcwd()))
            Gvar.DATA[USER][PATH] = os.getcwd()
            return "changed to: " + os.getcwd()
        else:
            try:
                while len(msg) >= 1:
                    if msg[len(msg) - 1] == "/" or msg[len(msg) - 1] == "/":
                        msg.pop(len(msg) - 1)
                    else:
                        break
                M = ""
                for i in msg:
                    M += i
                msg = M
                i = len(msg) - 1
                POS = -1
                while i >= 0:
                    if msg[i] == "\\" or msg[i] == "/":
                        POS = i
                        break
                    i = i - 1
                DIR = ""
                for i in range(POS + 1, len(msg)):
                    DIR += msg[i]
                try:
                    os.chdir(DIR)
                    Gvar.DATA[USER][PATH] = Gvar.DATA[USER][PATH] + "/" + DIR
                    return "Changed to: " + os.getcwd()
                except Exception as e:
                    Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
                    
                    return e
            except Exception as e:
                Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
                
                print(e)
                return "Impossible change directory."
                pass
        return
    try:
        msg = msg.split(" ")
        msg = msg[1]
        if msg == "..":
            if os.path.dirname(os.getcwd()) == Gvar.ROOT:
                return "Impossible"
            os.chdir(os.path.dirname(os.getcwd()))
            Gvar.DATA[USER][6] = os.getcwd()
            return "changed to: " + os.getcwd()
        try:
            while len(msg) >= 1:
                if msg[len(msg) - 1] == "\\" or msg[len(msg) - 1] == "/":
                    msg.pop(len(msg) - 1)
                else:
                    break
            M = ""
            for i in msg:
                M += i
            msg = M
            i = len(msg) - 1
            POS = -1
            while i >= 0:
                if msg[i] == "\\" or msg[i] == "/":
                    POS = i
                    break
                i = i - 1
            DIR = ""
            for i in range(POS + 1, len(msg)):
                DIR += msg[i]
            try:
                os.chdir(DIR)
                Gvar.DATA[USER][PATH] = Gvar.DATA[USER][PATH] + "/" + DIR
                return "Changed to: " + os.getcwd()
            except Exception as e:
                
                Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
                return "Error on chdir: " + str(e)
        except Exception as e:
            
            Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
            print(e)
            return "Impossible change directory"
            pass
    except Exception as e:
        
        print(e)
        Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
        Gvar.DATA[USER][CHDIR] = 1
        return "send directory name"


def ls(USER):
    try:
        sstr = "in " + os.getcwd() + ": \n"
        ls = os.listdir()
        ls.sort()
        j = 1
        for i in ls:
            if os.path.isdir(i):
                sstr += f"({j}){pyrogram.emoji.FILE_FOLDER} " + i + "\n"
            elif os.path.isfile(i):
                sstr += f"({j})[file] " + i + "\n"
            elif os.path.islink(i):
                sstr += f"({j}){pyrogram.emoji.LINK} " + i + "\n"
            else:
                sstr += f"({j})[other] " + i + "\n"
            j+=1
        return sstr
    except Exception as e:
        
        Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
        print("Error: " + str(e))
        return "Error: " + str(e)


def NOTEPAD(USER, msg):
    if Gvar.DATA[USER][GETING_NOTEPAD_NAME] == 1:
        Gvar.DATA[USER][GETING_NOTEPAD_NAME] = 0
        try:
            msg = msg.split(" ")
            msg = msg[0]
            file = open(msg, "w")
            Gvar.DATA[USER][WRITING_FILEPATH] = msg
            Gvar.DATA[USER][WRITING] = 1
            file.close()
            return "file created"
        except Exception as e:
            print(e)
            Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
            
            return "Error: " + str(e)
    try:
        if msg.startswith("/note"):
            msg = msg.split(" ")
        try:
            msg = msg[1]
            try:
                file = open(msg, "w")
                file.close()
                Gvar.DATA[USER][WRITING] = 1
                Gvar.DATA[USER][WRITING_FILEPATH] = msg
            except Exception as e:
                
                Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
                return "Error: " + str(e)
        except Exception as e:
            
            Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
            Gvar.DATA[USER][GETING_NOTEPAD_NAME] = 1
            return "send filename: "
    except Exception as e:
        print(e)
        
        Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
        return "Error: " + str(e)


def WRITER(USER, msg):
    if msg.startswith("/note"):
        Gvar.DATA[USER][WRITING] = 0
        Gvar.DATA[USER][WRITING_FILEPATH] = 0
        return "Closed file"
    else:
        try:
            try:
                file = open(Gvar.DATA[USER][WRITING_FILEPATH], "a")
                total = file.write(msg)
                return f"Writed {total} bytes"
            except Exception as e:
                
                Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
                return "Error writing file "+str(e)
        except Exception as e:
            
            print(e)
            Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
            return "Error: " + str(e)


def cat(USER, msg:str):
    if Gvar.DATA[USER][CATING] == 1:
        Gvar.DATA[USER][CATING] = 0
        try:
            msg = msg.split(" ")
            msg = msg[0]
        except Exception as e:
            Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
            print(e)
            
            return "Error: " + str(e)
    elif msg.startswith("/cat"):
        try:
            msg = msg.split(' ')
            msg = msg[1]

        except Exception as e:    
            
            Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
            print(e)
            Gvar.DATA[USER][CATING] = 1
            return "Send file name"
    else:
        return "SINTAXIS ERROR: " + msg + " is /cat FILE"
    try:
        file = open(msg, "r")
        return file.read(Gvar.MAX_MESSAGE_LENGTH)
    except Exception as e:
        
        Gvar.LOG.append(str(e) +" "+ Gvar.DATA[USER][USER_ID])
        print("Error on cat:", e)
        return "Error on cat: " + str(e)
def cp(a):
    return a
def stats(F=1):
    seconds_uptime = round(cp(Gvar.UPTIME)) 
    minutes_uptime = round(seconds_uptime // 60)
    hours_uptime = round(minutes_uptime // 60)
    days_uptime = round(hours_uptime // 24)
    seconds_uptime%=60
    minutes_uptime%=60
    hours_uptime%=24
    s = ""
    if(floor(days_uptime) != 0):
        s += f"{floor(days_uptime)}d"
    if(floor(hours_uptime) != 0):
        if(s != ""): s+='-'
        s += f"{floor(hours_uptime)}h"
        pass
    if(floor(minutes_uptime) != 0):
        if(s != ""): s+='-'
        s+= f"{floor(minutes_uptime)}m"
        pass
    if(floor(seconds_uptime) != 0):
        if(s != ""): s+='-'
        s+= f"{floor(seconds_uptime)}s"
        pass
    s = "Uptime: " + s + "\n"
    CPU_P=round(st.cpu_percent(interval=1))
    CPU_F=round(st.cpu_freq().current)
    CPU_C=round(st.cpu_count())
    MEM_P = round(st.virtual_memory().percent)
    MEM_FREE= round(st.virtual_memory().available/Gvar.GB)
    RAM = round(st.virtual_memory().total/Gvar.GB)
    DISK_USED=round(100.0-st.disk_usage(os.getcwd()).percent)
    DISK_FREE=round(st.disk_usage(os.getcwd()).free/Gvar.GB)
    DISK_T = round(st.disk_usage(os.getcwd()).total/Gvar.GB)
    s += f"CPU: {CPU_P}%\n"
    s += f"CPU SPEED: {CPU_F}Mhz\n" 
    s += f"CPU COUNT: {CPU_C}\n"
    if sys.platform != "win32":
            try:
                temp = st.sensors_temperatures()["coretemp"][0]
                s+=f"CPU_TEMP: {temp.current}C\n"
                s+=f"MAX_CPU_TEMP: {temp.critical}C\n"
            except Exception as e:
                print(e)
    s += f"RAM: {RAM}GB\n"
    s += f"RAM USED: {MEM_P}%\n" 
    s += f"RAM FREE: {MEM_FREE}GB\n"
    s += f"TOTAL DISK: {DISK_T}GB\n"
    s += f"DISK USED: {DISK_USED}%\n" 
    s += f"DISK FREE: {DISK_FREE}GB\n"
    return s

def spider(user,msg): #TODO
    return "Work in progress"

def copy(message:Message): #TODO
    return "Work in progress" 
    pass

def getusers(message:Message):
    s = ""
    if message.from_user.id in Gvar.ADMINS:
        for USER in Gvar.DATA:
            s+=USER[USERNAME]+"\n"
        return s
    else:
        return "access denied"
    pass

def upd(msg:pyrogram.types.Message,Ifile,Ofile):
    time.sleep(1)
    while 1:
        time.sleep(1)
        try:
            total=os.path.getsize(Ifile)
            curr=os.path.getsize(Ofile)
            s=prog(curr,total,10)
            if s != msg.text:
                msg=msg.edit_text(s)
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(1)
def ffmpegW(Ifile,Ofile):
    os.system(f'ffmpeg -i {Ifile} -cpu-used 5 -c:v libx265 -compression_level 10 -tune "ssim" -preset "plasebo" {Ofile}')

def ffmpegL(Ifile,Ofile):
    os.system(f'ffmpeg -i {Ifile} -c:v libx264 -compression_level 10 -tune "ssim" -preset "plasebo" {Ofile}')

def VidComp(message:pyrogram.types.Message):
    try:
        msg = message.text.split(" ")
        cmd = msg[0]
        Ifile = msg[1]
        Ofile = msg[2]
        try:
            NoPass = int(msg[3])
        except:
            NoPass = 1
    except:
        return "try use /comp Ifile Ofile number of pass"
    try:
        f=open(Ifile,"r")
        f.close()
    except:
        return "file not found"
    try:
        f=open(Ofile,"r")
        f.close()
        return "Ofile already exist"
    except:
        pass
    nms = message.reply("compressing...")
    while NoPass > 0:
        NoPass -= 1
        Tth=th.Thread(target=upd,args=[nms,Ifile,Ofile],daemon=1)
        Tth.start()
        if sys.platform != "win32":
            ffmpegW(Ifile,Ofile) 
        else:
            ffmpegL(Ifile,Ofile)
        Tth.kill()
        os.remove(Ifile)
        os.rename(Ofile,Ifile)

def getZ(msg):
    msg = msg.split(" ")
    msg.append(None)
    if msg[1] is None:
        return "/getZ filename <--"
    try:
        f=open(msg[1])
        f.close()
    except:
        return "file not found"
    return os.path.getsize(msg[1])




def vid_down(usr,msg:Message,bot:pyrogram.client.Client):
    try:
        do = MyDownloader(bot,usr)
        do.download_video(msg.text)
        bot.delete_messages(msg.chat.id,msg.id)
        Gvar.DATA[usr][LAST_MESSAGE_DOWNLOAD_ID] = 0
        try:
            if do.file.endswith(".mp4") or do.file.endswith(".mkv") or do.file.endswith(".mpg"):
                bot.send_video(msg.chat.id,do.file,progress=progress,progress_args=[FindUser(msg.chat.id),bot])    
        except:
            bot.send_document(msg.chat.id,do.file,progress=progress,progress_args=[FindUser(msg.chat.id),bot])
    
    except Exception as e:
        msg.reply(str(e))
        Gvar.LOG.append(str(e))
        print(e)
def USER_PROCCESS(USER, message: Message,bot:pyrogram.client.Client):
    MSG = str(message.text)
    if MSG.startswith("http") or MSG.startswith("https"):
        Gvar.FUNC_QUEUE.append([vid_down,[USER,message,bot]])
    if MSG.startswith("/cc"):
        return copy(message)
    elif MSG.startswith('/cv'):
        return copy(message)
    elif Gvar.DATA[USER][WRITING] == 1:
        return WRITER(USER, MSG)
    elif MSG.startswith("/comp"):
        tth=th.Thread(target=VidComp,args=[message],daemon=True)
        tth.start()
        return "in progress"
    elif MSG.startswith("/news"):
        return Gvar.NEWS #change in time
    elif MSG.startswith("/help"):
        return Gvar.HELP
    elif MSG.startswith("/spider"):
        return spider(USER,MSG)
    elif MSG.startswith("/cd"):
        return os.getcwd()
    elif MSG.startswith("/getZ"):
        return str(getZ(MSG))
    elif MSG.startswith("/ls"):
        return ls(USER)
    elif MSG.startswith("/note") or Gvar.DATA[USER][GETING_NOTEPAD_NAME]:
        return NOTEPAD(USER, MSG)
    elif MSG.startswith("/chdir") or Gvar.DATA[USER][CHDIR]:
        return chdir(USER, MSG)
    elif MSG.startswith("/mkdir") or Gvar.DATA[USER][MKDIR]:
        return mkdir(USER, MSG)
    elif MSG.startswith("/geturl") or Gvar.DATA[USER][GETURL] or os.path.islink(MSG):
        return geturl(USER, MSG)
    elif MSG.startswith("/cat") or Gvar.DATA[USER][CATING]:
        return cat(USER, MSG)
    elif MSG.startswith("/logs"):
        ms = ""
        for i in range(len(Gvar.LOG)):
            ms += Gvar.LOG[i] + "\n"
        return ms
    elif MSG.startswith('/stats+'):
        return stats(1)
    elif MSG.startswith('/stats'):
        return stats(0)
    elif MSG.startswith("/getU"):
        return getusers(message)
    elif MSG.startswith('/send'):
        try:
            MSG = MSG.split(' ')[1]
            if MSG.isnumeric():
                MSG = int(MSG)
                dirs = os.listdir()
                dirs.sort()
                MSG = dirs[MSG-1]
            if(os.path.isdir(MSG)):
                tar = tarfile.TarFile(MSG + ".7z","w")
                tar.add(MSG)
                MSG = MSG + ".7z"
            bot.send_document(message.chat.id,MSG,progress=progress,progress_args=[FindUser(message.chat.id),bot])
            Gvar.DATA[USER][LAST_MESSAGE_DOWNLOAD_ID]
            return "uploaded"
        except Exception as e:
            Gvar.LOG.append(str(e) +" "+ str(Gvar.DATA[USER][USER_ID]))
            return f"File not found E:{str(e)}"
    else:
        return 0
    return 0

def UPD_HOUR():
    Gvar.UPTIME+=1
def FUNC_QUEUE_HANDLER():
    if len(Gvar.FUNC_QUEUE) > 0:
        func,args = Gvar.FUNC_QUEUE[0]
        Gvar.FUNC_QUEUE.pop(0)
        func(*args)
timer = Timer(
    [UPD_HOUR,FUNC_QUEUE_HANDLER],
    [1,1]
)
timer.start()