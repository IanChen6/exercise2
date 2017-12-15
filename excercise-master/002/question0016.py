# -*- coding:utf-8 -*-
__author__ = 'IanChen'

''' 纯文本文件 city.txt为城市信息, 里面的内容（包括花括号）如下所示：

[
	[1, 82, 65535], 
	[20, 90, 13],
	[26, 809, 1024]
]
'''

from collections import OrderedDict
import json,xlwt

with open("wenben3.txt",'r') as f:
    data = json.load(f)#顺序是跟text中定义的顺序是一样的
    workbook=xlwt.Workbook()
    sheet= workbook.add_sheet("numbers",cell_overwrite_ok=True)
    for index,t in enumerate(data):
        for index2,value in enumerate(t):
            sheet.write(index,index2,value)

    workbook.save("F:/excercise/002/table/numbers.xls")
