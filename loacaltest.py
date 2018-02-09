# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     
   Description :
   Author :       ianchen
   date：          
-------------------------------------------------
   Change Activity:
                   2017/11/22:
-------------------------------------------------
"""
#完善公司信息
import requests

headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
postdata={"BatchID":5590,
"BatchYear":2018,
"BatchMonth":1,
"CompanyID":18282900,
"CustomerID":9,
# "TaxId":440300754285743,
# "TaxPwd":77766683,
"TaxId":'91440300MA5DJ3NT34',
"TaxPwd":"10047063",
'jobname':'工程1',
'jobparams':"工作中",
'Type':'CUSTOMERINFO'
          }
# re=requests.post(url="http://120.79.65.131:8080/crawl2local/",data=postdata)
re=requests.post(url="http://127.0.0.1:8000/crawl2local/",data=postdata)
# "http://120.79.65.131:8080/crawl2local/
print(re.text)