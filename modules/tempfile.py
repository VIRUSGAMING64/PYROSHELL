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
