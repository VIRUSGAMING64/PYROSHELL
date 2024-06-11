import yt_dlp
from pyrogram.types import *
from pyrogram.client import *
import modules.Gvar as Gvar
class VidDownloader:
    file = ""
    arg = "downloading video"
    def __init__(self, bot:Client,user,chat_id,progress:callable,args:list):
        self.bot = bot
        self.progress = progress
        self.args = args
        self.user = user
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
        self.progress(*self.args)

    def download_video(self, url):
        ydl_opts = {
            'format': 'best',
            'writethumbnail': True,
            'progress_hooks': [self.my_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                self.user.download_id = self.bot.send_message(self.user.chat,"downloading").id
                ydl.download([url])
                self.bot.delete_messages(self.user.chat,self.user.download_id)
            except Exception as e:
                Gvar.LOG.append(str(e)+ " " + str(self.user.id))