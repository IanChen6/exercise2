# -*- coding:utf-8 -*-
__author__ = 'IanChen'

# 敏感词文本文件 filtered_words.txt，里面的内容为以下内容，
# 当用户输入敏感词语时，则打印出 Freedom，否则打印出 Human Rights。

word_filtered=set()
with open("敏感词.txt","r") as f:
    for w in f.readlines():
        word_filtered.add(w.strip())

while True:
    s=input("input：")
    s=s.replace(" ","")
    if s == "exit":
        break
    if s in word_filtered:
        print("you have input an illegal word")
    else:
        print(s)