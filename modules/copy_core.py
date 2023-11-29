import os
import time as T
class CORE:
    Ipath = None
    Opath = None
    BLOCK_SIZE=500 #in megabytes
    @classmethod
    def __init__(self):
        pass
    def __init__(self,_Ipath,_Opath):
        self.Ipath = _Ipath
        self.Opath = _Opath
    def Tfunc(self,cant,tot,speed,args):
        print(speed / 1024**2)
        return
    def copy(self,move = False,func = None,func_args = None):
        starttime = T.time()
        Ifile = open(self.Ipath,'rb')
        Ofile = open(self.Opath,'wb')
        if(func == None):
            func = self.Tfunc
        if(Ifile.seekable() and 0):
            pass
        else:
            l = 1
            r = int(1024**2 * self.BLOCK_SIZE)
            m = int((l+r)//2)
            cant = 0
            tot = os.path.getsize(Ifile)
            while(1):
                now =T.time() 
                line = Ifile.read(m)
                if line:
                    Ofile.write(line)
                    cant += len(line)
                    try:
                        func(cant,tot,m,func_args)
                    except Exception as e:
                        func(cant,tot,m)
                    now2 = T.time()
                    if(((now2 - now) < 1) and (l <= r)):
                        l = m + 1
                    else:
                        r = m - 1 
                    m = (l + r)//2
                else:
                    break
            Ofile.close()
            Ifile.close()
            if(move == True):
                os.remove(self.Ipath)
        Ttime = T.time()-starttime
        return Ttime
