# -*- coding:utf-8 -*-
__author__ = 'IanChen'

from PIL import ImageDraw,ImageFont,Image
import os

def add_number(img):
    draw= ImageDraw.Draw(img)
    myfont=ImageFont.truetype("C:/windows/fonts/Arial.ttf",size=40)
    fillcolor = "#ff0000"
    width,height = img.size
    draw.text((width-40,0),"40",font=myfont,fill=fillcolor)
    img.save('result.jpg',"jpeg")

    return 0
if __name__ == "__main__":
    image=Image.open("picture.png")
    add_number(image)
    print("%s进程启动......"%os.getpid())
