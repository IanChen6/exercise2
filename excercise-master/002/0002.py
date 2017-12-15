# -*- coding:utf-8 -*-
__author__ = 'IanChen'

#将 0001 题生成的 200 个激活码（或者优惠券）保存到 MySQL 关系型数据库中。

import pymysql
import sys

# sys.path.append(r"F:\\excercise\question1")#文件名不用用数字
# from question1 import ...
import uuid


def create_code(number=200):
    result = []
    while True is True:
        temp = str(uuid.uuid1()).replace('-', '')
        if not temp in result:
            result.append(temp)
        if len(result) is number:
            break
    return result
def insert_code(code):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1029384756', db='exercise',
                                use_unicode=True, charset="utf8")
    cursor = conn.cursor()
    cursor.execute('''
        insert into showmethecode(code) VALUES (%s)
        ''',code)
    conn.commit()

if __name__ == "__main__":
    result=create_code()
    for i in range(200):
        insert_code(result[i])


