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
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy
from PIL import  Image

with open('wordcloud.txt','r',encoding='utf-8') as f:
    mytext=f.read()
alice=numpy.array(Image.open('alice.png'))#设置词云形状
#设置停用词
stopwords = set(STOPWORDS)
stopwords.add("其他")
stopwords.add("阅读")
stopwords.add("相关")
stopwords.add("一个")
wordcloud=WordCloud(background_color="white",width=1000, height=860, margin=2,stopwords=stopwords,random_state=1, mask=alice,font_path = r'C:/Users/Windows/fonts/simkai.ttf').generate(mytext)#字体解析路径、random state 是给一个随机设定的初始值
image_colors = ImageColorGenerator(alice)#根据给定图片的颜色布局生成字体颜色
# %matplotlib inline
# plt.imshow(wordcloud,interpolation='bilinear')
plt.imshow(wordcloud.recolor(color_func=image_colors),interpolation='bilinear')
plt.axis('off')
plt.show()
wordcloud.to_file('test.png')
pass


