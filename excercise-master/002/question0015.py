# -*- coding:utf-8 -*-
__author__ = 'IanChen'

''' 纯文本文件 city.txt为城市信息, 里面的内容（包括花括号）如下所示：

{
    "1" : "上海",
    "2" : "北京",
    "3" : "成都"
}
'''

from collections import OrderedDict
import json,xlwt

with open("wenben2.txt",'r') as f:
    data = json.load(f,object_pairs_hook=OrderedDict)#顺序是跟text中定义的顺序是一样的
    workbook=xlwt.Workbook()
    sheet= workbook.add_sheet("city",cell_overwrite_ok=True)
    for index,(key,value) in enumerate(data.items()):
        sheet.write(index,0,key)
        sheet.write(index,1,value)
    workbook.save("F:/excercise/002/table/city.xls")
