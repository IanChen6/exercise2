# -*- coding:utf-8 -*-
__author__ = 'IanChen'

import pymongo


conn=pymongo.MongoClient('127.0.0.1',27017)
db=conn.test#连接test数据库，没有则自动创建
my_set=db.test_set#使用test_set集合，没有则自动创建
my_set.insert({"name":"zhangsan","age":18})#插入单条数据
#插入多条数据
users=[{"name":"tianyuan","age":17},{"name":"lisi","age":20}]
my_set.insert(users)

#查询全部
# for i in my_set.find():
#     print(i)
#查询name=zhangsan的
# for i in my_set.find({"name":"zhangsan"}):
    # print(i)
# print(my_set.find_one({"name":"zhangsan"}))

my_set.update({"name":"zhangsan"},{'$set':{"age":20}}#update数据



#例：查询集合中age大于25的所有记录
my_set.find({"age":{"$gte":23}})
