import os
from modules.Gvar import *
class FILE_DIVIDER:
    def __init__(self,filename,size = None,chuncksize = None):
        self.filename = filename
        if chuncksize == None:
            self.MX_SIZE = MB*100
        else:
            self.MX_SIZE = chuncksize
        if size == None:
            self.SIZE = KB
        else:
            self.SIZE = chuncksize
    def start(self):
        file = open(self.filename,'rb')
        writed = 0
        nfile = 1
        line = file.read(self.SIZE)
        file2 = open(f'{self.filename}{nfile}','wb')
        while line:
            writed += self.SIZE
            file2.write(line)
            line = file.read(self.SIZE)
            if writed >= self.MX_SIZE:
                file2.close()
                writed = 0
                nfile+=1
                file2 = open(f'{self.filename}{nfile}','wb')
        file2.close()

class FILE_JOINER:
    def __init__(self,filename):
        self.filename = filename
    def start(self):
        ofile = open(f'{self.filename}','wb')
        try:
            i = 1
            while True:    
                ifile = open(f'{self.filename}{i}','rb')
                SIZE = MB*10
                line = ifile.read(SIZE)
                while line:
                    ofile.write(line)
                    line = ifile.read(SIZE)
                ifile.close()
                os.remove(f'{self.filename}{i}')
                i+=1
        except Exception as e:
            print('end')
            pass
        finally:
            ofile.close()

