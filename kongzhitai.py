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
# with open('asset.txt', 'r', encoding='utf8') as f:
#     mess = f.read()
#     if mess.startswith(u'\ufeff'):
#         mess = mess.encode('utf8')[3:].decode('utf8')
#     mess = json.loads(mess)
#     for i in mess:
#         data=i.values()
#         # data=data[0]
#         print(data)
#         pass
#     f.close()
# a=[1,2,3,4,5,6,7,8,9,10,11]
# def isplit_by_n(ls, n):
#     for i in range(0, len(ls), n):
#         yield ls[i:i+n]
#
# def split_by_n(ls, n):
#     return list(isplit_by_n(ls, n))
#
# a=split_by_n([1,2,3,4,5,6,7,8,9,10],2)
# pass
a='执行事务合伙人:西安地坤:投资:管理有限公司'
l=a.split(":")
print(l)