# -*- coding:utf-8 -*-
__author__ = 'IanChen'


x = [4, 6, 2, 1, 7, 3,111,231,24]
# x.sort()
# print(x)
def my_sort(list):
    for i in range(len(list)-1):
        for j in range(i + 1, len(list)):
            if list[i] > list[j]:
                transfer = list[i]
                list[i] = list[j]
                list[j] = transfer
    return list

print(my_sort(x))