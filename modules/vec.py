import hashlib as hash
import os
try:
    os.mkdir("data")
except:
    pass
class vec:
    dev = 0
    def __init__(self,name:str = "vec") -> None:
        self.name = name
        try:
            os.mkdir(name)
        except Exception as e:
            pass
    def __getitem__(self,index):
        st = "0"
        index = hash.sha512(str(index).encode()).hexdigest()
        pos = f"{self.name}/{index}"
        try:
            dt = open(pos,"r")
            line = dt.read(1024**2)
            st = ''
            while line:
                st += line
                line = dt.read(1024**2)
            dt.close()
        except Exception as e:
            if self.dev:
                print(e)
            file = open(pos,"w")
            file.write("0")
            file.close()
        if st.isnumeric():
            st = int(st)
        return st
    def __setitem__(self,index,val):
        try:
            index = hash.sha512(str(index).encode()).hexdigest()
            pos = f"{self.name}/{index}"
            file = open(pos,"w")
            file.write(str(val))
            file.close()
        except Exception as e:
            if self.dev:
                print(e)
    def pop(self,index):
        index = hash.sha512(str(index).encode()).hexdigest()
        pos = f"{self.name}/{index}"
        os.remove(pos)
    def sort(self):
        d = os.listdir(f"{self.name}")
        print(d)
        pass
