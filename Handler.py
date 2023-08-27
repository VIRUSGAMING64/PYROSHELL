import urllib.request as uq
from datatypes import *
import Gvar
import os
import ENV
from pyrogram.types import *
import threading as th
import time


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
            print(e)
            try:
                os.mkdir(msg)
                return "Directory created"
            except Exception as e:
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
        Gvar.DATA[USER][3] = 1
        return "Send directory name"
        pass


def geturl(USER, msg:str):
    return "/geturl in progress"
    #TODO
    pass


def chdir(USER, msg):
    if not msg.startswith("/chdir") and Gvar.DATA[USER][CHDIR] != 1:
        return "Debuging..."
    if Gvar.DATA[USER][CHDIR] == 1:
        Gvar.DATA[USER][CHDIR] = 0
        try:
            msg = msg.split(" ")
            try:
                msg = msg[0]
            except Exception as e:
                print(e, " one message")
        except Exception as e:
            print(e)
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
                    return e

            except Exception as e:
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
                return str(e)
        except Exception as e:
            print(e)
            return "Impossible change directory"
            pass
    except Exception as e:
        print(e)
        Gvar.DATA[USER][CHDIR] = 1
        return "send dir name"


def ls():
    try:
        sstr = "IN THIS DIRL:\n"
        ls = os.listdir()
        ls.sort()
        for i in ls:
            if os.path.isdir(i):
                sstr += "   [dir] " + i + "\n"
            elif os.path.isfile(i):
                sstr += "   [file] " + i + "\n"
            else:
                sstr += "   [other] " + i + "\n"
        return sstr
    except Exception as e:
        return str(e)


def USER_PROCCESS(USER, message:Message):
    CHAT_ID = Gvar.DATA[USER][ID]
    MSG = str(message.text)
    RES = ""
    if MSG.startswith("/cd"):
        return os.getcwd()
    elif MSG.startswith("/ls"):
        return ls()
    elif MSG.startswith("/chdir") or Gvar.DATA[USER][CHDIR]:
        return chdir(USER, MSG)
    elif MSG.startswith("/mkdir") or Gvar.DATA[USER][MKDIR]:
        return mkdir(USER, MSG)
    elif MSG.startswith("/geturl") or Gvar.DATA[USER][GETURL]:
        return geturl(USER, MSG)
    else:
        return "None"
    pass
