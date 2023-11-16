from modules.datatypes import *
import modules.Gvar as Gvar
import os
def debug(e):
    _debug = open("debug-env.txt","a")
    _debug.write(str(e) + "\n")
    _debug.close()




class MAIN:
    FILE = Gvar.ROOT + "datas.V"
    OFILE = None
    def __init__(self):
        try:
            F = open(self.FILE, "r")
            MEM = ""
            while 1:
                D = F.read(1024 * 1024)
                if D:
                    MEM += D
                else:
                    break
            F.close()
            MEM = MEM.split("\n")
            for i in MEM:
                Gvar.DATA.append(i.split(" "))
            for i in range(len(Gvar.DATA)):
                for j in range(2, len(Gvar.DATA[i])):
                    if str(Gvar.DATA[i][j]).isnumeric():
                        Gvar.DATA[i][j] = int(Gvar.DATA[i][j])
                        pass
            for i in range(len(Gvar.DATA)):
                while len(Gvar.DATA[i]) < Gvar.USER_VARIABLES:
                    Gvar.DATA[i].append(0)
            self.save()
        except Exception as e:
            print(e)
            pass

    def save(self):
        self.OFILE = open(self.FILE, "w")
        i = 0
        j = 0
        for USER_DATA in Gvar.DATA:
            for ARG in USER_DATA:
                A = str(ARG)
                if j != len(USER_DATA) - 1:
                    A += " "
                self.OFILE.write(A)
                j += 1
            if i != len(Gvar.DATA) - 1:
                self.OFILE.write("\n")
            i += 1
        self.OFILE.close()
        pass
