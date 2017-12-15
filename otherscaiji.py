# -*- coding:UTF-8 -*-

#!/usr/bin/env python

# @Author  clevertang
# @Date    2017-7.12
import json
import sys
import time

import requests
from bs4 import BeautifulSoup

from libs.fetcher import Fetcher
from libs.loghandler import getLogger

sys.path.append("..")
sys.path.append("../..")


from conf import m_settings
from libs.taskbase import TaskBase


class Hfcredithov(TaskBase):



    def __init__(self):
        TaskBase.__init__(self)
        self.resultCount = 0
        self.fetcher = Fetcher(m_settings.mfile_database())
        self.beanstalkclient = m_settings.beanstalk_client()
        self.logger = getLogger(self.__class__.__name__, console_out=False, level="debug")
        self.province = "安徽省"
        self.city = "合肥"



    def sendData(self,url,name,date):
        extract_data={
            "topic":"registration_company",
            "company":name,
            "province":"安徽",
            "city":"安徽合肥",
            "registered_date":date,#"2011-11-11"
            "_site_record_id":"hfcredit.gov.cn",   #站点的site,
            "url":url #抓取到数据的url
        }
        self.beanstalkclient.put("offline_crawl_data",json.dumps(extract_data))
        time.sleep(1)
    #在call的时候调用这个函数
    def start(self):
        pageNum = json.loads(requests.get(
            "http://hfcredit.gov.cn/Credit/HFCreditImpl?method=xydmList&PageNum=1&temp=1499846781588").text).get(
            "total") / 10 + 1
        # domain = "http://hfcredit.gov.cn/HeFei/xydmlist.jsp?type=xydm"
        jsonbaisicurl = "http://hfcredit.gov.cn/Credit/HFCreditImpl?method=xydmList&PageNum={}&temp=1499842281095"
        try:
            for i in pageNum:
                url=jsonbaisicurl.format(i)
                data = requests.get(url).text
                jsondata = json.loads(data)
                rows = jsondata.get("rows")
                for a in rows:
                    name = a["MC"]
                    date = a["ZCRQ"]

                self.sendData(self,url,name,date)
        except Exception,e:
            pass




if __name__ == "__main__":
    worker = Hfcredithov()
    # worker.sendData()
    worker()
# 这个是我到公司写的第一份代码