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
# "TaxId":"440300692516197",#深圳市隆创盛科技有限公司()
# "TaxPwd":"27930462",
"TaxId":'91440300775551684W',#bote
"TaxPwd":"79066664",
# "TaxId":'440300582721683',#和乐手袋
# "TaxPwd":"84322586",
# "TaxId":'440300782766261',#深圳市清驰科技有限公司()
# "TaxPwd":"79606847",
# "TaxId":'440300081895157',#麦哲伦()
# "TaxPwd":"88272474",
# "TaxId":'440300550321415',#深圳市欧普泰光电有限公司
# "TaxPwd":"hu168",
# "TaxId":'440300680370610',#深圳市皇锐科技有限公司
# "TaxPwd":"81559668",
# "TaxId":'91440300305843121K',#派盟
# "TaxPwd":"000999",
# "TaxId":'440300693952599',#昂迅
# "TaxPwd":"82181715",
# "TaxId":'91440300MA5DCXYE4M',#深圳市快视电子有限公司,缺补亏明细表、16主表、企业基础信息表
# "TaxPwd":"86836800",
# "TaxId":'91440300558679788J',#深圳市蓝景自动化设备有限公司
# "TaxPwd":"620186",
# "TaxId":'44030058156273X',#深圳鸿滔国际贸易有限公司
# "TaxPwd":"84193654",
'jobname':'工程1',
'jobparams':"工作中",
'Type':'CUSTOMERINFO',
# "CustomerName":'深圳市欧迪光电科技有限公司'
          }
# re=requests.post(url="http://120.79.65.131:8080/crawl2local/",data=postdata)
re=requests.post(url="http://127.0.0.1:8000/crawl2local/",data=postdata)
# re=requests.post(url="http://127.0.0.1:8000/local_cc/",data=postdata)
# "http://120.79.65.131:8080/crawl2local/
print(re.text)