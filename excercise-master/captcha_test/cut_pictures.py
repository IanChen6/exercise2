# -*- coding:utf-8 -*-
__author__ = 'IanChen'


from PIL import Image,ImageEnhance
from PIL import ImageFilter
import time

#图片切割
def segment(im):
    s = 12
    w = 40
    h = 81
    t = 0
    im_new = []

    for i in range(4):
        im1 = im.crop((s + w * i, t, s + w * (i + 1), h))#区域拷贝
        im_new.append(im1)
    return im_new


# 图片预处理，二值化，图片增强
def imgTransfer(f_name):
    im = Image.open(f_name)
    im = im.filter(ImageFilter.MedianFilter())
    # enhancer = ImageEnhance.Contrast(im)
    # im = enhancer.enhancer(1)
    im = im.convert('L')

    return im