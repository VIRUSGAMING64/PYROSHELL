from datatypes import *
import Gvar as Gvar
class CSV:
    data = []
    locate = ""
    def __init__(self,file:str=Gvar.ROOT+"/user_datas.csv"):   
        self.load(file)
    def load(self,file:str = Gvar.ROOT+"/user_datas.csv"):
        self.locate = file
        file = open(file,"r")
        data = file.read(Gvar.GB)
        data = data.split("\n")
        for i in range(len(data)):
            data[i] = data[i].split(' ')
        self.data = data
        file.close()
    def save(self):
        file = open(self.locate,"w")
        it = 0
        for usr in self.data:
            for data in usr:
                file.write(data + " ")
            if(it != len(self.data)-1):
                file.write("\n") 
            it+=1
        file.close()
    def find(self,id:int | str): # O(n) -> with tree change to -> O(log(n)) #TODO
        for i in range(len(self.data)):
            if(self.data[i][USER_ID] == id):
                return i
        return -1
    def find(self,usr:list): # O(n) -> with tree change to -> O(log(n)) #TODO
        for i in range(len(self.data)):
            if(self.data[i] == usr):
                return i
        return -1
    def append(self,usr:[]):
        return self.data.append(usr)
    def erase(self,pos):
        return self.data.pop(pos)
    def reload(self):
        self.load(self.locate)
    def sort(self):
        return self.data.sort()