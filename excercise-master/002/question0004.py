# -*- coding:utf-8 -*-
__author__ = 'IanChen'

#统计单词出现的个数
import re
with open('danciceshi.txt',"r") as f:
    str=f.read()
    words=re.findall("\b?(\w+)\b?",str)
    wordDict=dict()
    for word in words:
        if word.lower() in wordDict:
            wordDict[word.lower()]+=1
        else:
            wordDict[word]=1
    for key,value in wordDict.items():
        print("%s:%s"%(key,value))
    f.close()

# import re
#
# fin = open('danciceshi.txt', 'r')
# str = fin.read()
#
# reObj = re.compile('\b?(\w+)\b?')
# words = reObj.findall(str)
#
# wordDict = dict()
#
# for word in words:
#     if word.lower() in wordDict:
#         wordDict[word.lower()] += 1
#     else:
#         wordDict[word] = 1
#
# for key, value in wordDict.items():
#     print('%s: %s' % (key, value))