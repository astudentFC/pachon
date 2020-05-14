#代码核心：附件邮件发送，协程，request爬虫
from gevent import monkey#协程
monkey.patch_all()#变为协作式运行，即异步
import smtplib,email
import time,schedule#定时


from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests,gevent
from bs4 import BeautifulSoup
from gevent.queue import Queue

msg= MIMEMultipart('related')#多形态


def fangwen(url):
    res=requests.get(url)
    bea=BeautifulSoup(res.text,'html.parser')
    return bea


def zongbiao(lis):
    listh3={}#总表菜单载体
    for lk in lis:
        h3=lk.find('a')
        if  'Tag' in str(type(h3)):
            listh3[h3.text]=h3['href']#单页总列表
    print(listh3)
    return listh3#dic，总菜单


def danribiao(li,listh3):
    n=0#单日跟新系数
    listh2={}#单日菜单载体
    for l in li:#最新日期
        if l==li[0]:
            data=l.text
            n+=1
    print(data)

    for listhn in listh3:#打印单日最新
        if n>0:
            listh2[listhn]=listh3[listhn]#总列表截取最新日列表
            n=n-1
    print(listh2)
    return listh2


def get_piclist(msg,listh2):
    piclist=[]#单日图片载体0
    biaoqianlist=[]
    for danye_url in listh2:
        danye_bea=fangwen(listh2[danye_url])
        items=danye_bea.find('div',class_='entry')
        item2=items.find_all('img')#目录下所有图片
        biaoqians=items.find_all('p')
        for item in item2:
            piclist.append(item['src'])#分两次获得图片具向位置
        del piclist[-2:]#把两次结尾处广告去除
        if len(biaoqianlist)>=9:
            for biaoqiann in biaoqians:
                biaoqianlist.append(biaoqiann.text)
            biaoqian=biaoqianlist[9]#从所有p下信息获得固定位置标签
            msgbiaoqian=MIMEText(biaoqian,'plain','utf-8')
            msg.attach(msgbiaoqian)
            print(biaoqian)
    print('图片数量：{}'.format(len(piclist)))
    return piclist  #true总图
def pic_down_email(piclist,msg):#图片下载与写入
    num=1
    i=0

    for url in piclist:
        with open('第{}张.jpg'.format(num),'wb+') as ph:
            h5=requests.get(piclist[i])
            ph.write(h5.content)
            i+=1
            num+=1
    for n in range(1,num):
        f=open('第{}张.jpg'.format(n),'rb')
        msgi=MIMEImage(f.read())
        msgi.add_header('Content-Disposition', 'attachment', filename='image{}.jpg'.format(n))
        msg.attach(msgi)
    return pic_duilie


def xiechen(msg,httpduilie):
    piclist=get_piclist(msg,httpduilie)
    pic_duilie=pic_down_email(piclist,msg)
    print("完成一个")



bea=fangwen('http://acg17.com/category/meitu/')#美图（总页）
#要素提取
lis=bea.find('div',class_="post-listing archive-box")#全部列表
li=lis.find_all('span',class_='tie-date')#日期提取
listh3=zongbiao(lis)
listh2=danribiao(li,listh3)

pic_duilie=Queue()
piclist =get_piclist(msg,pic_duilie)
for i in range(len(piclist)):
    pic_duilie.put_nowait(piclist[i])
print(pic_duilie)
print('爬虫数量：{}'.format(len(piclist)))

tasks_list=[]#任务列表
for i in range(len(piclist)):
    task=gevent.spawn(xiechen(msg,pic_duilie))
    tasks_list.append(task)
gevent.joinall(tasks_list)


toname=input("请输入你的qq号：")+"@qq.com"
username='287493629@qq.com'#
password='xcbxjiocyykrcabh'#协议权限码
server=smtplib.SMTP_SSL('smtp.qq.com',465)#注释协议,smtp地址和端口
server.login(username,password)#登录
server.sendmail(username,toname,msg.as_string())#发送邮箱
server.quit()

'''schedule.every().day.at("13:53").do(job)#时间检测


while True:
    schedule.run_pending()    
    time.sleep(60)'''
