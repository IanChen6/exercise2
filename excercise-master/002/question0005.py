# -*- coding:utf-8 -*-
__author__ = 'IanChen'

from PIL import Image
import os

path = "image"
for pict in os.listdir(path):
    pictpath=os.path.join(path,pict)
    print(pictpath)
    with Image.open(pictpath) as im:
        w,h=im.size
        n=w/1366 if (w/1366) >=(h/640) else h/640
        im.thumbnail((w/n,h/n))
        im.save(pict+'_result.jpg',"jpeg")

