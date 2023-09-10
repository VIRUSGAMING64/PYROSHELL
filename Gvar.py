import os

"""
    if you don't see work in progress in
    github is because this work is local
"""
ADMINS = [1659735368]
API_ID = 29695292
API_HASH = "8b05ce00146edeeae7aafc4bea30e713"  # bot api
HAND = ""
FILEROOT = os.getcwd()
ROOT = os.getcwd() + "\\env"  # for envs
QUEUE_INLINE = []
QUEUE_DIRECT = []
USER_VARIABLES = 21
QUEUE_DOWNLOAD = []
DOWNLOADING = 0
DATA = []
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
    "download youtube videos",
    "work with videos [combert x264 to x265]",
    "download torrent",
    "work with compresed files [ZIP]",
    "/tree command [tree of directory]",
    "/spider command [get all urls in a web page with deep X [default X = 0]]"
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
