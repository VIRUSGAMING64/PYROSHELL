import requests as rq
import modules.Gvar as Gvar
import google.generativeai as googleIA
import os
googleIA.configure(api_key=os.getenv("GOOGLE"))
class GenAI:
    def __init__(self):
        self.model = googleIA.GenerativeModel().start_chat()
    def query(self,qe:str):
        return self.model.send_message(qe).text

chats = {
    "id":GenAI
}

def NewChat(id):
    chats[id] = GenAI()
    return chats[id]

def GetAI(id):
    try:
        chat = chats[id]
        return chat 
    except Exception as e:
        print(str(e))
        return NewChat(id)

NewChat(1).query("hola")