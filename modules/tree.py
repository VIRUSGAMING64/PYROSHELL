import os
class TreeMaker:
    showfiles = 1
    up = "^"
    down = "|"
    left = '>'
    spaces = 3
    trees = ""
    show = True
    def __init__(self) -> None:
        pass
    def end(self,s):
        try:
            k = ""
            for i in range(len(s)-1,-1,-1):
                if(s[i] == '\\' or s[i] == '/'):
                    break
                else:
                    k = s[i] + k
            return k
        except Exception as e:
            print(e)
    def tree(self,dir,prof = 0):
        if(self.show):
            print(' ' * (self.spaces - 1)*prof,end="",sep="")
        else:
            self.trees += ' ' * (self.spaces - 1)*prof
        try:
            os.access(dir,3)
            os.chdir(dir)
            if self.show:
                print(self.end(dir) + " ---D" + "\n",end="")
            else:
                self.trees += self.end(dir) + " ---D" + "\n"
        except Exception as e:  #dir is file
            if self.showfiles == 1:
                if self.show:
                    print(self.end(dir) + " ---F")
                else:
                    self.trees += self.end(dir) + " ---F\n"
            return
        l = os.listdir()
        l.sort()
        lk = 0
        for i in l:
            if i.startswith('.'):
                continue
            try:
                if self.showfiles == False and os.path.isfile(dir):
                    continue
            except Exception as e:
                continue
            os.chdir(dir)
            self.tree(dir + '\\'+i,prof+1)
            for k in range(self.spaces):
                if self.show:
                    print(" "*3*prof,sep="",end="")
                    print(self.down + "\n",sep="",end="")
                else:
                    self.trees += " "*3*prof
                    self.trees +=self.down + "\n"
            if self.show:
                print(" " * prof * 3+self.left * 3,sep="",end="")
            else:
                self.trees += " " * prof * 3 + self.left * 3
            if(lk == len(l)-1):
                if self.show:
                    print( " " +self.up*3)
                else:
                    self.trees += " " + self.up * 3
            lk+=1

tr = TreeMaker()
tr.tree(os.getcwd())