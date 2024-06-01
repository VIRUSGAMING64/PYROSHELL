import os
import time
RUNNING_THREADS = 0
nulls_parents = 0
GET_QUERYS = 0
POST_QUERYS = 0
END_THREAD = 1
DEBUG_URL = os.getenv("DEBUG_URL")
DEPLOY_HOOK = os.getenv("DEPLOY_HOOK")
GOOGLE_API = os.getenv("GOOGLE")
TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")  # bot api
ADMINS = [1659735368] # <- THIS IS CHAT_ID OF ADMINS
DEBUG_GROUP_ID = -1001809067914 #TODO
HAND = None
BOT_ON = 0
UPTIME=0
FILEROOT = os.getcwd()
ROOT = os.getcwd() + "/env"  # for envs
QUEUE_INLINE = []
MUTED_USERS = [] #Use in format "code"+"number"
QUEUE_DIRECT = [] #queue for direct messages
FUNC_QUEUE = []
QUEUE_TO_SEND = [] #queue of larges messages
QUEUE_TORRENT = [] #torrent downloads
QUEUE_DOWNLOAD = [] # queue of downloads
USER_VARIABLES = 127 
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
    ["/queues","get size of queues"],
    ["/getZ","get file size"],
    ["/getU","get list of users"],
    ["/sz","get file size"],
    ["/cat", "get 4096 first bytes of file"],
    ["/geturl", "download url"],
    ["/stats", 'get server stats'],
    ["/mkdir", "make a directory"],
    ["/cd", "change of directory"],
    ["/note", "make a file to write in her"],
    ["/comp", "compress a video don't work"],
    ["/help", "send help"],
]

if DEBUG_URL == None:
    DEBUG_URL = 'https://vshell.onrender.com/debug'

HELP = ""
for i in BOT_COMMANDS:
    HELP += i[0] + " " + i[1] + "\n"
try:
    os.mkdir("env")
except:
    pass