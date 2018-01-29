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
import hashlib
import json
from suds.client import Client
import suds
a="账号和密码不匹配"
js=json.dumps(a,ensure_ascii=False)
if "账号和密码不匹配"in js:
    print("pp")
