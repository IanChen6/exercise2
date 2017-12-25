# -*- coding:utf-8 -*-
import hashlib
import json

# h = hashlib.sha1('83093013'.encode('utf8')).hexdigest()
# print(h)
# 图片上传测试
import requests
import base64
import re
#
# with open("国税申报表截图142.png", 'rb') as a:
#     upload_url = 'http://39.108.112.203:8687/uploadFile.php'
#     data = {'fileType': '.png'}
#     files = {"imgfile": a.read()}
#     r = requests.post(upload_url, data=data, files=files)
#     imgname = re.search(r'filePath":"(.*?)"', r.text)
#     imgname = imgname.group(1)
#     print(imgname)


# #爬虫post测试：
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
postdata={"BatchID":45,
"BatchYear":2017,
"BatchMonth":1,
"CompanyID":18282900,
"CustomerID":9,
# "TaxId":440300754285743,
"TaxId":440300771615767,
"TaxPwd":83093013,

# "TaxPwd":77766683,
'jobname':'工程1',
'jobparams':"工作中"
          }
re=requests.post(url="http://120.79.65.131:8000/search-post",data=postdata)
# re=requests.post(url="http://127.0.0.1:8000/search-post",data=postdata)
print(re.text)

# import time
# str=time.strftime('%Y-%m-%d', time.localtime())
# print(str)
# print(type(str))

# split()测试
# str="国税申报结果截图.png"
# split=str.split('.')
# print(split[1])
# if split[1]=='png':
#     print('true')

# import calendar
# monthRange = calendar.monthrange(2017,12)
# print(monthRange)
# print(monthRange[1])
# for i in range(1,13):
#     print(i)

import json
# a=[1,2,4,6]
# r = {}
# for i in range(len(a)):
#
#     r["{}".format(i)]=a[i]
# print(r)
# c=json.loads(b)
# print(c)
# d=[8,9,10]
# f=a+d
# print(f)

#
# from selenium import webdriver
#
# browser = webdriver.PhantomJS(executable_path='D:/BaiduNetdiskDownload/phantomjs-2.1.1-windows/bin/phantomjs.exe')
# browser.get("https://zhidao.baidu.com/question/1694533052778979748.html")
# handle=browser.current_window_handle
# newwindow = 'window.open("https://www.baidu.com");'
# browser.execute_script(newwindow)
# handles = browser.window_handles
# browser.switch_to_window(handles[-1])
# browser.s
# handle2=browser.current_window_handle
# print(handle2)
# print(handle)
#
# print(handles)