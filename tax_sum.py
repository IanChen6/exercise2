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
import json
import socket
import re
import decimal
import sys
from lxml import etree
import time
from selenium import webdriver
from selenium.webdriver.support import ui

with open('python.txt', 'r') as f:
    mess = json.loads(f.read())
    f.close()
user = mess['user']
pwd = mess['pwd']
fw1 = float(mess['fw1'])
fw2 = float(mess['fw2'])
hw1 = float(mess['hw1'])
hw2 = float(mess['hw2'])
hwms = float(mess['hwms'])
hwyj = float(mess['hwyj'])
fwms = float(mess['fwms'])
fwyj = float(mess['fwyj'])
companyid = mess["companyid"]
customerid = int(mess["customerid"])

import pymssql


def get_db(companyid):
    conn = pymssql.connect(host='39.108.1.170', port='3433', user='Python', password='pl,okmPL<OKM',
                           database='CompanyCenter', autocommit=True, charset='utf8')
    cur = conn.cursor()
    sql = "[dbo].[Platform_Company_GetDBUrl]"
    params = (companyid, pymssql.output(str, ''))
    foo = cur.callproc(sql, params)
    jdbc = foo[-1]
    import re
    match = re.search(r'jdbc:sqlserver://(.*?):(\d+);database=(.*)', jdbc)
    host = match.group(1)
    port = int(match.group(2))
    db = match.group(3)
    conn.close()
    return host, port, db


def insert_db(host, port, db, sql, params):
    conn = pymssql.connect(host=host, port=port, user='Python', password='pl,okmPL<OKM',
                           database=db, charset='utf8')
    cur = conn.cursor()
    if not cur:
        raise Exception("数据库连接失败")
    len(params)
    cur.callproc(sql, params)
    conn.commit()
    cur.close()


host, port, db = get_db(companyid)

options = webdriver.ChromeOptions()
# options.add_argument("headless")
# options.add_argument("window-size=1200x1600")
options.add_argument('disable-infobars')
options.add_argument("--start-maximized")
# D:/BaiduNetdiskDownload/chromedriver.exe
try:
    browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    browser.get(url='http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html')
    wait = ui.WebDriverWait(browser, 8)
    wait.until(lambda browser1: browser1.find_element_by_css_selector("#shlogin"))
    browser.find_element_by_xpath('//li[@id="shlogin"]').click()
    browser.find_element_by_xpath("//*[@id='nsrsbh$text']").send_keys(user)  # send_keys：实现往框中输入内容
    browser.find_element_by_xpath("//*[@id='nsrpwd$text']").send_keys(pwd)
except:
    try:
        print("浏览器启动异常")
        sys.exit()
    except Exception as e:
        print("socket服务端连接失败")
        print()
        sys.exit()
while True:
    try:
        page = browser.page_source
    except:
        try:
            print("浏览器异常关闭")
            sys.exit()
        except Exception as e:
            print(e)
            print("socket服务端连接失败")
            sys.exit()
    try:
        if '我的定制功能' in page:
            pass
    except:
        try:
            print("浏览器异常关闭")
            sys.exit()
        except Exception as e:
            print(e)
            print("socket服务端连接失败")
            sys.exit()
    if '我的定制功能' in page:
        try:
            browser.get(url="http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/fp/zzszyfpdksq/fp_zzszyfpdksq.html")
            # browser.find_element_by_css_selector("#mini-94 span").click()
            p=browser.page_source
            browser.switch_to_frame("txsqxx")
            fwpp = browser.find_element_by_css_selector('#dkfpjefw').text
            hwpp = browser.find_element_by_css_selector('#dkfpje').text
            fwzp = browser.find_element_by_css_selector('#zpdkjefw').text
            hwzp = browser.find_element_by_css_selector('#zpdkjehw').text
            gsparams = (companyid,customerid, fwpp,hwpp,fwzp,hwzp)
            insert_db(host, port, db, "[dbo].[Python_Serivce_GSInvoiceSummary_Add]", gsparams)
        except Exception as e:
            print("error")
            print(e)