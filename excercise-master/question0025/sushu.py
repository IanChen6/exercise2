# -*- coding:utf-8 -*-
__author__ = 'IanChen'

# def get_prime(a,b):
#     for i in range(a,b):
#         if is_prime(i):
#             print(i)
#
#
# def is_prime(a):
#     for i in range(2,a-1):
#         if a%i == 0:
#             return False
#
#     return True
#
# get_prime(10,40)

for i in range(10, 40):
    flag = True
    for j in range(2, i - 1):
        if i % j == 0:
            flag=False
            # break
    if flag:
        print(i)
        # break
