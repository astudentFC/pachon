import requests
from bs4 import BeautifulSoup
import time
html_cainiao="https://www.runoob.com/css/css-tutorial.html"
re=requests.get(html_cainiao)
bea=BeautifulSoup(re.text,'html.parser')
child_html_list=bea.find("div",class_="design")
child_html=child_html_list.find_all("a",target="_top")

i=0
html_dict={}
for html_over10 in child_html:
    if i<20:
        html_dict[html_over10['title']]=html_cainiao+html_over10['href']
        i+=1
for html in html_dict:
    childRequest=requests.get(html_dict[html])
    html_str=childRequest.text
    with open ("{}.html".format(html),"w",encoding="utf-8") as htm:
        html_str_new=html_str.replace("/wp-content/themes/runoob/style.css?v=1.156","css.css")
        htm.write(html_str_new)
    time.sleep(1)
