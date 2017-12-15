# -*- coding:utf-8 -*-
__author__ = 'IanChen'

# 第0010题：使用Python生成类似于下图中的字母验证码图片

from PIL import Image,ImageDraw,ImageFont,ImageFilter

import random

def rndChar():
    return chr(random.randint(65,90))#返回ASCII字符

def rndColor():
    return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

def rndColor2():
    return (random.randint(32,127),random.randint(32,127),random.randint(32,127))

width=240
height=60
image=Image.new("RGB",(width,height),(255,255,255))#Image.new(mode,size,color=None)
# 创建Font对象
font = ImageFont.truetype('C:/windows/fonts/Arial.ttf', 36)#加载一个TrueType或者OpenType字体文件，并且创建一个字体对象
#创建Draw对象
draw=ImageDraw.Draw(image)
#填充每一个像素
for x in range(width):
    for y in range(height):
        draw.point((x,y),fill=rndColor())
#输出文字
for t in range(4):
    a=rndChar()
    draw.text((60*t+10,10),a,font=font,fill=rndColor2())

#模糊
image = image.filter(ImageFilter.BLUR)
image.save("code.jpg","jpeg")