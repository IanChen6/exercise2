# -*- coding:utf-8 -*-
__author__ = 'IanChen'

#保存到redis数据库
import redis
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
def save_code():
    conn=redis.Redis(host="127.0.0.1",port="6379")
    p=conn.pipeline()
    for i in range(200):
        p.sadd("code",create_code()[i])
    p.execute()
    return conn.scard('code')

if __name__ == "__main__":
    save_code()