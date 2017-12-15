# -*- coding:utf-8 -*-
__author__ = 'IanChen'

# 敏感词文本文件 filtered_words.txt，里面的内容为以下内容，
# 当用户输入敏感词语时，则用*代替

word_filtered=set()
with open("敏感词.txt","r") as f:
    for w in f.readlines():
        word_filtered.add(w.strip())

while True:
    s=input("input：")
    s=s.replace(" ","")
    if s == "exit":
        break
    # if s in word_filtered:
    #     s=s.replace(s,"*"*len(s))
    #     print(s)
    # else:
    #     print(s)
    for w in word_filtered:
        if w in s:
            s = s.replace(w, '*' * len(w))
    print(s)