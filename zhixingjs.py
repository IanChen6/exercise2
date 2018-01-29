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
import json

from selenium import webdriver

# browser = webdriver.Chrome(executable_path='D:/BaiduNetdiskDownload/chromedriver.exe')
# browser.get('https://www.baidu.com')
# browser.execute_script(
#     "var xmlhttp=new XMLHttpRequest();\n" + "xmlhttp.open(\"GET\",\"https://www.baidu.com\",false);\n" + "xmlHttp.setRequestHeader(\"Content-type\",\"application/x-www-form-urlencoded\");\n" +  # 表单提交的头部信息
#     "xmlhttp.setRequestHeader(\"testHeader\",\"123456\");\n" +  # 自定义请求头
#     "xmlhttp.send(\"name=test&sex=1&age=18\");\n" +  # 表单数据
#     "return xmlhttp.responseText;")

# ml=['\n\t\t\t\t\t\t', '纳税人名称：\xa0', '\n\t\t\t\t\t\t', '\xa0深圳市一新防腐技术有限公司\n\t\t\t\t\t\t', '\n\t\t\t\t\t\t', '纳税人识别号：\xa0', '\n\t\t\t\t\t\t', '\xa0440300788330637\n\t\t\t\t\t\t', '\n\t\t\t\t\t']
# print(ml)
# l=map(lambda x: x.strip(), ml)
# l=list(l)
# print(l)
# fl=list(filter(lambda x:x.strip(),l))
# print(fl)
import redis
redis_cli = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

xinyong_dict = {"1": '深圳市自主鲜果蔬饮品有限公司西乡天虹分公司', "2": '', "3": '123456', "4": 18282900,
                "5": 89, "6": '1111', "7": '22222', "8": '33333'}
pjson = json.dumps(xinyong_dict,ensure_ascii=False)
redis_cli.lpush("gongshang", pjson)

