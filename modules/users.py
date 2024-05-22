
import pyrogram
import modules.Gvar as Gvar
from modules.datatypes import *
from modules.gemini import GenAi
def CreateNewUser(message:pyrogram.types.Message):
    date = message.from_user.last_online_date
    TEMP_USER = [
            message.from_user.id,  # USER_ID  0
            message.id,  # LAST_MESSAGE_ID 1
            0,  # CHDIR 2
            0,  # MKDIR 3
            0,  # SEND 4
            0,  # GETURL 5
            Gvar.ROOT+ "/" + str(message.from_user.id) + "-" + str(message.from_user.first_name),  # PATH 6
            0,  # ASKING 7
            0,  # WRITING 8
            0,  # GETING_NOTEPAD_NAME 9
            0,  # WRITING_FILEPATH 10
            0,  # BOT_LAST_MESSAGE_ID 11
            0,  # CATING 12
            0,  # LAST_MESSAGE_DOWNLOAD_ID 13
            message.chat.id,  # chat_id 14
            message.from_user.dc_id,  # other vars 15
            message.from_user.is_verified,  # VERIFIED 16
            message.from_user.is_premium,  # PREMIUN 17
            message.from_user.language_code,  # LANG_CODE 18
            message.from_user.last_name,  # LAST_NAME 19
            message.from_user.first_name,  # FIRST_NAME 20
            message.from_user.username,  # USERNAME 21
        ]
    lt = len(TEMP_USER)
    for i in range(128-lt):
        TEMP_USER.append(0)
    del lt
    return TEMP_USER

class CSV:
    data = []
    locate = ""
    def __init__(self,file:str=Gvar.ROOT+"/user_datas.csv"):   
        self.load(file)
    def load(self,file:str = Gvar.ROOT+"/user_datas.csv"):
        self.locate = file
        file = open(file,"r")
        data = file.read(Gvar.GB)
        data = data.split("\n")
        for i in range(len(data)):
            data[i] = data[i].split(' ')
        self.data = data
        file.close()
    def save(self):
        file = open(self.locate,"w")
        it = 0
        for usr in self.data:
            for data in usr:
                file.write(data + " ")
            if(it != len(self.data)-1):
                file.write("\n") 
            it+=1
        file.close()
    def find(self,id:int | str): # O(n) -> with tree change to -> O(log(n)) #TODO
        for i in range(len(self.data)):
            if(str(self.data[i][USER_ID]) == str(id)):
                return i
        return -1
    def find(self,usr:list): # O(n) -> with tree change to -> O(log(n)) #TODO
        for i in range(len(self.data)):
            if(self.data[i] == usr):
                return i
        return -1
    def append(self,usr:list):
        return self.data.append(usr)
    def erase(self,pos):
        return self.data.pop(pos)
    def reload(self):
        self.load(self.locate)
    def sort(self):
        return self.data.sort()