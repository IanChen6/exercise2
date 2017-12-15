# -*- coding:utf-8 -*-
import hashlib
import json

# h = hashlib.sha1('83093013'.encode('utf8')).hexdigest()
# print(h)
# 图片上传测试
import requests
import base64

#
with open("国税申报结果截图.png", 'rb') as a:
    upload_url = 'http://39.108.112.203:8687/uploadFile.php'
    data = {'fileType': '.png'}
    files = {"imgfile": a.read()}
    r=requests.post(upload_url,data=data,files=files)
    print(r.text)

# #爬虫post测试：
# # headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
# postdata={"BatchID":45,
# "BatchYear":2016,
# "BatchMonth":48,
# "CompanyID":22,
# "CustomerID":1,
# "TaxId":440300771615767,
# "TaxPwd":83093013}
# requests.post(url="http://120.79.65.131/search-post",data=postdata)


