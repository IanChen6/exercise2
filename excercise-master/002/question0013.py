# -*- coding:utf-8 -*-
__author__ = 'IanChen'

# 用 Python 写一个爬图片的程序，爬 这个链接里的日本妹子图片 :-)[http://tieba.baidu.com/p/2166231880]

import os
import requests
from bs4 import BeautifulSoup

url="http://tieba.baidu.com/p/2166231880"
html=requests.get(url)
soup = BeautifulSoup(html.text,"html.parser")#读取HTML标签
img_urls = soup.findAll("img",bdwater="杉本有美吧,1280,860")#通过img标签属性搜索标签，寻找bdwater=“。。。”
# 的标记，返回一个结果集
for img_url in img_urls:
    img_src=img_url["src"]
    a=os.path.split(img_src)[0]
    save_path=os.path.split(img_src)[1]#将目录和文件分割，返回一个tuple
    with open("F:/excercise/002/image/"+os.path.split(img_src)[1],"wb") as f:
        f.write(requests.get(img_src).content)