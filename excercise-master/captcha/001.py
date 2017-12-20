# -*- coding:utf-8 -*-
__author__ = 'IanChen'

import pytesseract
from PIL import Image
import base64
import requests
import json

# im = Image.open("code.jpg")
# im = im.convert("L")

#
# def initTable(threshold=140):
#     table = []
#     for i in range(256):
#         if i < threshold:
#             table.append(0)
#         else:
#             table.append(1)
#
#     return table
#
# binaryImage = im.point(initTable(), '1')
# binaryImage.show()
# tmp=pytesseract.image_to_string(im)
# print(tmp)

# with open('captcha.jpg','rb') as f:
#     base64_data=str(base64.b64encode(f.read()))
#     base64_data=base64_data[2:-1]
#
#     post_data={"a": 1,"b":base64_data}
#     post_data=json.dumps({"a": 1,"b": base64_data})
#     res=requests.post(url="http://192.168.18.113:8002/mycode.ashx",data=post_data)
#     print(res.text)

i=11//6
print(i)
for i in range(1):
    print(i)

