import urllib.request as uq
from datatypes import *
import Gvar
import os
from tree import *
import ENV
from pyrogram.emoji import *
from pyrogram.types import *
import threading as th
import time

def debug(e):
    _debug = open("debug-utils.txt","a")
    _debug.write(str(e) + "\n")
    _debug.close()


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
            debug(e)
            print(e)
            try:
                os.mkdir(msg)
                return "Directory created"
            except Exception as e:
                debug(e)
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
        debug(e)
        Gvar.DATA[USER][3] = 1
        return "Send directory name"
        pass


def __geturl(url,filename):
    ret = "Downloaded..."
    try:
        Dn = uq.urlopen(url)
        D = Dn.read(1024 * 1024)
        file = open(filename,"wb")
        while D:
            file.write(D)
            D = Dn.read(1024 * 1024)
    except Exception as e:
        debug(e)
        ret = "Error: " + str(e) 
    finally:
        file.close()
        return ret

def geturl(USER, msg: str):
    if msg.startswith("/geturl"):
        try:
            msg = msg.split(' ')
            return __geturl(msg[1],msg[2])
        except Exception as e:
            debug(e)
            return "command sintaxis: /geturl URL FILENAME"
    else:
        try:
            msg = msg.split(' ')
            return __geturl(msg[0],msg[1])
        except Exception as e:
            debug(e)
            return "incorrect link and filename format"   
            

def chdir(USER, msg):
    if Gvar.DATA[USER][CHDIR] == 1:
        Gvar.DATA[USER][CHDIR] = 0
        try:
            msg = msg.split(" ")
            try:
                msg = msg[0]
            except Exception as e:
                debug(e)
                print(e, " one message")
        except Exception as e:
            print(e)
            debug(e)
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
                    Gvar.DATA[USER][PATH] = Gvar.DATA[USER][PATH] + "\\" + DIR
                    return "Changed to: " + os.getcwd()
                except Exception as e:
                    debug(e)
                    return e

            except Exception as e:
                debug(e)
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
                Gvar.DATA[USER][PATH] = Gvar.DATA[USER][PATH] + "\\" + DIR
                return "Changed to: " + os.getcwd()
            except Exception as e:
                debug(e)
                return "Error on chdir: " + str(e)
        except Exception as e:
            debug(e)
            print(e)
            return "Impossible change directory"
            pass
    except Exception as e:
        debug(e)
        print(e)
        Gvar.DATA[USER][CHDIR] = 1
        return "send directory name"


def ls():
    try:
        sstr = "in " + os.getcwd() + ": \n"
        ls = os.listdir()
        ls.sort()
        for i in ls:
            if os.path.isdir(i):
                sstr += "   [dir] " + i + "\n"
            elif os.path.isfile(i):
                sstr += "   [file] " + i + "\n"
            elif os.path.islink(i):
                sstr += "   [link] " + i + "\n"
            else:
                sstr += "   [other] " + i + "\n"
        return sstr
    except Exception as e:
        debug(e)
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
            debug(e)
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
                debug(e)
                return "Error: " + str(e)
        except Exception as e:
            debug(e)
            Gvar.DATA[USER][GETING_NOTEPAD_NAME] = 1
            return "send filename: "
    except Exception as e:
        print(e)
        debug(e)
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
                debug(e)
                return "Error writing file "+str(e)
        except Exception as e:
            debug(e)
            print(e)
            return "Error: " + str(e)


def cat(USER, msg:str):
    if Gvar.DATA[USER][CATING] == 1:
        Gvar.DATA[USER][CATING] = 0
        try:
            msg = msg.split(" ")
            msg = msg[0]
        except Exception as e:
            print(e)
            debug(e)
            return "Error: " + str(e)
    elif msg.startswith("/cat"):
        try:
            msg = msg.split(' ')
            msg = msg[1]

        except Exception as e:    
            debug(e)
            print(e)
            Gvar.DATA[USER][CATING] = 1
            return "Send file name"
    else:
        return "SINTAXIS ERROR: " + msg + " is /cat FILE"
    try:
        file = open(msg, "r")
        return file.read(Gvar.MAX_MESSAGE_LENGTH)
    except Exception as e:
        debug(e)
        print("Error on cat:", e)
        return "Error on cat: " + str(e)

def tree(user,msg):
    dt = TreeMaker()
    dt.show=False
    dt.showfiles = True
    dt.tree(Gvar.DATA[user][PATH])
    return dt.trees

def spider(user,msg):
    return "Work in progress"

def getsize(user,msg):
    return "Work in progress"

def USER_PROCCESS(USER, message: Message):
    CHAT_ID = Gvar.DATA[USER][ID]
    MSG = str(message.text)
    RES = ""
    if Gvar.DATA[USER][WRITING] == 1:
        return WRITER(USER, MSG)
    elif MSG.startswith("/sz"):
        return getsize(USER,MSG)
    elif MSG.startswith("/tree"):
        return tree(USER,MSG)
    elif MSG.startswith("/news"):
        return Gvar.NEWS #change in time
    elif MSG.startswith("/help"):
        return Gvar.HELP
    elif MSG.startswith("/spider"):
        return spider(USER,MSG)
    elif MSG.startswith("/note") or Gvar.DATA[USER][GETING_NOTEPAD_NAME]:
        return NOTEPAD(USER, MSG)
    elif MSG.startswith("/cd"):
        return os.getcwd()
    elif MSG.startswith("/ls"):
        return ls()
    elif MSG.startswith("/chdir") or Gvar.DATA[USER][CHDIR]:
        return chdir(USER, MSG)
    elif MSG.startswith("/mkdir") or Gvar.DATA[USER][MKDIR]:
        return mkdir(USER, MSG)
    elif MSG.startswith("/geturl") or Gvar.DATA[USER][GETURL]:
        return geturl(USER, MSG)
    elif MSG.startswith("/cat") or Gvar.DATA[USER][CATING]:
        return cat(USER, MSG)
    else:
        return "None"
    pass
