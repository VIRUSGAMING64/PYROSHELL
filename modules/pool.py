from threading import *
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
