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

from sklearn import datasets
from sklearn.linear_model import LinearRegression

# iris=datasets.load_iris()
#data对应了样本的四个特征,150行4列
# print(iris.data.shape)
# print(iris.data[:5])#x显示样本特征的前5行
# print(iris.target.shape)#target对应了样本的类别（目标属性），150行1列 （这里的目标属性就是鸢尾花的品种）
# print(iris.target)#显示样本的所有目标属性

model=LinearRegression()
print(model)