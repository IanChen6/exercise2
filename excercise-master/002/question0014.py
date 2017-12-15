# -*- coding:utf-8 -*-
__author__ = 'IanChen'

''' 纯文本文件 student.txt为学生信息, 里面的内容（包括花括号）如下所示：

{
	"1":["张三",150,120,100],
	"2":["李四",90,99,95],
	"3":["王五",60,66,68]
}
请将上述内容写到 student.xls 文件中，如下图所示：
'''

from collections import OrderedDict
import json,xlwt

with open("文本文件.txt",'r') as f:
    data = json.load(f,object_pairs_hook=OrderedDict)#顺序是跟text中定义的顺序是一样的
    workbook=xlwt.Workbook()
    sheet= workbook.add_sheet("stundent",cell_overwrite_ok=True)
    for index,(key,values) in enumerate(data.items()):
        sheet.write(index,0,key)
        for i,value in enumerate(values):
            sheet.write(index,i+1,value)
    workbook.save("F:/excercise/002/table/student.xls")
