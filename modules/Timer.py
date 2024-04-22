import time
from threading import Thread
def Time(func:callable,tm:int):
    while 1:
        time.sleep(tm)
        func()
    pass
class Timer:
    def __init__(self,func=None,time:list=[]):
        self.time = time
        if func is None:
            self.funcs = []
            self.threads=[]
            self.time = []
            return
        if func is callable:
            self.funcs = [func]
        else:
            self.funcs = func
        
            self.threads = []
        i = 0
        for func in self.funcs:
            if self.time[i] < 0:
                raise "time can't be < 0"
            self.threads.append(
                Thread(target=Time,args=[func,self.time[i]])
            )
            i+=1
    def start(self,pos=None):
        if pos is None:
            for i in range(len(self.threads)):
                self.threads[i].start()
            pass
        else:
            self.threads[pos].start()
            pass
    def stop(self,pos=None):
        if pos is None:
            for i in range(len(self.threads)):
                self.threads[i].kill()
        else:
            self.threads[pos].kill()
    def add(self,func:callable,time:int):
        self.funcs.append(func)
        self.time.append(time)
        self.threads.append(Thread(target=Time,args=[func,time]))
        self.start(len(self.time)-1)