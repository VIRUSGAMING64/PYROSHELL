from datatypes import *
import Gvar
import os


class MAIN:
    FILE = Gvar.ROOT + "datas.V"
    OFILE = None

    def __init__(self):
        try:
            F = open(self.FILE, "r")
            MEM = ""
            while 1:
                D = F.read(65536)
                if D:
                    MEM += D
                else:
                    break
            MEM = MEM.split("\n")
            for i in MEM:
                Gvar.DATA.append(i.split(" "))
            F.close()
            for i in range(len(Gvar.DATA)):
                for j in range(2, len(Gvar.DATA[i])):
                    if str(Gvar.DATA[i][j]).isnumeric():
                        Gvar.DATA[i][j] = int(Gvar.DATA[i][j])
                        pass
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
