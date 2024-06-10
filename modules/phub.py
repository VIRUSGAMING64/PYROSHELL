
import requests as rq
import re as exp
import urllib.request as req
import time
link = "https://es.pornhub.com"

headers = {
    "method":"GET",
    "authority":"es.pornhub.com",
    "scheme":"https",
    "accept":"*/*",
    "Accept-Encoding":"gzip, deflate, br, zstd",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "Referer":"https://es.pornhub.com/",
    "Sec-Ch-Ua":'Brave";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "Sec-Ch-Ua-Platform":"Windows",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}   
porn = []
links = {}

def GetUrls(link):
    txt = rq.get(link,timeout=10,headers=headers).text
    return exp.findall('href="/*.*"',txt)

def Get(link):
    try:
        return links[link]
    except:
        links[link] = 0
        return 0
    
def Put(link):
    links[link] = 1

I = 0

def find(base,link,prof=1):
    global porn,I
    if prof == 100:
        return
    i:str=""
    lk = GetUrls(link)
    for i in lk:
        if i.startswith('href="/channels'):
            d=i.split(" ")
            sub = d[0].removeprefix('href="').removesuffix('"')
            if Get(base + sub) == 0:
                Put(base + sub)
                find(base,base + sub,prof+1)
        elif i.startswith('href="/view'):
            d=i.split(" ")[0].removeprefix('href="').removesuffix('"')
            if Get(base+d)==0:
                Put(base+d)
                porn.append(base+d)    
                I+=1
                print(I)


find(link,link)
file = open("links.txt","w")

for i in porn:
    file.write(i+"\n")