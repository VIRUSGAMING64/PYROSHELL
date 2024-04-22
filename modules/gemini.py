import requests as rq
class GenAi:
    def __init__(self,usermame,password):
        self.user = usermame
        self.password = password
        rq.get(f"https://mapi-a2dm.onrender.com/register/?username={usermame}&password={password}&repassword={password}")
    def query(self,query):
        username=self.user
        password=self.password
        res = rq.get(f'https://mapi-a2dm.onrender.com/query/?query="{query}"&username={username}&password={password}')
        return res.text