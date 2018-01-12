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
# import json
#
import requests

headers ={
'Cookie': 'tgw_l7_route=41b5a189c640d63f085c449f4ffcdefa; JSESSIONID=B6532D82A9CE05A4DBD28CCA3A5D1A57; DZSWJ_TGC=5a7fdd5ccdff4cc5b3137f1706f87554; CNZXDATA="QTJCM0ExQTc5MjAwQ0EzRTYxNUZBMTFBQjMyM0RBMzVBQUExODU2NUVGNUQyQTBEMzkyMjFCM0QxQzVGOTY0NDcxNTlCNUNFOTREM0U2REEyQjlBNTBGMUM2RjA2MEIwQTM2ODE0MjIyRTE5MjRBMUFFMUFENDk4REIwNjc0ODU="',
'Origin': 'http://dzswj.szgs.gov.cn',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
'Content-Type':'application/json; charset=UTF-8',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Referer': 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
'X-Requested-With':'XMLHttpRequest',
'Connection': 'keep-alive',
'x-form-id': 'mobile-signin-form'}
url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
data = '{"nsrsbh":"91440300MA5DRRFB45","nsrpwd":"71dd2b1e769b6aebd8ea41aa5dd5b6e55306819f","tagger":"[{\\"x\\":267,\\"y\\":73},{\\"x\\":173,\\"y\\":24},{\\"x\\":217,\\"y\\":81}]","redirectURL":"","time":"2018-01-11 11:37:25"}'
resp = requests.post(url=url, headers=headers, data=data)
#[{\"x\":264,\"y\":48},{\"x\":65,\"y\":83},{\"x\":220,\"y\":101}]
# data='[{"x":264,"y":48},{"x":65,"y":83},{"x":220,"y":101}]'
# jyjg=requests.post(url='http://dzswj.szgs.gov.cn/api/checkClickTipCaptcha',data=data)
pass
#
# s=r'[{\"x\":25,\"y\":50},{\"x\":128,\"y\":57},{\"x\":275,\"y\":107}]'
# # s=json.dumps(s,ensure_ascii=False)
# # 107s.replace('"','\/"')
#
# print(s)