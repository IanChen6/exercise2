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
import sys
# print ("脚本名：", sys.argv[0])
# print(sys.argv[1])
# # for i in range(1, len(sys.argv)):
# #     print ("参数", i, sys.argv[i])
# import random
# import platform
# import time
# sysname=platform.platform()
# a=platform.architecture()
# b=platform.processor()
# d={'name':1,'age':2}
# print(d)
# d.clear()
# print(d)
# sleep_time = [3, 2, 1.5, 2.7, 3.9, 2.5, 3.1, 2.4, 2.8, 2.6]
# start=time.time()
# time.sleep(sleep_time[random.randint(0, 9)])
# end=time.time()
# print(end-start)
# from decimal import *
# b=Decimal('3.40')
# a=str(Decimal('3.40').quantize(Decimal('0.00')))
# print(a)
with open('asset.txt', 'r', encoding='utf8') as f:
    mess = f.read()
    if mess.startswith(u'\ufeff'):
        mess = mess.encode('utf8')[3:].decode('utf8')
    mess = json.loads(mess)
    f.close()
