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
#
# from flask import Flask
# from flask import request
#
# app=Flask(__name__)
#
# @app.route('/hello')
# def index():
#     return "Hello World"
#
# @app.route('/method',methods=['GET','POST'])
# def mt():
#     return "Hello World"
#
# if __name__ == "__main__":
#     app.run(debug=True)


# import requests
# from multiprocessing.pool import ThreadPool
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
# postdata = {"BatchID": 45,
#             "BatchYear": 2017,
#             "BatchMonth": 7,
#             "CompanyID": 18282900,
#             "CustomerID": 9,
#             # "TaxId":440300754285743,
#             "TaxId": 440300771615767,
#             "TaxPwd": 83093013,
#             # "TaxPwd":77766683,
#             'jobname': '工程1',
#             'jobparams': "工作中"
#             }
# pool = ThreadPool(processes=20)
#
#
#
# # def sb():
# #     print('开始任务')
# re = requests.post(url="http://120.79.65.131:8000/search-post", data=postdata, timeout=200)
# print(re.text)
# #     sys.exit()
#
#
# # re = requests.post(url="http://127.0.0.1:8000/search-post", data=postdata)
# # a = 0
# # while a < 100:
# #     a += 1
# #     pool.apply_async(sb)
# # print('over')
# # pool.close()
# # pool.join()
#
# from pdfminer.converter import PDFPageAggregator
# from pdfminer.layout import LTTextBoxHorizontal, LAParams
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
# from pdfminer.pdfparser import PDFParser, PDFDocument
#
# fp = open("pdfparse.pdf", "rb")
#
# # 用文件对象创建一个pdf文档分析器
# parse_pdf = PDFParser(fp)
#
# # 创建一个PDF文档
# doc = PDFDocument()
#
# parse_pdf.set_document(doc)
# doc.set_parser(parse_pdf)
#
# doc.initialize()
#
# # 检测文档是否提供txt转换，不提供就忽略
# if not doc.is_extractable:
#     raise PDFTextExtractionNotAllowed
# else:
#     # 创建PDf资源管理器 来管理共享资源
#     rsrcmgr = PDFResourceManager()
#
#     # 创建一个PDF参数分析器
#     laparams = LAParams()
#
#     # 创建聚合器
#     device = PDFPageAggregator(rsrcmgr, laparams=laparams)
#
#     # 创建一个PDF页面解释器对象
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#
#     # 循环遍历列表，每次处理一页的内容
#     # doc.get_pages() 获取page列表
#     for page in doc.get_pages():
#         # 使用页面解释器来读取
#         interpreter.process_page(page)
#
#         # 使用聚合器获取内容
#         layout = device.get_result()
#
#         results_last=""
#         # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
#         for out in layout:
#             # 判断是否含有get_text()方法，图片之类的就没有
#             # if hasattr(out,"get_text"):
#             if isinstance(out, LTTextBoxHorizontal):
#                 results = out.get_text()
#                 if results_last=="税（费）种\n":
#                     print("results: " + results)
#
#                     sz = results.strip("").split("\n")
#                     print(sz)
#                 if "7=5×6" in results:
#                     print("results: " + results)
#                     jn=results.strip("").split("\n")
#                     jn.pop(0)
#                     print(jn)
#                 results_last=results
# pdf_dict={}
# for i in range(len(sz)-3):
#     pdf_dict[sz[i]]=jn[i]
# print(pdf_dict)
# import json
# js=json.dumps({"1":"abc","b":"3323d"})
# js=json.loads(js)
# dm=js.copy()
# dm.update(pdf_dict)
# print(dm)
# ll=tuple(dm.items())
# print(ll)
# pdfjson=json.dumps(dm,ensure_ascii=False)
# print(pdfjson)
#
# s='\xa0\n     1693\n    '
# out="".join(s.strip())
# print(out)


# import os
# if  not os.path.exists("dishui/aa"):
#     os.mkdir('dishui/aa')
import requests
# #国税、地税申报信息
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
postdata={"BatchID":10298,
"BatchYear":2017,
"BatchMonth":1,
"CompanyID":18282900,
"CustomerID":9,
# "TaxId":440300754285743,
# "TaxPwd":77766683,
"TaxId":'91440300MA5DFMBMXU',
"TaxPwd":"741258",
'jobname':'工程1',
'jobparams':"工作中",
'Type':'TAXDATA',
      'JobExtend':'aaa'
          }
re=requests.post(url="http://120.79.65.131:8000/spider/",data=postdata)
# re=requests.post(url="http://127.0.0.1:8000/spider/",data=postdata)
# re=requests.post(url="http://120.79.65.131:8000/cancel/",data=postdata)
# re=requests.post(url="http://127.0.0.1:8000/cancel/",data=postdata)
print(re.text)

