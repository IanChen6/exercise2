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
from suds.client import Client
import suds
import json
import requests
import re

client = suds.client.Client(url="http://120.79.184.213:8023/yzmmove.asmx?wsdl")
# x_locate = client.service.GetTackXForDll(image_url,y_locte)
track=client.service.GetTacketForDll()
ticket=json.loads(track)["ticket"]
print(ticket)
pass