import os

"""
    if you don't see work in progress in
    github is because this work is local
"""
ADMINS = [1659735368] # <- THIS IS CHAT ID OF ADMINSS
API_ID = 29695292
API_HASH = "8b05ce00146edeeae7aafc4bea30e713"  # bot api
HAND = ""
FILEROOT = os.getcwd()
ROOT = os.getcwd() + "\\env"  # for envs
QUEUE_INLINE = []
MUTED_USERS = [] #Use in format "code"+"number"
QUEUE_DIRECT = [] #queue for direct messages
USER_VARIABLES = 21 
QUEUE_DOWNLOAD = [] # queue of downloads
DOWNLOADING = 0 # if 1 user downloading 
DATA = [] # all users and variables
MAX_MESSAGE_LENGTH = 4096 
WORKERS = os.cpu_count() 
TOKEN = None  # bot token 

BOT_COMMANDS = [
    ["/help", "send help"],
    ["/ls", "send files and dirs in this rute"],
    ["/cat", "get 4096 first bytes of file"],
    ["/geturl", "download url"],
    ["/mkdir", "make a directory"],
    ["/chdir", "change of directory"],
    ["/note", "make a file to write in her"],
    ["/cd", "show actual directory"],
    ["/news", "show work in progress"],
]

IN_PROGRESS = [
    "download youtube videos", # libreria de jlsearch bot o buscar en github??
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
    os.mkdir("Public")
except:
    pass
try:
    os.mkdir("env")
except:
    pass
