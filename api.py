from fastapi import *
import json
import uvicorn
def mainapi():
   
    app = FastAPI()
    @app.get("/help")
    async def help():
        api = {
            "documentation":"/redoc",
            "get_names":"/name",
        }
        return api
    @app.get("/name")
    async def name(id:int = 10,size:int = 17):
        if(size > 17):
            return -1
        num = []
        id = str(2**id)
        st = ""
        for i in (id):
            st+=str(i)
            if(len(st) == size):
                print("here")
                num.append(st)
                st = ""
        if(len(st)):
            num.append(st)
        return num
        
    print("runing api")
    if 0:
        host = "0.0.0.0"
    else:
        host = "127.0.0.1"
    uvicorn.run(app,host=host,port=80,reload=0)

mainapi()