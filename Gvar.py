import os

ADMINS = [1659735368]
API_ID = 29695292
API_HASH = "8b05ce00146edeeae7aafc4bea30e713"  # bot api
HAND = ""
ROOT = os.getcwd() + "\\env"  # for envs
QUEUE_INLINE = []
QUEUE_DIRECT = []
QUEUE_DOWNLOAD = []
DOWNLOADING = 0
DATA = []


try:
    os.mkdir("Public")
except:
    pass
try:
    os.mkdir("env")
except:
    pass
