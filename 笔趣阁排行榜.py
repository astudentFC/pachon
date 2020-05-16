import requests
from bs4 import BeautifulSoup

def xuanbang1(zongbang):# todo 选择三榜之一，返回选榜网页
    sanbang=zongbang[0].find_all("a")
    url_zong=[]
    i=1
    for bang in sanbang:
        print("{}、{}".format(i,bang['title']))
        i+=1
        url_zong.append("https://www.52bqg.com{}".format(bang['href']))
    xuanBang_input=int(input("请选择：（输入序号）"))
    url1=url_zong[xuanBang_input-1]
    return url1

def banglei(url1):
    re1=requests.get(url1)
    bea1=BeautifulSoup(re1.text,"html.parser")
    mulu_turtle=bea.find("div",id="main")
    zongbang_turle=mulu.find_all("table")
    for num in range(1,9):
        print(zongbang_turle[num].find("span",class_='btitle').text)
        mingDan_zong=zongbang_turle[num].find_all("li")
        i=1
        for mingDan in mingDan_zong:
            name=mingDan.find("a")['title']
            name_url=mingDan.find("a")['href']
            print("\t{:<2}、{:<20}{}".format(i,name,name_url))
            i+=1

re=requests.get("https://www.52bqg.com/paihangbang/")
re.encoding="gbk"
bea=BeautifulSoup(re.text,"html.parser")
mulu=bea.find("div",id="main")
zongbang=mulu.find_all("table")
url1=xuanbang1(zongbang)
print(url1)
banglei(url1)




