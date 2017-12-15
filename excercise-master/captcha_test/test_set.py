# -*- coding:utf-8 -*-
__author__ = 'IanChen'
import requests
import time

# 文件下载，主要下载训练集
def download_pics(pic_name):
    url = 'http://smart.gzeis.edu.cn:8081/Content/AuthCode.aspx'
    res = requests.get(url, stream=True)

    with open(u'J:/数据分析学习/python/机器学习之验证码识别/pics/%s.jpg' % (pic_name), 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()


if __name__ == '__main__':
    for i in range(100):
        pic_name = int(time.time() * 1000000)
        download_pics(pic_name)