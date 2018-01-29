# -*- coding:utf-8 -*-
__author__ = 'IanChen'

# import sys
# sys.path.extend("D:\\新建文件夹\excercise-master\excercise-master\log_ging")

import os

# print(os.path.abspath(__file__))
# print(os.path.dirname(os.path.realpath(__file__)))
#
# user="abcdefg"
# if not os.path.exists('./{}'.format(user)):
#     os.mkdir('./{}'.format(user))
#
# with open('cookies/{}cookies.json'.format("a"), 'w') as f:  # 将login后的cookies提取出来
#     f.write("123")
#     f.close()
#
# print(os.path.basename(__file__))
# aa=sys.argv[0]
# p=os.path.dirname(sys.argv[0]).split('/')[-1]
# print(p)

# import collections
# d={'1':123,"13":4,"12":245,'10':99}
# dd=collections.OrderedDict(sorted(d.items(),key=lambda t:t[0]))
# print(dd)

# import redis#
# redis_cli = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
# a=redis_cli.lrange('szgslist',0,-1)
# print(a)
# for i in a:
#     if "456" in i:
#         redis_cli.lrem('szgslist',1,i)

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

# dcap = dict(DesiredCapabilities.PHANTOMJS)
# dcap["phantomjs.page.settings.userAgent"] = (
#     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
# dcap["phantomjs.page.settings.loadImages"] = True
# service_args = []
# service_args.append('--webdriver=szgs')
# browser = webdriver.PhantomJS(
#     executable_path='D:/BaiduNetdiskDownload/phantomjs-2.1.1-windows/bin/phantomjs.exe',
#     desired_capabilities=dcap, service_args=service_args)
# # browser = webdriver.PhantomJS(
# #     executable_path='/home/tool/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',
# #     desired_capabilities=dcap)
browser = webdriver.Chrome(executable_path='D:/BaiduNetdiskDownload/chromedriver.exe')
browser.get("https://www.baidu.com/")
a=browser.title
browser.execute_script('document.title="123456"')
b=browser.title
newwindow='window.open("https://www.baidu.com/")'
browser.execute_script(newwindow)
browser.execute_script(newwindow)
browser.execute_script(newwindow)

pass