#发票信息汇总
# headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
# postdata={"BatchID":5590,
# "BatchYear":2018,
# "BatchMonth":1,
# "CompanyID":18282900,
# "CustomerID":9,
# # "TaxId":440300754285743,
# # "TaxPwd":77766683,
# "TaxId":'9144030008389925X7',
# "TaxPwd":"y20170410",
# 'jobname':'工程1',
# 'jobparams':"工作中",
# 'Type':'CUSTOMERINVOICE'
#           }
# # re=requests.post(url="http://120.79.65.131:8000/spider/",data=postdata)
# re=requests.post(url="http://127.0.0.1:8000/spider/",data=postdata)
# print(re.text)

#自动申报
# headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
# postdata={"BatchID":1285,
# "BatchYear":2018,
# "BatchMonth":1,
# "CompanyID":18282900,
# "CustomerID":9,
# # "TaxId":440300754285743,
# # "TaxPwd":77766683,
# "TaxId":'9144030008389925X7',
# "TaxPwd":"y20170410",
# 'jobname':'工程1',
# 'jobparams':"工作中",
# 'Type':'TAXAPPLYNORMAL',
# 'fw1':"0.00",
# 'fw2':"0.00",
# 'hw1':"0.00",
# 'hw2':"174764.08",
# 'fwms':"0.00",
# 'hwms':"0.00",
# 'fwyj':"0.00",
# 'hwyj':"5242.92",
# 'djzs':"0.00",
# 'dfzs':"0.00",
# 'dczs':"0.00",
# 'djms':"0.00",
# 'dfms':"0.00",
# 'dcms':"0.00"
#           }
# # re=requests.post(url="http://120.79.65.131:8000/spider/",data=postdata)
# # re=requests.post(url="http://127.0.0.1:8000/cancel/",data=postdata)
# re=requests.post(url="http://127.0.0.1:8000/spider/",data=postdata)
# print(re.text)
#完善公司信息
# headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
# postdata={
#     "BatchID":'0116f9940108d588fca3040839',
# "BatchYear":2018,
# "BatchMonth":1,
# "CompanyID":18282900,
# "CustomerID":9,
# # "TaxId":440300754285743,
# # "TaxPwd":77766683,
# "CustomerName":'深圳市九十九维信息咨询有限公司',
# "TaxId":'440300683771524',
# "TaxPwd":"xdh123456",
# 'jobname':'工程1',
# 'jobparams':"工作中",
# 'Type':'CUSTOMERINFO',
# # 'bathcancel':[["0116f9940108d588fca2df60a6","0116f9940108d588fca2f25938","0116f9940108d588fca3040839","0116f9940108d588fca312db59","0116f9940108d588fca31f8e73","0116f9940108d588fca32c418a","0116f9940108d588fca339f049","0116f9940108d588fca34819ec","0116f9940108d588fca3548cbf","0116f9940108d588fca35fb7f5","0116f9940108d588fca36cac59","0116f9940108d588fca378b529","0116f9940108d588fca3867ab8","0116f9940108d588fca394aa00","0116f9940108d588fca3a3d0ef","0116f9940108d588fca3b1d223","0116f9940108d588fca3be5ded","0116f9940108d588fca3cb9ab5","0116f9940108d588fca3d939f4","0116f9940108d588fca3e7c2db","0116f9940108d588fca3f70fe4","0116f9940108d588fca40480fe","0116f9940108d588fca411aa87","0116f9940108d588fca41dfd74","0116f9940108d588fca42bb57a","0116f9940108d588fca438699f","0116f9940108d588fca449370c","0116f9940108d588fca45638ce","0116f9940108d588fca46275fc","0116f9940108d588fca46f9f30","0116f9940108d588fca4804bef"]]
#           }
# re=requests.post(url="http://120.79.65.131:8000/spider/",data=postdata)
# # re=requests.post(url="http://127.0.0.1:8000/spider/",data=postdata)
# # re=requests.post(url="http://127.0.0.1:8000/cancel/",data=postdata)
# print(re.text)
#代开发票
# headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
# postdata={"BatchID":5590,
# "BatchYear":2018,
# "BatchMonth":1,
# "CompanyID":18282900,
# "CustomerID":9,
# # "TaxId":440300754285743,
# # "TaxPwd":77766683,
# "TaxId":'9144030008389925X7',
# "TaxPwd":"y20170410",
# 'jobname':'工程1',
# 'jobparams':"工作中",
# 'Type':'TAXINVOICE'
#           }
# # re=requests.post(url="http://120.79.65.131:8000/spider/",data=postdata)
# re=requests.post(url="http://127.0.0.1:8000/spider/",data=postdata)
# print(re.text)


# captcha_url = 'http://dzswj.szgs.gov.cn/tipCaptcha?0.9322011782378214'
# res = requests.get(url=captcha_url).json()
# image = res['image']
# image="data:image/jpg;base64,"+image
# tip=res["tipMessage"]

# post_data = {"a": 1, "b": image}
# post_data = json.dumps({"a": 1, "b": image})
# res = requests.post(url="http://39.108.112.203:8002/mycode.ashx", data=post_data, timeout=30)
# print(res.text)


