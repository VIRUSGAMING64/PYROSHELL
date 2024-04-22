import os
import time

"""
    En este modulo estan las variables globales
    if you don't see work in progress in
    github is because this work is local

"""
GET_QUERYS = 0
POST_QUERYS = 0
TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")  # bot api
ADMINS = [1659735368] # <- THIS IS CHAT ID OF ADMINS
HAND = None
BOT_ON = 0
FILEROOT = os.getcwd()
ROOT = os.getcwd() + "/env"  # for envs
QUEUE_INLINE = []
MUTED_USERS = [] #Use in format "code"+"number"
QUEUE_DIRECT = [] #queue for direct messages
QUEUE_TO_SEND = [] #queue of larges messages
QUEUE_TORRENT = [] #torrent downloads
QUEUE_DOWNLOAD = [] # queue of downloads
USER_VARIABLES = 31 
DEBUG_MODE = True
DOWNLOADING = 0 # if 1 user downloading 
DATA = [] # all users and `variables
MAX_MESSAGE_LENGTH = 4096 
WORKERS = os.cpu_count()  
LOG = []
START_TIME = time.time_ns()
SECOND = 10**9
B  = 1024**0
KB = 1024**1
MB = 1024**2
GB = 1024**3
TB = 1024**4
YB = 1024**5
BOT_COMMANDS = [
    ["BOT","COMMANDS"],
    ["/ls", "send files and dirs in this rute"],
    ["/send",'send a file'],
    ["/cc","copy element"],
    ["/cv","paste file"],
    ["/sz","get file size"],
    ["/cat", "get 4096 first bytes of file"],
    ["/geturl", "download url"],
    ["/stats", 'get server stats'],
    ["/tree", "make directorys tree"],
    ["/mkdir", "make a directory"],
    ["/chdir", "change of directory"],
    ["/note", "make a file to write in her"],
    ["/cd", "show actual directory"],
    ["/news", "show work in progress"],
    ["/help", "send help"],
]

IN_PROGRESS = [
    "download youtube videos", # libreria de ytd_lib
    "work with videos [combert x264 to x265]", # ????
    "download torrent", # ????
    "work with compresed files [ZIP]", #esto creo que hay documentacion en los .7z
    "/spider command [get all urls in a web page with deep X [default X = 0]]" # esto debe hacerse con HTTPHandler de urllib.request
]


HELP = ""
NEWS = ""
for i in IN_PROGRESS:
    NEWS += i + "\n"
for i in BOT_COMMANDS:
    HELP += i[0] + " " + i[1] + "\n"
try:
    os.mkdir("env")
except:
    pass
