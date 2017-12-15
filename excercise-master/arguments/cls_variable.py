# -*- coding:utf-8 -*-
__author__ = 'IanChen'


class Test(object):
    num_of_instance = 0  # 类变量

    def __init__(self, name):
        self.name = name  # 实例变量
        Test.num_of_instance += 1


if __name__ == '__main__':
    print(Test.num_of_instance)  # 0
    t1 = Test('jack')
    print(Test.num_of_instance)  # 1
    t2 = Test('lucy')
    print(t1.name, t1.num_of_instance)  # jack 2
    print(t2.name, t2.num_of_instance)  # lucy 2
