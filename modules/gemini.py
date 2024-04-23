import requests as rq
import modules.Gvar as Gvar
class GenAi:
    def __init__(self,usermame,password):
        try:
            self.user = usermame
            self.password = password
            rquest = rq.get(f"https://mapi-a2dm.onrender.com/register/?username={usermame}&password={password}&repassword={password}",timeout=50000)
        except Exception as e:
            Gvar.LOG.append(str(e))
    def query(self,query):
        try:
            username=self.user
            password=self.password
            res = rq.get(f'https://mapi-a2dm.onrender.com/query/?quest="{query}"&username={username}&password={password}')
        except Exception as e:
            Gvar.LOG.append(str(e))
        if res.text == "":
            return "No answer"
        return res.text