from threading import *
import time
import os
class TempFile():
    def __init__(self,name,mode):
        self.name = os.path.realpath(name)
        self.mode = mode
        self.file = open(name,mode)
    def write(self,data):
        return self.file.write(data)
    def read(self,size):
        return self.file.read(size)
    def kill(self):
        self.file.close()
        os.remove(self.name)

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
    def add(self,func:callable,time:int):
        self.funcs.append(func)
        self.time.append(time)
        self.threads.append(Thread(target=Time,args=[func,time]))
        self.start(len(self.time)-1)

class v_pool:
    funcs:list[Thread] = []
    def __init__(self,funcs:list,args:list[list]=[],sequence:bool=False):
        for i in range(len(funcs)):
            if(i < len(args)):
                if args[i] == None:
                    args[i] = ()    
                funcs[i] = Thread(target=funcs[i],args=args[i])
            else:
                funcs[i] = Thread(target=funcs[i])
        self.sequence = sequence
        self.funcs = funcs
    def start_all(self,deamon = 0,indices = []):
        if indices != []:
            for i in indices:
                self.Setdeamon(i,deamon)
        elif deamon != 0:
            self.Setdeamon()
        for i in range(len(self.funcs)):
            if self.funcs[i].is_alive() == 0:
                if self.sequence == 0:
                    self.funcs[i].start()
                else:
                    self.funcs[i].join()
        return 1
    def start(self,index:int=None):
        if(index == None):
            return self.start_all()
        if(self.funcs[index].is_alive()):
            return 0
        return self.funcs[index].start()
    def Setdeamon(self,index=None,deamon = 1):
        if index is None:
            for i in range(len(self.funcs)):
                self.funcs[i].daemon=deamon
        else:
            self.funcs[index].daemon=deamon
    def add_thread(self,func:callable,start = 1,deamon=0):
        func=Thread(target=func,deamon=deamon)
        self.funcs.append(func)
        if(start):
            self.funcs[len(self.funcs)].start()
