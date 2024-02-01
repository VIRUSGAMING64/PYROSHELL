from modules.imports import *
def mainapi():
    while (Gvar.BOT_ON == 0):
        print("timing...")
        time.sleep(1)
    
    app = FastAPI()
    @app.get("/")
    async def main():
        return {"documentation: ":"/redoc"}
    
    
    print("runing api")
    if 1:
        host = "0.0.0.0"
    else:
        host = "127.0.0.1"
    uvicorn.run(app,host=host,port=80,reload=0)
