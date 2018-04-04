# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：   国家信用网
   Description :
   Author :       ianchen
   date：          
-------------------------------------------------
   Change Activity:
                   2017/11/22:
-------------------------------------------------
"""
import requests
from pyquery import PyQuery
import json
import re
import decimal
import sys
from lxml import etree
import time
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import ui
import pymssql
from selenium.webdriver.common.action_chains import ActionChains
import logging
import os

with open('gjcredit.txt', 'r', encoding='utf8') as f:
    mess = f.read()
    if mess.startswith(u'\ufeff'):
        mess = mess.encode('utf8')[3:].decode('utf8')
    mess = json.loads(mess)
    f.close()
companyid = "0"
batchid = mess['batchid']
companyname = mess['companyname']
jobname = "抓取数据"
jobparams = {}
jobparams = mess['jobparams']

def create_logger(level=logging.DEBUG, path="task"):
    # create logger
    logger_name = "example"
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    # create file handler
    log_path = './logs/{}log.log'.format(path)
    fh = logging.FileHandler(log_path, encoding='utf8')
    fh.setLevel(level)
    # CREATE FORMATTER
    fmt = "%(asctime)s %(levelname)s %(filename)s %(lineno)d %(thread)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)
    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


logger = create_logger(path='gjxy')

def insert_db(sql, params):
    conn = pymssql.connect(host='39.108.1.170', port='3433', user='python', password='pl,okmPL<OKM',
                           database='Platform', charset='utf8')
    cur = conn.cursor()
    if not cur:
        raise Exception("数据库连接失败")
    len(params)
    cur.callproc(sql, params)
    conn.commit()
    cur.close()


def add_task(host, port, db, batchid, batchyear, batchmonth, companyid, customerid, type, jobname, jobparam):
    conn = pymssql.connect(host=host, port=port, user='python', password='pl,okmPL<OKM', database=db, autocommit=True,
                           charset='utf8')
    cur = conn.cursor()
    sql = '[dbo].[Python_Serivce_Job_AddV1]'
    params = (batchid, batchyear, batchmonth, companyid, customerid, type, jobname, jobparam)
    foo = cur.callproc(sql, params)
    print(foo[-1])
    conn.close()


def job_finish(host, port, db, batchid, companyid, customerid, status, result):
    conn = pymssql.connect(host=host, port=port, user='Python', password='pl,okmPL<OKM', database=db, autocommit=True,
                           charset='utf8')
    cur = conn.cursor()
    sql = '[dbo].[Python_Serivce_Job_Finish]'
    params = (batchid, companyid, customerid, status, result)
    print(params)
    foo = cur.callproc(sql, params)
    conn.close()


def isplit_by_n(ls, n):
    for i in range(0, len(ls), n):
        yield ls[i:i + n]


def split_by_n(ls, n):
    return list(isplit_by_n(ls, n))


options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
options.add_argument("--start-maximized")

try:
    browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    browser.get(url='http://gd.gsxt.gov.cn/index.html')
    wait = ui.WebDriverWait(browser, 8)
    wait.until(lambda browser1: browser1.find_element_by_css_selector("#keyword"))
    browser.find_element_by_xpath("//*[@id='keyword']").send_keys(companyname)  # send_keys：实现往框中输入内容
    for i in range(3):
        browser.find_element_by_xpath("//*[@id='btn_query']").click()
        break
except:
    try:
        print("浏览器启动异常")
        logger.info("浏览器启动异常")
        sys.exit()
    except Exception as e:
        logger.info(e)
        print(e)
        sys.exit()
while True:
    try:
        page = browser.page_source
    except:
        try:
            print("浏览器异常关闭")
            logger.info("浏览器异常关闭")
            job_finish('39.108.1.170', '3433', 'Platform', batchid, companyid, "0", '-1',
                       "爬取失败")
            sys.exit()
        except Exception as e:
            print(e)
            logger.info(e)
            sys.exit()
    try:
        if '欢迎您' in page:
            pass
    except:
        try:
            print("浏览器异常关闭")
            logger.info("浏览器异常关闭")
            job_finish('39.108.1.170', '3433', 'Platform', batchid, companyid, "0", '-1',
                       "爬取失败")
            sys.exit()
        except Exception as e:
            print(e)
            logger.info(e)
            sys.exit()
    if '查询到' in page or '查询结果' in page:
        # 工商信用网基本信息的提取
        try:
            logger.info("查询到结果")
            add_task('39.108.1.170', '3433', 'Platform', batchid, '0', '0', companyid, '0',
                     "CUSTOMERINFO", jobname, jobparams)
            logger.info("添加任务")
            time.sleep(4)
            result = browser.page_source
            if companyname not in result:
                for cs in range(10):
                    if companyname not in result:
                        print("刷新页面")
                        browser.refresh()
                        browser.switch_to_alert().accept()
                        time.sleep(4)
                        html = browser.page_source
                    else:
                        break
            if companyname not in result:
                print("无该公司信息")
                browser.quit()
                break
            rq = PyQuery(result)
            alist = rq('.search_list_item')
            for i in alist:
                xqurl = PyQuery(i).attr('href')
                break
            # with open('gjxy.html', 'r', encoding='utf') as f:
            #     html = f.read()
            #     f.close()
            headers = {
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                'Cache-Control': 'max-age=0',
                "X-Requested-With": "XMLHttpRequest",
                "Host": "www.gsxt.gov.cn",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                "Connection": "keep-alive",
                'Upgrade-Insecure-Requests': '1',
                'Referer': 'http://www.gsxt.gov.cn/corp-query-search-1.html',
                "Cookie": "__jsluid=eb8523c9655107d177806597beb43f57; UM_distinctid=15b0d57141c23d-08caf973d-4349052c-1fa400-15b0d57141d940; tlb_cookie1=114ui_8280; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1492692994; Hm_lpvt_d7682ab43891c68a00de46e9ce5b76aa=1493024386; JSESSIONID=E7E8CC28F2EA0ABAF34E5B0B28A76730-n1:0; tlb_cookie=24query_8080; CNZZDATA1261033118=1201860774-1490573985-%7C1493103540; Hm_lvt_cdb4bc83287f8c1282df45ed61c4eac9=1490577462,1492505367; Hm_lpvt_cdb4bc83287f8c1282df45ed61c4eac9=1493104058",
                # "Referer": "http://www.gsxt.gov.cn/corp-query-search-1.html"
            }
            logger.info("获取详情页地址")
            detailurl = 'http://gd.gsxt.gov.cn' + xqurl
            browser.get(detailurl)
            time.sleep(3)
            html = browser.page_source
            if companyname not in html:
                for cs in range(10):
                    if companyname not in html:
                        print("刷新页面")
                        browser.get(detailurl)
                        time.sleep(2)
                        html = browser.page_source
                    else:
                        break
            if companyname not in html:
                print("无该公司信息")
                browser.quit()
                break
            # jq = PyQuery(html)
            # print(jq('title'))  # 获取title标签的源码
            # dl = jq(".overview dl")  # 处理多个元素
            # # print(div)
            # item_dict = {}
            # for i in dl:
            #     print(PyQuery(i).text())
            #     item = PyQuery(i).text()
            #     if ":" in item:
            #         itemlist = item.split(':', 1)
            #     elif "：" in item:
            #         itemlist = item.split('：', 1)
            #     item_dict[itemlist[0]] = itemlist[1]
            #     pass
            # print(item_dict)
            root = etree.HTML(html)
            dl = root.xpath('//*[@class="overview"]//dl')
            item_dict = {}
            for i in dl:
                print(PyQuery(i).text())
                item = PyQuery(i).text()
                if ":" in item:
                    itemlist = item.split(':', 1)
                elif "：" in item:
                    itemlist = item.split('：', 1)
                item_dict[itemlist[0]] = itemlist[1].strip()
                pass
            select = root.xpath('//*[@id="shareholderInfo_wrapper"]//table//tbody/tr')
            title = ['序号', '股东名称']
            gd = {}
            gudong={}
            for i in select:
                nom = 0
                for j in title:
                    gd[title[nom]] = i.xpath(".//text()")[nom]
                    nom += 1
                gudong[gd['序号']]=gd
            item_dict["股东及出资信息"]=gudong
            print(item_dict)
            logger.info(item_dict)
            logger.info("信用网成功爬取")
            insert_db('[dbo].[Python_Serivce_CreditWebGuoJia_Add]',
                      (batchid, companyname, json.dumps(item_dict, ensure_ascii=False)))
            job_finish('39.108.1.170', '3433', 'Platform', batchid, companyid, "0", '1',
                       "信用网成功爬取")
            browser.quit()
            break

        except Exception as e:
            logger.info('爬取失败')
            logger.info(e)
            job_finish('39.108.1.170', '3433', 'Platform', batchid, companyid, "0", '-1',
                       "信用网爬取失败")
            browser.quit()
            print(e)
            pass
