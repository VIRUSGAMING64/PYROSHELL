import yt_dlp
from pyrogram.types import *
from pyrogram.client import *

class VidDownloader:
    file = ""
    arg = "downloading video"
    def __init__(self, bot:Client,user,chat_id):
        self.bot = bot
        self.USER = user
        self.chat_id = chat_id
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
        #TODO poner progress args
    def download_video(self, url):
        ydl_opts = {
            'format': 'best',
            'writethumbnail': True,
            'progress_hooks': [self.my_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            #TODO eliminar menssage generado por la descarga