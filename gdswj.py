# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：广东省税务局登记信息抓取
   Description :
   Author :       ianchen
   date：
-------------------------------------------------
   Change Activity:
                   2017/11/22:
-------------------------------------------------
"""
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
import sys
import platform
import logging
import os

# import requests
# from pdfminer.converter import PDFPageAggregator
# from pdfminer.layout import LTTextBoxHorizontal, LAParams
# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
# from pdfminer.pdfparser import PDFParser, PDFDocument

# 读取账号信息
with open('guangdong.txt', 'r', encoding='utf8') as f:
    mess = f.read()
    if mess.startswith(u'\ufeff'):
        mess = mess.encode('utf8')[3:].decode('utf8')
    mess = json.loads(mess)
    f.close()

zh = mess['zh']
pwd = mess['pwd']
companyid = "0"
batchid = mess['batchid']
companyname = mess['companyname']
jobname = "抓取数据"
jobparams = mess['jobparams']
zh = json.loads(jobparams)['Request']
if not zh.strip():
    zh=mess['zh']


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


logger = create_logger(path='gdgs')


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
    sysname = platform.platform()
    if "XP" in sysname or "xp" in sysname:
        browser = webdriver.Chrome(executable_path='chromedriver_xp.exe', chrome_options=options)  # 添加driver的路径
    else:
        browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)  # 添加driver的路径
    browser.get(
        url='http://www.etax-gd.gov.cn/sso/login?service=http://www.etax-gd.gov.cn/xxmh/html/index.html?bszmFrom=1&t=1523156103552')
    wait = ui.WebDriverWait(browser, 8)
    wait.until(lambda browser1: browser1.find_element_by_css_selector("#one1"))
    browser.find_element_by_xpath("//*[@id='userName']").send_keys(zh)  # send_keys：实现往框中输入内容
    browser.find_element_by_xpath("//*[@id='passWord']").send_keys(pwd)
    # dragger = browser.find_element_by_css_selector('#nc_1_n1z')
    # action = ActionChains(browser)
    # action.click_and_hold(dragger).perform()
    # try:
    #     for index in range(20):
    #         try:
    #             action.move_by_offset(10, 0).perform()  # 平行移动鼠标
    #         except UnexpectedAlertPresentException:
    #             break
    #         action.reset_actions()
    #         time.sleep(0.1)  # 等待停顿时间
    # except:
    #     pass
except Exception as e:
    try:
        print("浏览器启动异常")
        logger.info("浏览器启动异常")
        logger.info(e)
        sys.exit()
    except Exception as e:
        print()
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
            logger.info("浏览器异常关闭")
            logger.info(e)
            print(e)
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
            logger.info("浏览器异常关闭")
            sys.exit()
    if '欢迎您' in page:
        try:
            logger.info("登录成功")
            add_task('39.108.1.170', '3433', 'Platform', batchid, '0', '0', companyid, '0',
                     "CUSTOMERINFO", jobname, jobparams)
            logger.info("任务添加成功")
            b_ck = browser.get_cookies()
            browser.quit()
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
            dcap["phantomjs.page.settings.loadImages"] = True
            browser = webdriver.PhantomJS(
                executable_path='phantomjs.exe',
                desired_capabilities=dcap)
            browser.implicitly_wait(10)
            browser.get(url='http://gs.etax-gd.gov.cn/xxmh/html/index.html')
            browser.delete_all_cookies()
            browser.add_cookie(
                {'domain': '.gs.etax-gd.gov.cn', 'name': b_ck[0]['name'], 'value': b_ck[0]['value'], 'path': '/',
                 'expires': None})
            browser.add_cookie(
                {'domain': '.gs.etax-gd.gov.cn', 'name': b_ck[1]['name'], 'value': b_ck[1]['value'], 'path': '/',
                 'expires': None})
            browser.add_cookie(
                {'domain': '.gs.etax-gd.gov.cn', 'name': b_ck[2]['name'], 'value': b_ck[2]['value'], 'path': '/',
                 'expires': None})
            browser.add_cookie(
                {'domain': '.gs.etax-gd.gov.cn', 'name': b_ck[3]['name'], 'value': b_ck[3]['value'], 'path': '/',
                 'expires': None})
            browser.add_cookie(
                {'domain': '.gs.etax-gd.gov.cn', 'name': b_ck[4]['name'], 'value': b_ck[4]['value'], 'path': '/',
                 'expires': None})
            browser.add_cookie(
                {'domain': '.gs.etax-gd.gov.cn', 'name': b_ck[5]['name'], 'value': b_ck[5]['value'], 'path': '/',
                 'expires': None})
            browser.get(
                'http://gs.etax-gd.gov.cn/web-tycx/tycx/4thLvlFunTabsInit.do?cdId=511&gnDm=sscx.yhscx.swdjcx#none')
            page = browser.page_source
            # 国税
            browser.switch_to_frame('cxtable')
            time.sleep(1)
            browser.switch_to_frame('nsrxxIframe')
            page1 = browser.page_source
            if "纳税人识别号" not in page1:
                for jz in range(10):
                    if "纳税人识别号" not in page1:
                        browser.get(
                            'http://gs.etax-gd.gov.cn/web-tycx/tycx/4thLvlFunTabsInit.do?cdId=511&gnDm=sscx.yhscx.swdjcx#none')
                        page = browser.page_source
                        browser.switch_to_frame('cxtable')
                        time.sleep(1)
                        browser.switch_to_frame('nsrxxIframe')
                        page1 = browser.page_source
                    else:
                        print("查询成功")
            root = etree.HTML(page1)
            judge = root.xpath('//*[@id="dwnsrjbxx"]//table')
            # 表格标题
            title = root.xpath('//*[@id="dwnsrjbxx"]//div[@class="searchTable"]/div')
            t_list = []
            for t in title:
                tt = t.xpath("./div/text()")
                print(tt[0])
                t_list.append(tt[0])
            t_list.insert(0, "基本信息")
            a = 1
            tb_list = []
            for i in judge:
                data_json = []
                tb_detail = i.xpath(".//tr")
                for j in tb_detail:
                    t = j.xpath('./td')
                    for d in t:
                        a = d.xpath('./text()')
                        if len(a) == 0:
                            a.append("")
                        data_json.append(a)
                tb_list.append(data_json)

            data_dict = {}
            c = 0
            for i in range(len(t_list)):
                if t_list[i] == "投资总额":
                    tz = []
                    tz.append(tb_list[c])
                    c = c + 1
                    tz.append(tb_list[c])
                    data_dict[t_list[i]] = tz
                elif t_list[i] == "总分机构情况":
                    zfjg = []
                    zfjg.append(tb_list[c])
                    c = c + 1
                    zfjg.append(tb_list[c])
                    c = c + 1
                    zfjg.append(tb_list[c])
                    c = c + 1
                    zfjg.append(tb_list[c])
                    data_dict[t_list[i]] = zfjg
                else:
                    data_dict[t_list[i]] = tb_list[c]
                c += 1
            print(data_dict)
            gs_data = {}
            if '基本信息' in data_dict.keys():
                d1 = {}
                get_data = data_dict["基本信息"]
                for i in range(0, len(get_data), 2):
                    d1[get_data[i][0]] = get_data[i + 1][0]
                    end = i + 1
                    endflag = len(get_data) - 1
                    if end >= endflag:
                        break
                gs_data["基本信息"] = d1
            zh=gs_data["基本信息"]['纳税人识别号（社会信用代码）：']
            zh=zh.encode("utf-8").decode("utf8")
            if '登记状态信息' in data_dict.keys():
                biaoti = ["项目内容", "姓名", "身份证件种类", "证件号码", "固定电话", "移动电话", "电子邮箱"]
                d1 = {}
                get_data = data_dict["登记状态信息"]
                clean = split_by_n(get_data, 7)
                for i in range(len(clean)):
                    d2 = {}
                    for j in range(len(biaoti)):
                        d2[biaoti[j]] = clean[i][j][0]
                    d1[i] = d2
                gs_data["登记状态信息"] = d1

            if '注册资本' in data_dict.keys():
                biaoti = ["币种", "币种金额"]
                d1 = {}
                get_data = data_dict["注册资本"]
                clean = split_by_n(get_data, 2)
                for i in range(len(clean)):
                    d2 = {}
                    for j in range(len(biaoti)):
                        d2[biaoti[j]] = clean[i][j][0]
                    d1[i] = d2
                gs_data["注册资本"] = d1

            if '投资总额' in data_dict.keys():
                biaoti = ["币种", "币种金额"]
                d1 = {}
                d3 = {}
                get_data = data_dict["投资总额"]
                clean = split_by_n(get_data[0], 2)
                for i in range(len(clean)):
                    d2 = {}
                    for j in range(len(biaoti)):
                        d2[biaoti[j]] = clean[i][j][0]
                    d1[i] = d2
                d3['金额'] = d1
                biaoti = ["投资方名称", "投资方经济性质", "投资比例", "证件种类", "证件号码", "国籍", "地址"]
                d1 = {}
                clean = split_by_n(get_data[1], 7)
                for i in range(len(clean)):
                    d2 = {}
                    for j in range(len(biaoti)):
                        d2[biaoti[j]] = clean[i][j][0]
                    d1[i] = d2
                d3['投资方信息'] = d1
                gs_data["投资总额"] = d3

            if '总分机构情况' in data_dict.keys():
                biaoti = ["纳税人识别号", "名称", "注册地址"]
                d1 = {}
                d2 = {}
                d3 = {}
                get_data = data_dict["总分机构情况"]
                for i in range(len(biaoti)):
                    d2[biaoti[i]] = get_data[1][i][0]
                d3['分支机构情况'] = d2
                for i in range(0, len(get_data[2]), 2):
                    d1[get_data[2][i][0]] = get_data[2][i + 1][0]
                    end = i + 1
                    endflag = len(get_data[2]) - 1
                    if end >= endflag:
                        break
                for i in range(0, len(get_data[3]), 2):
                    d1[get_data[3][i][0]] = get_data[3][i + 1][0]
                    end = i + 1
                    endflag = len(get_data[3]) - 1
                    if end >= endflag:
                        break
                d3['总机构情况'] = d1
                gs_data["总分机构情况汇总"] = d3
            print(data_dict)
            info = {}
            info['国税'] = gs_data
            # logger.info(info)
            logger.info("国税信息获取成功")

            # 地税
            browser.switch_to_default_content()
            time.sleep(0.1)
            browser.switch_to_frame('cxtable')
            time.sleep(0.1)
            browser.find_element_by_link_text('地税').click()
            time.sleep(5)
            browser.switch_to_frame('nsrxxIframe')
            page1 = browser.page_source
            if "纳税人识别号" not in page1:
                for cs in range(10):
                    if "纳税人识别号" not in page1:
                        browser.switch_to_default_content()
                        time.sleep(0.1)
                        browser.switch_to_frame('cxtable')
                        time.sleep(0.1)
                        browser.find_element_by_link_text('地税').click()
                        time.sleep(5)
                        browser.switch_to_frame('nsrxxIframe')
                        page1 = browser.page_source
                    else:
                        print("查询成功")
            root = etree.HTML(page1)
            judge = root.xpath('//*[@id="dwnsrjbxx"]//table')
            # 表格标题
            title = root.xpath('//*[@id="dwnsrjbxx"]//div[@class="searchTable"]/div')
            t_list = []
            for t in title:
                tt = t.xpath("./div/text()")
                print(tt[0])
                t_list.append(tt[0])
            t_list.insert(0, "基本信息")
            a = 1
            tb_list = []
            for i in judge:
                data_json = []
                tb_detail = i.xpath(".//tr")
                for j in tb_detail:
                    t = j.xpath('./td')
                    for d in t:
                        a = d.xpath('./text()')
                        if len(a) == 0:
                            a.append("")
                        data_json.append(a)
                tb_list.append(data_json)
            data_dict = {}
            c = 0
            for i in range(len(t_list)):
                if t_list[i] == "投资总额":
                    tz = []
                    tz.append(tb_list[c])
                    c = c + 1
                    tz.append(tb_list[c])
                    data_dict[t_list[i]] = tz
                elif t_list[i] == "总分机构情况":
                    zfjg = []
                    zfjg.append(tb_list[c])
                    c = c + 1
                    zfjg.append(tb_list[c])
                    c = c + 1
                    zfjg.append(tb_list[c])
                    c = c + 1
                    zfjg.append(tb_list[c])
                    data_dict[t_list[i]] = zfjg
                else:
                    data_dict[t_list[i]] = tb_list[c]
                c += 1
            print(data_dict)
            ds_data = {}
            if '基本信息' in data_dict.keys():
                d1 = {}
                get_data = data_dict["基本信息"]
                for i in range(0, len(get_data), 2):
                    d1[get_data[i][0]] = get_data[i + 1][0]
                    end = i + 1
                    endflag = len(get_data) - 1
                    if end >= endflag:
                        break
                ds_data["基本信息"] = d1

            if '登记状态信息' in data_dict.keys():
                biaoti = ["项目内容", "姓名", "身份证件种类", "证件号码", "固定电话", "移动电话", "电子邮箱"]
                d1 = {}
                get_data = data_dict["登记状态信息"]
                clean = split_by_n(get_data, 7)
                for i in range(len(clean)):
                    d2 = {}
                    for j in range(len(biaoti)):
                        d2[biaoti[j]] = clean[i][j][0]
                    d1[i] = d2
                ds_data["登记状态信息"] = d1

            if '注册资本' in data_dict.keys():
                biaoti = ["币种", "币种金额"]
                d1 = {}
                get_data = data_dict["注册资本"]
                clean = split_by_n(get_data, 2)
                for i in range(len(clean)):
                    d2 = {}
                    for j in range(len(biaoti)):
                        d2[biaoti[j]] = clean[i][j][0]
                    d1[i] = d2
                ds_data["注册资本"] = d1

            if '投资总额' in data_dict.keys():
                biaoti = ["币种", "币种金额"]
                d1 = {}
                d3 = {}
                get_data = data_dict["投资总额"]
                clean = split_by_n(get_data[0], 2)
                for i in range(len(clean)):
                    d2 = {}
                    for j in range(len(biaoti)):
                        d2[biaoti[j]] = clean[i][j][0]
                    d1[i] = d2
                d3['金额'] = d1
                biaoti = ["投资方名称", "投资方经济性质", "投资比例", "证件种类", "证件号码", "国籍", "地址"]
                d1 = {}
                clean = split_by_n(get_data[1], 7)
                for i in range(len(clean)):
                    d2 = {}
                    for j in range(len(biaoti)):
                        d2[biaoti[j]] = clean[i][j][0]
                    d1[i] = d2
                d3['投资方信息'] = d1
                ds_data["投资总额"] = d3

            if '总分机构情况' in data_dict.keys():
                biaoti = ["纳税人识别号", "名称", "注册地址"]
                d1 = {}
                d2 = {}
                d3 = {}
                get_data = data_dict["总分机构情况"]
                for i in range(len(biaoti)):
                    d2[biaoti[i]] = get_data[1][i][0]
                d3['分支机构情况'] = d2
                for i in range(0, len(get_data[2]), 2):
                    d1[get_data[2][i][0]] = get_data[2][i + 1][0]
                    end = i + 1
                    endflag = len(get_data[2]) - 1
                    if end >= endflag:
                        break
                for i in range(0, len(get_data[3]), 2):
                    d1[get_data[3][i][0]] = get_data[3][i + 1][0]
                    end = i + 1
                    endflag = len(get_data[3]) - 1
                    if end >= endflag:
                        break
                d3['总机构情况'] = d1
                ds_data["总分机构情况汇总"] = d3
            print(ds_data)
            info['地税'] = ds_data
            # logger.info(info)
            logger.info("国税信息获取成功")

            # 查询季报数据
            browser.get("http://gs.etax-gd.gov.cn/web-tycx/tycx/4thLvlFunTabsInit.do?cdId=513&gnDm=sscx.yhscx.sbzscx")
            cc = browser.page_source
            browser.find_element_by_xpath('//*[@id="gnmc"]/li[2]/a').click()
            browser.switch_to_frame('cxtable')
            time.sleep(0.5)
            wait = ui.WebDriverWait(browser, 8)
            wait.until(lambda browser: browser.find_element_by_css_selector('#sbssqq'))
            time.sleep(0.5)
            browser.find_element_by_css_selector('#zsxmDm').find_element_by_xpath(
                '//option[@value="10104"]').click()  # 选择企业所得税
            browser.find_element_by_css_selector('#sblxDm').find_element_by_xpath(
                '//option[@value="3"]').click()  # 选择按季申报
            sb_startd = browser.find_element_by_css_selector('#skssqq')
            sb_startd.clear()
            sb_startd.send_keys('2017-10-01')
            sb_endd = browser.find_element_by_css_selector('#skssqz')
            sb_endd.clear()
            sb_endd.send_keys('2017-12-31')
            sb_startd = browser.find_element_by_css_selector('#sbssqq')
            sb_startd.clear()
            sb_startd.send_keys('2017-01-01')
            sb_startd.click()
            time.sleep(1)
            browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/table/tbody/tr[3]/td[5]/input').click()
            time.sleep(2)
            # 表格信息爬取
            content = browser.page_source
            root = etree.HTML(content)
            select = root.xpath('//table[@id="dataList"]/tbody/tr')
            pg = browser.page_source
            if "没有" not in pg:
                for i in select[1:]:
                    jsxx = i.xpath('.//text()')
                    jsxx = list(filter(lambda x: x.strip(), jsxx))
                    if "度预缴纳税申报表" in jsxx[3] and "2017-10-01" in jsxx[6] and "2017-12-31" in jsxx[7]:
                        yyj = jsxx[11]
                        ybt = jsxx[12]
                        zgjg = jsxx[1]
                        ynsb = {}
                        ynsb['实际已预缴所得税额'] = yyj
                        ynsb['应补(退)所得税额'] = ybt
                        ynsb["国地标志"] = zgjg
                        info["上季度纳税情况"] = ynsb
                        logger.info("查询到季报信息")
                        break
            # 纳税人登记信息
            browser.get("https://gs.etax-gd.gov.cn/web-sxbl/BsfwtWeb/pages/yhs/rd/ybnsrdjxxcx.html")
            time.sleep(2)
            content = browser.page_source
            for i in range(5):
                if "增值税一般纳税人" not in content:
                    browser.get("https://gs.etax-gd.gov.cn/web-sxbl/BsfwtWeb/pages/yhs/rd/ybnsrdjxxcx.html")
                    time.sleep(2)
                    content = browser.page_source
            root = etree.HTML(content)
            select = root.xpath('//div[@class="mini-grid-bodyInner"]//tbody/tr')
            gszgcx = {}
            for i in select[1:]:
                tiaomu = {}
                zgtb = i.xpath('.//text()')
                title = ['序号', '文字字轨', '纳税人资格认定名称', '有效期起', '有效期止', '认定日期']
                for j in range(len(zgtb)):
                    tiaomu[title[j]] = "".join(zgtb[j].split())
                try:
                    if "增值税一般纳税人" not in tiaomu["纳税人资格认定名称"]:
                        continue
                except:
                    continue
                gszgcx[zgtb[0]] = tiaomu
            info['纳税人资格查询'] = gszgcx

            logger.info(info)
            insert_db('[dbo].[Python_Serivce_GSTaxGuangDong_Add]',
                      ((batchid, companyname, zh, pwd, json.dumps(info, ensure_ascii=False))))
            print("数据插入成功")
            logger.info("数据插入成功")
            job_finish('39.108.1.170', '3433', 'Platform', batchid, companyid, "0", '1',
                       "国税局成功爬取")

            # 获取pdf地址
            # ck = {}
            # for x in b_ck:
            #     ck[x['name']] = x['value']
            # headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            #            'Accept-Language': 'zh-CN,zh;q=0.9',
            #            'Accept - Encoding': 'gzip, deflate',
            #            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            #            'Connection': 'keep-alive'}
            # resp = requests.get(url='http://gs.etax-gd.gov.cn/web-sbzs/nssb/printPdf.do?pzxh=10014418000006825186', headers=headers,timeout=10,
            #                      cookies=ck).text
            # pdf_content = requests.get(url='http://gs.etax-gd.gov.cn/web-sbzs/nssb/printPdf.do?pzxh=10014418000006825186', headers=headers, timeout=10,
            #                             cookies=ck).content
            # if "错误" not in resp:
            #     with open("季度申报表详情{}.pdf".format(zh), 'wb') as w:
            #         w.write(pdf_content)
            #     parse_pdf("季度申报表详情{}.pdf".format(zh))
            # else:
            #     root = etree.HTML(resp)
            #     url=root.xpath('/html/head/script[6]/text()')[0]
            #     findurl = re.search('\/web-sbzs\/nssb\/showPdf.do\?fjkey=\d*', url)
            #     pdfurl='http://gs.etax-gd.gov.cn'+findurl.group()
            #     resp = requests.get(url=pdfurl,
            #                         headers=headers, timeout=10,
            #                         cookies=ck).text
            #     pdf_content = requests.get(
            #         url=pdfurl, headers=headers,
            #         timeout=10,
            #         cookies=ck).content
            #     if "错误" not in resp:
            #         with open("季度申报表详情{}.pdf".format(zh), 'wb') as w:
            #             w.write(pdf_content)
            #         parse_pdf("季度申报表详情{}.pdf".format(zh))
            # jdpdf_dict = self.parse_pdf("resource/{}/申报表详情{}.pdf".format(self.user, pzxh))
            browser.quit()
            break

        except Exception as e:
            logger.info("国税局爬取失败")
            logger.info(e)
            print(e)
            browser.quit()
            job_finish('39.108.1.170', '3433', 'Platform', batchid, companyid, "0", '-1',
                       "爬取失败")
            # ycgb = browser.window_handles
            # dq = browser.current_window_handle
            # for c_window in ycgb:
            #     if c_window != dq:
            #         browser.switch_to_window(c_window)
            #         browser.close()
            #         browser.switch_to_window(dq)
            # browser.get( 'http://gs.etax-gd.gov.cn/xxmh/html/index.html')
            # time.sleep(1.5)
