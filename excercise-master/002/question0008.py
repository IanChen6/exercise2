# -*- coding:utf-8 -*-
__author__ = 'IanChen'

# 第 0008 题：一个HTML文件，找出里面的正文。

import re,requests
from bs4 import BeautifulSoup

url = "http://python.jobbole.com/85231/"
data=requests.get(url)
r=re.findall('<body>[\s\S]*</body>',data.text)
# print(r[0])

print("..................................\n ................")
soup=BeautifulSoup(data.text,"html.parser")
print(soup.body.text)