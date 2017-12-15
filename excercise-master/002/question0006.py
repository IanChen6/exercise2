# -*- coding:utf-8 -*-
__author__ = 'IanChen'

"""
**第 0006 题：**
你有一个目录，放了你一个月的日记，都是 txt，
为了避免分词的问题，假设内容都是英文，请统计出你认为每篇日记最重要的词。
"""
import os
import re


def findWord(file):
    with open('danciceshi.txt', "r") as f:
        str = f.read()
        words = re.findall("\b?(\w+)\b?", str)
        wordDict = dict()
        for word in words:
            if word.lower() in wordDict:
                wordDict[word.lower()] += 1
            else:
                wordDict[word] = 1
        # for key, value in wordDict.items():
        #     print("%s:%s" % (key, value))
        ansList = sorted(wordDict.items(), key=lambda t: t[1], reverse=True)
        print('file: %s->the most word: %s' % (file, ansList[1]))



if __name__ == '__main__':
    findWord('F:\excercise\002\danciceshi.txt')