from pyrogram.client import *
import modules.Gvar as Gvar
import os
import tarfile as tar

def SetZero(i:int):
    s = str(i)
    if len(s) == 1:
        s = '000'+s
    elif len(s) == 2:
        s = "00"+s
    elif len(s) == 3:
        s = "0"+s
    return s

def DirToTar(dirname):
    file=tar.TarFile(dirname+".001","w")
    file.add(dirname)
    file.close()
    return dirname + ".001"

def Compress(filename,MAX_Z = 2000*Gvar.MB):
    id = 1
    fid = 1
    file = open(filename,"rb")
    ch_file = open(filename + ".001","wb")
    chunk = file.read(Gvar.MB)
    files = [filename + ".001"]
    while chunk:
        ch_file.write(chunk)
        chunk = file.read(Gvar.MB)
        if id % (MAX_Z // Gvar.MB) == 0:
            fid += 1
            ch_file.close()
            ch_file = open(filename+ "." + SetZero(fid),"wb")
            files.append(filename + "." + SetZero(fid))
        id = id+1
    ch_file.close()
    file.close()
    os.remove(filename)
    return files

def SendFile(chatID,filename,bot:Client,progress:Callable = None,args = None,thumb = None):
    try:
        if os.path.isdir(filename):
            filename = DirToTar(filename)
        size = os.path.getsize(filename)
        files = [filename]
        if size > Gvar.MB * 2000:
            files = Compress(filename)
        file:str =""
        for file in files:
            if file.endswith(".mp4") or file.endswith(".mpg") or file.endswith('.mkv'):
                bot.send_video(chatID,file,progress=progress,progress_args=args,thumb=thumb)
            elif file.endswith(".jpg") or file.endswith(".png"):
                bot.send_photo(chatID,file,progress=progress,progress_args=args,thumb=thumb)
            else:
                bot.send_document(chatID,file,progress=progress,progress_args=args,thumb=thumb)
    except Exception as e:
        return str(e)
