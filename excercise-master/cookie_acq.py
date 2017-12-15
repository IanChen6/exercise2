# -*- coding:utf-8 -*-
__author__ = 'IanChen'

import requests
import re

session = requests.session()
url = "https://www.jufaanli.com/search2?TypeKey=1%3A%E5%AE%89%E6%85%B0"
# session.get(url)

resp = requests.get(url)
print(resp.cookies._cookies['.jufaanli.com']['/']['BJYSESSION'])
print(type(resp.cookies._cookies['.jufaanli.com']['/']['BJYSESSION']))
# resp.cookies._cookies[0][0]
c=re.findall(r'BJYSESSION=',resp.cookies._cookies[0][0])
# print(c.group(1))
# print(resp.request._cookies._cookies)
