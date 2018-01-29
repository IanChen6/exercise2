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
import decimal
import calendar
import hashlib
import json
import platform
from decimal import *
import pymssql
import requests
from suds.client import Client
import suds
import re
import decimal
import sys
from lxml import etree
import time
from selenium import webdriver
from selenium.webdriver.support import ui
import logging


def insert_db(host, port, db, sql, params):
    conn = pymssql.connect(host=host, port=port, user='Python', password='pl,okmPL<OKM',
                           database=db, charset='utf8', autocommit=False)
    cur = conn.cursor()
    if not cur:
        raise Exception("数据库连接失败")
    # cur.callproc('[dbo].[Python_Serivce_DSTaxApplyShenZhen_Add]', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))
    len(params)
    result = cur.callproc(sql, params)
    cur.nextset()
    nextResult = cur.fetchall()
    # result=cur.nextset()

    # conn.commit()
    cur.close()
    return nextResult


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


def create_logger(level=logging.DEBUG, path="ssss"):
    # create logger
    logger_name = "example"
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    # create file handler
    log_path = './logs/{}log.log'.format(path)
    fh = logging.FileHandler(log_path)
    fh.setLevel(level)
    # CREATE FORMATTER
    fmt = "%(asctime)s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)
    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


class ksbs(object):
    def __init__(self, logger):
        with open('ym.txt', 'r', encoding='utf8') as f:
            mess = f.read()
            if mess.startswith(u'\ufeff'):
                mess = mess.encode('utf8')[3:].decode('utf8')
            mess = json.loads(mess)
            f.close()
        self.taxid = mess['TaxId']
        self.pwd = mess['TaxPwd']
        self.periodyear = mess['PeriodYear']
        self.periodmonth = mess['PeriodMonth']
        self.opertype = mess['OperType']
        self.taxtype = mess['TaxType']
        self.bookid = mess['bookid']
        self.applyyear = mess['applyyear']
        self.applymonth = mess['applymonth']
        self.acclaw = mess['acclaw']
        self.Companyid = mess['CompanyID']
        self.logger = logger
        if 0 < self.periodmonth < 10:
            self.periodmonth = "0" + str(self.periodmonth)
        else:
            self.periodmonth = mess['PeriodMonth']
        monthRange = calendar.monthrange(self.periodyear, int(self.periodmonth))
        self.days = monthRange[1]

    def jiami(self):
        h = hashlib.sha1(self.pwd.encode('utf8')).hexdigest()
        return h

    def taggertwo(self, tupian, md):
        while True:
            try:
                client = suds.client.Client(url="http://39.108.112.203:8701/SZYZService.asmx?wsdl")
                result = client.service.SetYZImg(123456, "1215454545", "pyj", md, tupian)
                for i in range(30):
                    result1 = client.service.GetYZCode(md)
                    if result1 is not None:
                        result1 = str(result1)
                        return result1
                    time.sleep(10)
            except Exception as e:
                print(e)
            break

    def tagger(self, tupian, md):
        while True:
            try:
                client = suds.client.Client(url="http://39.108.112.203:8701/SZYZService.asmx?wsdl")
                auto = client.service.GetYZCodeForDll(tupian)
                if auto is not None:
                    result1 = str(auto)
                    return result1
                if auto is None:
                    return auto
            except Exception as e:
                print(e)
            break

    def login(self):
        try_times = 0
        while try_times <= 14:
            print("开始登陆")
            try_times += 1
            if try_times > 10:
                time.sleep(1)
            session = requests.session()
            headers = {'Host': 'dzswj.szgs.gov.cn',
                       'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'Content-Type': 'application/json; charset=UTF-8',
                       'Referer': 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                       'x-form-id': 'mobile-signin-form',
                       'X-Requested-With': 'XMLHttpRequest',
                       'Origin': 'http://dzswj.szgs.gov.cn'}
            session.get("http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html", headers=headers)
            captcha_url = 'http://dzswj.szgs.gov.cn/tipCaptcha'
            tupian_resp = session.get(url=captcha_url, timeout=10)
            tupian_resp.encoding = 'utf8'
            tupian = tupian_resp.json()
            image = tupian['image']
            tipmessage = tupian["tipMessage"]
            tupian = json.dumps(tupian, ensure_ascii=False)
            m = hashlib.md5()
            tupian1 = tupian.encode(encoding='utf8')
            m.update(tupian1)
            md = m.hexdigest()
            print(md)
            tag = self.tagger(tupian, md)
            if tag is None:
                continue
            jyjg = session.post(url='http://dzswj.szgs.gov.cn/api/checkClickTipCaptcha', data=tag)
            time_l = time.localtime(int(time.time()))
            time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
            tag = json.dumps(tag)
            login_data = '{"nsrsbh":"%s","nsrpwd":"%s","redirectURL":"","tagger":%s,"time":"%s"}' % (
                self.taxid, self.jiami(), tag, time_l)
            login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
            resp = session.post(url=login_url, data=login_data)
            # panduan=resp.json()['message']
            try:
                if "验证码正确" in jyjg.json()['message']:
                    if "登录成功" in resp.json()['message']:
                        print('登录成功')
                        cookies = {}
                        for (k, v) in zip(session.cookies.keys(), session.cookies.values()):
                            cookies[k] = v
                        return cookies
                    elif "账户和密码不匹配" in resp.json()['message'] or "不存在" in resp.json()['message'] or "已注销" in \
                            resp.json()['message']:
                        print('账号和密码不匹配')
                        status = "账号和密码不匹配"
                        return status
                    else:
                        time.sleep(3)
            except Exception as e:
                print(e)
        try_handed = 0
        while try_handed <= 3:
            try_handed += 1
            session = requests.session()
            # proxy_list = get_all_proxie()
            # proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]
            try:
                session.proxies = sys.argv[1]
            except:
                print("未传入代理参数")
            # session.proxies = {'https': 'http://116.22.211.55:6897', 'http': 'http://116.22.211.55:6897'}
            headers = {'Host': 'dzswj.szgs.gov.cn',
                       'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'Content-Type': 'application/json; charset=UTF-8',
                       'Referer': 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                       'x-form-id': 'mobile-signin-form',
                       'X-Requested-With': 'XMLHttpRequest',
                       'Origin': 'http://dzswj.szgs.gov.cn'}
            session.get("http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html", headers=headers)
            captcha_url = 'http://dzswj.szgs.gov.cn/tipCaptcha'
            tupian_resp = session.get(url=captcha_url, timeout=10)
            tupian_resp.encoding = 'utf8'
            tupian = tupian_resp.json()
            image = tupian['image']
            tipmessage = tupian["tipMessage"]
            tupian = json.dumps(tupian, ensure_ascii=False)
            m = hashlib.md5()
            tupian1 = tupian.encode(encoding='utf8')
            m.update(tupian1)
            md = m.hexdigest()
            print(md)
            tag = self.taggertwo(tupian, md)
            jyjg = session.post(url='http://dzswj.szgs.gov.cn/api/checkClickTipCaptcha', data=tag)
            time_l = time.localtime(int(time.time()))
            time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
            tag = json.dumps(tag)
            login_data = '{"nsrsbh":"%s","nsrpwd":"%s","redirectURL":"","tagger":%s,"time":"%s"}' % (
                self.taxid, self.jiami(), tag, time_l)
            login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
            resp = session.post(url=login_url, data=login_data)
            panduan = resp.json()['message']
            if "验证码正确" in jyjg.json()['message']:
                if "登录成功" in resp.json()['message']:
                    print('登录成功')
                    cookies = {}
                    for (k, v) in zip(session.cookies.keys(), session.cookies.values()):
                        cookies[k] = v
                    return cookies
                elif "账户和密码不匹配" in resp.json()['message'] or "不存在" in resp.json()['message'] or "已注销" in resp.json()[
                    'message']:
                    print('账号和密码不匹配')
                    status = "账号和密码不匹配"
                    return status
                else:
                    time.sleep(3)
            else:
                print("重试")
        return False

    def apply(self, browser):
        try:
            browser.find_element_by_xpath('//a[@id="mini-36"]/span').click()
            browser.find_element_by_xpath('//a[@id="mini-34"]/span').click()
            browser.find_element_by_xpath('//a[@id="mini-9"]/span').click()
            browser.find_element_by_xpath('//a[@id="mini-7"]/span').click()
        except:
            print("系统正常")
        browser.find_element_by_css_selector('#mini-4 span').click()

        page1 = browser.page_source
        root = etree.HTML(page1)
        judge = root.xpath('//*[@class="J_sbxx-tbody"]/tr')
        a = 1
        browser.find_element_by_css_selector(".sbxx-more").click()
        if self.taxtype == '全部':
            for i in judge:
                xgm = i.xpath('.//text()')
                if ' 小规模增值税季报 ' in xgm and '申报' in xgm:
                    try:
                        gsrq = xgm[5]
                        gsrq = re.search(r'(.*?)~(.*)', gsrq)
                        gsks = gsrq.group(1)
                        gsjs = gsrq.group(2)
                        browser.find_element_by_xpath(
                            '//*[@class="J_sbxx-tbody"]/tr[{}]//a[@class="opBtn"]'.format(a)).click()
                        allwins = browser.window_handles
                        shouye = browser.current_window_handle
                        for window in allwins:
                            if window != shouye:
                                browser.switch_to_window(allwins[-1])
                                zzs = window
                                browser.execute_script('document.title="国税-增值税"')
                                browser.switch_to_window(shouye)
                                break
                    except Exception as e:
                        self.logger.info(e)
                elif '企业所得税' in xgm[2] and '申报' in xgm:
                    try:
                        gsrq = xgm[5]
                        gsrq = re.search(r'(.*?)~(.*)', gsrq)
                        gsks = gsrq.group(1)
                        gsjs = gsrq.group(2)
                        browser.find_element_by_xpath(
                            '//*[@class="J_sbxx-tbody"]/tr[{}]//a[@class="opBtn"]'.format(a)).click()
                        allwins = browser.window_handles
                        shouye = browser.current_window_handle
                        for window in allwins:
                            if window != shouye:
                                browser.switch_to_window(allwins[-1])
                                qysd = window
                                browser.execute_script('document.title="国税-企业所得税"')
                                browser.switch_to_window(shouye)
                                break
                    except Exception as e:
                        self.logger.info(e)
                elif '企业财务报表' in xgm[2] and '申报' in xgm:
                    try:
                        gsrq = xgm[5]
                        gsrq = re.search(r'(.*?)~(.*)', gsrq)
                        gsks = gsrq.group(1)
                        gsjs = gsrq.group(2)
                        browser.find_element_by_xpath(
                            '//*[@class="J_sbxx-tbody"]/tr[{}]//a[@class="opBtn"]'.format(a)).click()
                        allwins = browser.window_handles
                        shouye = browser.current_window_handle
                        for window in allwins:
                            if window != shouye:
                                browser.switch_to_window(allwins[-1])
                                cwbb = window
                                browser.execute_script('document.title="国税-财务报表"')
                                browser.switch_to_window(shouye)
                                break
                    except Exception as e:
                        self.logger.info(e)
                a += 1
            # 地税申报页面
            try:
                wait = ui.WebDriverWait(browser, 8)
                ds_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/djsxx.html'
                browser.get(url=ds_url)
                try:
                    wait.until(lambda browser: browser.find_element_by_css_selector("#mini-29 .mini-button-text"))
                    browser.find_element_by_css_selector("#mini-29 .mini-button-text").click()
                except Exception as e:
                    print(e)
                    print("弹出框与预设不一致")
                try:
                    browser.find_element_by_css_selector("#mini-27 .mini-button-text").click()
                except Exception as e:
                    print(e)
                    print("弹出框与预设不一致")
                browser.find_element_by_xpath("//a[@href='javascript:gotoDs()']").click()
                time.sleep(3)
                windows = browser.window_handles
                window1 = browser.current_window_handle
                for c_window in windows:
                    if c_window != window1:
                        browser.close()
                        browser.switch_to_window(windows[-1])
                        break
                time.sleep(1)
                browser.find_element_by_css_selector('#layui-layer1 div.layui-layer-btn a').click()
                browser.switch_to_frame('qyIndex')
                wait.until(lambda browser: browser.find_element_by_css_selector("#menu3_3_102001"))
                browser.find_element_by_css_selector('#menu3_3_102001').click()
                browser.switch_to_frame('qymain')
                time.sleep(2)
                dspage = browser.page_source
                dsroot = etree.HTML(dspage)
                dsjudge = dsroot.xpath('//*[@id="tbody"]/tr')
                b = 1
                for i in dsjudge:
                    xgm = i.xpath('.//text()')
                    if '自行申报' in xgm and '我要申报' in xgm:
                        ssrq = browser.find_element_by_xpath('//*[@id="tbody"]/tr[{}]/td[3]'.format(b)).text
                        rq = re.search(r'(.*?)至(.*)', ssrq)
                        ks = rq.group(1)
                        js = rq.group(2)
                        browser.find_element_by_xpath('//*[@id="tbody"]/tr[{}]/td[7]/a'.format(b)).click()
                        browser.find_element_by_css_selector("#confirmSbBtn").click()
                        browser.execute_script('document.title="地税-地税三项"')
                        break
            except Exception as e:
                self.logger.info(e)
        if self.taxtype == '增值税':
            for i in judge:
                xgm = i.xpath('.//text()')
                if ' 小规模增值税季报 ' in xgm and '申报' in xgm:
                    try:
                        gsrq = xgm[5]
                        gsrq = re.search(r'(.*?)~(.*)', gsrq)
                        gsks = gsrq.group(1)
                        gsjs = gsrq.group(2)
                        browser.find_element_by_xpath(
                            '//*[@class="J_sbxx-tbody"]/tr[{}]//a[@class="opBtn"]'.format(a)).click()
                        allwins = browser.window_handles
                        shouye = browser.current_window_handle
                        for window in allwins:
                            if window != shouye:
                                browser.switch_to_window(allwins[-1])
                                zzs = window
                                browser.execute_script('document.title="国税-增值税"')
                                browser.switch_to_window(shouye)
                                break
                    except Exception as e:
                        self.logger.info(e)
                a += 1
            all = browser.window_handles
            c = browser.current_window_handle
            for cc in all:
                if cc != c:
                    browser.switch_to_window(cc)

        if self.taxtype == '企业所得税':
            for i in judge:
                xgm = i.xpath('.//text()')
                if '企业所得税' in xgm[2] and '申报' in xgm:
                    try:
                        gsrq = xgm[5]
                        gsrq = re.search(r'(.*?)~(.*)', gsrq)
                        gsks = gsrq.group(1)
                        gsjs = gsrq.group(2)
                        browser.find_element_by_xpath(
                            '//*[@class="J_sbxx-tbody"]/tr[{}]//a[@class="opBtn"]'.format(a)).click()
                        allwins = browser.window_handles
                        shouye = browser.current_window_handle
                        for window in allwins:
                            if window != shouye:
                                browser.switch_to_window(allwins[-1])
                                qysd = window
                                browser.execute_script('document.title="国税-企业所得税"')
                                browser.switch_to_window(shouye)
                                break
                    except Exception as e:
                        self.logger.info(e)
                a += 1
            all = browser.window_handles
            c = browser.current_window_handle
            for cc in all:
                if cc != c:
                    browser.switch_to_window(cc)

        if self.taxtype == '财务报表':
            for i in judge:
                xgm = i.xpath('.//text()')
                if '企业财务报表-季报' in xgm[2] and '申报' in xgm:
                    try:
                        # h,p,d=get_db(self.Companyid)
                        # fzdata=insert_db(h,p,d,'[dbo].[prAccount_Book_ReportTaxAsset]',(self.bookid,self.applyyear,self.applymonth,self.acclaw))
                        # lrdata=insert_db(h,p,d,'[dbo].[prAccount_Book_ReportTaxProfit]',(self.bookid,self.applyyear,self.applymonth,self.acclaw))
                        with open('asset.txt', 'r', encoding='utf8') as f:
                            fzdata = f.read()
                            if fzdata.startswith(u'\ufeff'):
                                fzdata = fzdata.encode('utf8')[3:].decode('utf8')
                            fzdata = json.loads(fzdata)
                            f.close()
                        with open('profitEnd.txt', 'r', encoding='utf8') as f:
                            lrdata = f.read()
                            if lrdata.startswith(u'\ufeff'):
                                lrdata = lrdata.encode('utf8')[3:].decode('utf8')
                            lrdata = json.loads(lrdata)
                            f.close()
                        gsrq = xgm[5]
                        gsrq = re.search(r'(.*?)~(.*)', gsrq)
                        gsks = gsrq.group(1)
                        gsjs = gsrq.group(2)
                        browser.find_element_by_xpath(
                            '//*[@class="J_sbxx-tbody"]/tr[{}]//a[@class="opBtn"]'.format(a)).click()
                        allwins = browser.window_handles
                        shouye = browser.current_window_handle
                        for window in allwins:
                            if window != shouye:
                                browser.switch_to_window(allwins[-1])
                                cwbb = window
                                if self.acclaw == "SMALL":
                                    for data in fzdata:
                                        if data[1] == "货币资金":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C1"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C1"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D1"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D1"]').send_keys(d2)
                                        if data[1] == "短期借款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G1"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G1"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H1"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H1"]').send_keys(d2)
                                        if data[1] == "短期投资":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C2"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D2"]').send_keys(d2)
                                        if data[1] == "应付票据":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G2"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H2"]').send_keys(d2)
                                        if data[1] == "应收票据":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C3"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D3"]').send_keys(d2)
                                        if data[1] == "应付账款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G3"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H3"]').send_keys(d2)
                                        if data[1] == "应收账款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C4"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D4"]').send_keys(d2)
                                        if data[1] == "预收账款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G4"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H4"]').send_keys(d2)
                                        if data[1] == "预付账款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C5"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D5"]').send_keys(d2)
                                        if data[1] == "应付职工薪酬":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G5"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H5"]').send_keys(d2)
                                        if data[1] == "应收股利":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C6"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D6"]').send_keys(d2)
                                        if data[1] == "应交税费":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G6"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H6"]').send_keys(d2)
                                        if data[1] == "应收利息":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C7"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D7"]').send_keys(d2)
                                        if data[1] == "应付利息":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G7"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H7"]').send_keys(d2)
                                        if data[1] == "其他应收款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C8"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D8"]').send_keys(d2)
                                        if data[1] == "应付利润":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G8"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H8"]').send_keys(d2)
                                        if data[1] == "存货":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C9"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D9"]').send_keys(d2)
                                        if data[1] == "其他应付款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G9"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H9"]').send_keys(d2)
                                        if data[1] == "其中：原材料":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C10"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D10"]').send_keys(d2)
                                        if data[1] == "其他流动负债":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G10"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H10"]').send_keys(d2)
                                        if data[1] == "在产品":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C11"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C11"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D11"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D11"]').send_keys(d2)
                                        if data[1] == "库存商品":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C12"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C12"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D12"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D12"]').send_keys(d2)
                                        if data[1] == "周转材料":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C13"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C13"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D13"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D13"]').send_keys(d2)
                                        if data[1] == "长期借款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G13"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G13"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H13"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H13"]').send_keys(d2)
                                        if data[1] == "其他流动资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C14"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C14"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D14"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D14"]').send_keys(d2)
                                        if data[1] == "长期应付款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G14"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G14"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H14"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H14"]').send_keys(d2)
                                        if data[1] == "递延收益":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G15"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G15"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H15"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H15"]').send_keys(d2)
                                        if data[1] == "其他非流动负债":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G45"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G45"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H45"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H45"]').send_keys(d2)
                                        if data[1] == "长期债券投资":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C16"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C16"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D16"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D16"]').send_keys(d2)
                                        if data[1] == "长期股权投资":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C17"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C17"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D17"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D17"]').send_keys(d2)
                                        if data[1] == "固定资产原价":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C18"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C18"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D18"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D18"]').send_keys(d2)
                                        if data[1] == "减:累计折旧":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C19"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C19"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D19"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D19"]').send_keys(d2)
                                        if data[1] == "在建工程":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C21"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C21"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D21"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D21"]').send_keys(d2)
                                        if data[1] == "工程物资":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C22"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C22"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D22"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D22"]').send_keys(d2)
                                        if data[1] == "固定资产清理":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C23"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C23"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D23"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D23"]').send_keys(d2)
                                        if data[1] == "生产性生物资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C24"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C24"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D24"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D24"]').send_keys(d2)
                                        if data[1] == "无形资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C25"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C25"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D25"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D25"]').send_keys(d2)
                                        if data[1] == "实收资本(或股本)":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G25"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G25"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H25"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H25"]').send_keys(d2)
                                        if data[1] == "开发支出":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C26"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C26"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D26"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D26"]').send_keys(d2)
                                        if data[1] == "资本公积":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G26"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G26"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H26"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H26"]').send_keys(d2)
                                        if data[1] == "长期待摊费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C27"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D27"]').send_keys(d2)
                                        if data[1] == "盈余公积":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G27"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H27"]').send_keys(d2)
                                        if data[1] == "其他非流动资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001C28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001C28"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001D28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D28"]').send_keys(d2)
                                        if data[1] == "未分配利润":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001G28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001G28"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001H28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001H28"]').send_keys(d2)
                                    browser.execute_script(
                                        "window.scrollTo(0,-document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;return lenOfPage")
                                    time.sleep(0.5)
                                    browser.find_element_by_id('mini-1$2').click()
                                    time.sleep(0.5)
                                    for data in lrdata:
                                        if data[1] == "减：所得税费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G31"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G31"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J31"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J31"]').send_keys(d2)
                                        if data[1] == "税收滞纳金":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G29"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G29"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J29"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J29"]').send_keys(d2)
                                        if data[1] == "自然灾害等不可抗力因素造成的损失":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G28"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J28"]').send_keys(d2)
                                        if data[1] == "无法收回的长期股权投资损失":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G27"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J27"]').send_keys(d2)
                                        if data[1] == "无法收回的长期债券投资损失":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G26"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G26"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J26"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J26"]').send_keys(d2)
                                        if data[1] == "其中：坏账损失":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G25"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G25"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J25"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J25"]').send_keys(d2)
                                        if data[1] == "减：营业外支出":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G24"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G24"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J24"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J24"]').send_keys(d2)
                                        if data[1] == "其中：政府补助":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G23"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G23"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J23"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J23"]').send_keys(d2)
                                        if data[1] == "加：营业外收入":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G22"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G22"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J22"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J22"]').send_keys(d2)
                                        if data[1] == "加：投资收益（损失以\" - \"号填列）":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G20"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G20"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J20"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J20"]').send_keys(d2)
                                        if data[1] == "其中：利息费用（收入以\" - \"号填列）":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G19"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G19"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J19"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J19"]').send_keys(d2)
                                        if data[1] == "财务费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G18"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G18"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J18"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J18"]').send_keys(d2)
                                        if data[1] == "研究费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G17"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G17"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J17"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J17"]').send_keys(d2)
                                        if data[1] == "业务招待费":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G16"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G16"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J16"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J16"]').send_keys(d2)
                                        if data[1] == "其中：开办费":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G15"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G15"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J15"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J15"]').send_keys(d2)
                                        if data[1] == "管理费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G14"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G14"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J14"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J14"]').send_keys(d2)
                                        if data[1] == "广告费和业务宣传费":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G13"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G13"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J13"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J13"]').send_keys(d2)
                                        if data[1] == "其中：商品维修费":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G12"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G12"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J12"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J12"]').send_keys(d2)
                                        if data[1] == "销售费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G11"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G11"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J11"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J11"]').send_keys(d2)
                                        if data[1] == "教育费附加、矿产资源补偿费、排污费":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G10"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J10"]').send_keys(d2)
                                        if data[1] == "城镇土地使用税、房产税、车船税、印花税":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G9"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J9"]').send_keys(d2)
                                        if data[1] == "土地增值税":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G8"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J8"]').send_keys(d2)
                                        if data[1] == "资源税":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G7"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J7"]').send_keys(d2)
                                        if data[1] == "城市维护建设税":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G6"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J6"]').send_keys(d2)
                                        if data[1] == "营业税":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G5"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J5"]').send_keys(d2)
                                        if data[1] == "其中：消费税":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G4"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J4"]').send_keys(d2)
                                        if data[1] == "营业税金及附加":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="003G3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="003G3"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="003J3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="003J3"]').send_keys(d2)
                                        if data[1] == "减：营业成本":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G2"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J2"]').send_keys(d2)
                                        if data[1] == "一、营业收入":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002G1"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002G1"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002J1"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002J1"]').send_keys(d2)
                                if self.acclaw == "NORMAL":
                                    for data in fzdata:
                                        if data[1] == "实收资本(或股本)":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J27"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K27"]').send_keys(d2)
                                        if data[1] == "商誉":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D28"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E28"]').send_keys(d2)
                                        if data[1] == "资本公积":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J28"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K28"]').send_keys(d2)
                                        if data[1] == "长期待摊费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D29"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D29"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E29"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E29"]').send_keys(d2)
                                        if data[1] == "减：库存股":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J29"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J29"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K29"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K29"]').send_keys(d2)
                                        if data[1] == "递延所得税资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D30"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D30"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E30"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E30"]').send_keys(d2)
                                        if data[1] == "其他综合收益":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J30"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J30"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K30"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K30"]').send_keys(d2)
                                        if data[1] == "其他非流动资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D31"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D31"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E31"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E31"]').send_keys(d2)
                                        if data[1] == "盈余公积":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J31"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J31"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K31"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K31"]').send_keys(d2)
                                        if data[1] == "未分配利润":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J32"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J32"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K32"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K32"]').send_keys(d2)
                                        if data[1] == "货币资金":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D2"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E2"]').send_keys(d2)
                                        if data[1] == "短期借款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J2"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K2"]').send_keys(d2)
                                        if data[1] == "以公允价值计量且其变动计入当期损益的金融资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D3"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E3"]').send_keys(d2)
                                        if data[1] == "以公允价值计量且其变动计入当期损益的金融负债":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J3"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K3"]').send_keys(d2)
                                        if data[1] == "应收票据":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D4"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E4"]').send_keys(d2)
                                        if data[1] == "应付票据":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J4"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K4"]').send_keys(d2)
                                        if data[1] == "应收账款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D5"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E5"]').send_keys(d2)
                                        if data[1] == "应付账款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J5"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K5"]').send_keys(d2)
                                        if data[1] == "预付款项":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D6"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E6"]').send_keys(d2)
                                        if data[1] == "预收款项":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J6"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K6"]').send_keys(d2)
                                        if data[1] == "应收利息":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D7"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E7"]').send_keys(d2)
                                        if data[1] == "开发支出":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D27"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E27"]').send_keys(d2)
                                        if data[1] == "无形资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D26"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D26"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E26"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E26"]').send_keys(d2)
                                        if data[1] == "油气资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D25"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D25"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E25"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E25"]').send_keys(d2)
                                        if data[1] == "生产性生物资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D24"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D24"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E24"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E24"]').send_keys(d2)
                                        if data[1] == "其他非流动负债":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J23"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J23"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K23"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K23"]').send_keys(d2)
                                        if data[1] == "固定资产清理":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D23"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D23"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E23"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E23"]').send_keys(d2)
                                        if data[1] == "递延所得税负债":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J22"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J22"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K22"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K22"]').send_keys(d2)
                                        if data[1] == "工程物资":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D22"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D22"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E22"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E22"]').send_keys(d2)
                                        if data[1] == "递延收益":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J21"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J21"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K21"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K21"]').send_keys(d2)
                                        if data[1] == "在建工程":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D21"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D21"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E21"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E21"]').send_keys(d2)
                                        if data[1] == "预计负债":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J20"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J20"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K20"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K20"]').send_keys(d2)
                                        if data[1] == "固定资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D20"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D20"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E20"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E20"]').send_keys(d2)
                                        if data[1] == "专项应付款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J19"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J19"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K19"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K19"]').send_keys(d2)
                                        if data[1] == "投资性房地产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D19"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D19"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E19"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E19"]').send_keys(d2)
                                        if data[1] == "长期应付款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J18"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J18"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K18"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K18"]').send_keys(d2)
                                        if data[1] == "长期股权投资":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D18"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D18"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E18"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E18"]').send_keys(d2)
                                        if data[1] == "应付债券":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J17"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J17"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K17"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K17"]').send_keys(d2)
                                        if data[1] == "长期应收款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D17"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D17"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E17"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E17"]').send_keys(d2)
                                        if data[1] == "长期借款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J16"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J16"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K16"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K16"]').send_keys(d2)
                                        if data[1] == "持有至到期投资":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D16"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D16"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E16"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E16"]').send_keys(d2)
                                        if data[1] == "可供出售金融资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D15"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D15"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E15"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E15"]').send_keys(d2)
                                        if data[1] == "其他流动负债":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J13"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J13"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K13"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K13"]').send_keys(d2)
                                        if data[1] == "一年内到期的非流动负债":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J12"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J12"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K12"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K12"]').send_keys(d2)
                                        if data[1] == "其他流动资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D12"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D12"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E12"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E12"]').send_keys(d2)
                                        if data[1] == "其他应付款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J11"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J11"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K11"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K11"]').send_keys(d2)
                                        if data[1] == "一年内到期的非流动资产":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D11"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D11"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E11"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E11"]').send_keys(d2)
                                        if data[1] == "应付股利":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J10"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K10"]').send_keys(d2)
                                        if data[1] == "存货":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D10"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E10"]').send_keys(d2)
                                        if data[1] == "应付利息":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J9"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K9"]').send_keys(d2)
                                        if data[1] == "其他应收款":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D9"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E9"]').send_keys(d2)
                                        if data[1] == "应交税费":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J8"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K8"]').send_keys(d2)
                                        if data[1] == "应收股利":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001D8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001D8"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001E8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001E8"]').send_keys(d2)
                                        if data[1] == "应付职工薪酬":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="001J7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001J7"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="001K7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="001K7"]').send_keys(d2)
                                    browser.execute_script(
                                        "window.scrollTo(0,-document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;return lenOfPage")
                                    time.sleep(0.5)
                                    browser.find_element_by_id('mini-1$2').click()
                                    time.sleep(0.5)
                                    for data in lrdata:
                                        if data[1] == "(二)稀释每股收益":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E32"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E32"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F32"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F32"]').send_keys(d2)
                                        if data[1] == "(一)基本每股收益":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E31"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E31"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F31"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F31"]').send_keys(d2)
                                        if data[1] == "5.外币财务报表折算差额":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E28"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F28"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F28"]').send_keys(d2)
                                        if data[1] == "4.现金流经套期损益的有效部分":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E27"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F27"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F27"]').send_keys(d2)
                                        if data[1] == "3.将有至到期投资重分类可供出售金融资产损益":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E26"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E26"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F26"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F26"]').send_keys(d2)
                                        if data[1] == "2.可供出售金融资产公允价值变动损益":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E25"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E25"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F25"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F25"]').send_keys(d2)
                                        if data[1] == "1.权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E24"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E24"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F24"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F24"]').send_keys(d2)
                                        if data[1] == "2.权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E22"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E22"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F22"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F22"]').send_keys(d2)
                                        if data[1] == "1.重新计量设定收益计划净负债或净资产的变动":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E21"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E21"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F21"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F21"]').send_keys(d2)
                                        if data[1] == "减：所得税费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E17"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E17"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F17"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F17"]').send_keys(d2)
                                        if data[1] == "其中：非流动资产处置损失":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E15"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E15"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F15"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F15"]').send_keys(d2)
                                        if data[1] == "减：营业外支出":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E14"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E14"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F14"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F14"]').send_keys(d2)
                                        if data[1] == "其中：非流动资产处置利得":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E13"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E13"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F13"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F13"]').send_keys(d2)
                                        if data[1] == "加：营业外收入":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E12"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E12"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F12"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F12"]').send_keys(d2)
                                        if data[1] == "其中：对联营企业和合营企业的投资收益":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E10"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F10"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F10"]').send_keys(d2)
                                        if data[1] == "投资收益(损失以\"－\"号填列)":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E9"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F9"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F9"]').send_keys(d2)
                                        if data[1] == "加：公允价值变动收益(损失以“-”号填列)":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E8"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F8"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F8"]').send_keys(d2)
                                        if data[1] == "资产减值损失":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E7"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F7"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F7"]').send_keys(d2)
                                        if data[1] == "财务费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E6"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F6"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F6"]').send_keys(d2)
                                        if data[1] == "管理费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E5"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F5"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F5"]').send_keys(d2)
                                        if data[1] == "销售费用":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E4"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F4"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F4"]').send_keys(d2)
                                        if data[1] == "营业税金及附加":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E3"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F3"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F3"]').send_keys(d2)
                                        if data[1] == "减：营业成本":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E2"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F2"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F2"]').send_keys(d2)
                                        if data[1] == "一、营业收入":
                                            d1 = str(data[2].quantize(Decimal('0.00')))
                                            d2 = str(data[3].quantize(Decimal('0.00')))
                                            browser.find_element_by_xpath('//input[@id="002E1"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002E1"]').send_keys(d1)
                                            browser.find_element_by_xpath('//input[@id="002F1"]').clear()
                                            browser.find_element_by_xpath('//input[@id="002F1"]').send_keys(d2)
                                browser.execute_script('document.title="国税-财务报表"')
                                browser.switch_to_window(shouye)
                                break
                    except Exception as e:
                        self.logger.info(e)
                a += 1
            all = browser.window_handles
            c = browser.current_window_handle
            for cc in all:
                if cc != c:
                    browser.switch_to_window(cc)

        if self.taxtype == '财务报表年报':
            for i in judge:
                xgm = i.xpath('.//text()')
                if '企业财务报表-年报' in xgm[2] and '申报' in xgm:
                    try:
                        gsrq = xgm[5]
                        gsrq = re.search(r'(.*?)~(.*)', gsrq)
                        gsks = gsrq.group(1)
                        gsjs = gsrq.group(2)
                        browser.find_element_by_xpath(
                            '//*[@class="J_sbxx-tbody"]/tr[{}]//a[@class="opBtn"]'.format(a)).click()
                        allwins = browser.window_handles
                        shouye = browser.current_window_handle
                        for window in allwins:
                            if window != shouye:
                                browser.switch_to_window(allwins[-1])
                                cwbb = window
                                browser.execute_script('document.title="国税-财务报表年报"')
                                browser.switch_to_window(shouye)
                                break
                    except Exception as e:
                        self.logger.info(e)
                a += 1
            all = browser.window_handles
            c = browser.current_window_handle
            for cc in all:
                if cc != c:
                    browser.switch_to_window(cc)

        if self.taxtype == '地税三项':
            try:
                wait = ui.WebDriverWait(browser, 8)
                ds_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/djsxx.html'
                browser.get(url=ds_url)
                try:
                    wait.until(lambda browser: browser.find_element_by_css_selector("#mini-29 .mini-button-text"))
                    browser.find_element_by_css_selector("#mini-29 .mini-button-text").click()
                except Exception as e:
                    print(e)
                    print("弹出框与预设不一致")
                try:
                    browser.find_element_by_css_selector("#mini-27 .mini-button-text").click()
                except Exception as e:
                    print(e)
                    print("弹出框与预设不一致")
                browser.find_element_by_xpath("//a[@href='javascript:gotoDs()']").click()
                time.sleep(3)
                windows = browser.window_handles
                window1 = browser.current_window_handle
                for c_window in windows:
                    if c_window != window1:
                        browser.close()
                        browser.switch_to_window(windows[-1])
                        break
                time.sleep(1)
                browser.find_element_by_css_selector('#layui-layer1 div.layui-layer-btn a').click()
                browser.switch_to_frame('qyIndex')
                wait.until(lambda browser: browser.find_element_by_css_selector("#menu3_3_102001"))
                browser.find_element_by_css_selector('#menu3_3_102001').click()
                browser.switch_to_frame('qymain')
                time.sleep(2)
                dspage = browser.page_source
                dsroot = etree.HTML(dspage)
                dsjudge = dsroot.xpath('//*[@id="tbody"]/tr')
                b = 1
                for i in dsjudge:
                    xgm = i.xpath('.//text()')
                    if '自行申报' in xgm and '我要申报' in xgm:
                        ssrq = browser.find_element_by_xpath('//*[@id="tbody"]/tr[{}]/td[3]'.format(b)).text
                        rq = re.search(r'(.*?)至(.*)', ssrq)
                        ks = rq.group(1)
                        js = rq.group(2)
                        browser.find_element_by_xpath('//*[@id="tbody"]/tr[{}]/td[7]/a'.format(b)).click()
                        browser.find_element_by_css_selector("#confirmSbBtn").click()
                        browser.execute_script('document.title="地税-地税三项"')
                        break
            except Exception as e:
                self.logger.info(e)

        if self.taxtype == '个人所得税':
            try:
                wait = ui.WebDriverWait(browser, 8)
                ds_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/djsxx.html'
                browser.get(url=ds_url)
                try:
                    wait.until(lambda browser: browser.find_element_by_css_selector("#mini-29 .mini-button-text"))
                    browser.find_element_by_css_selector("#mini-29 .mini-button-text").click()
                except Exception as e:
                    print(e)
                    print("弹出框与预设不一致")
                try:
                    browser.find_element_by_css_selector("#mini-27 .mini-button-text").click()
                except Exception as e:
                    print(e)
                    print("弹出框与预设不一致")
                browser.find_element_by_xpath("//a[@href='javascript:gotoDs()']").click()
                time.sleep(3)
                windows = browser.window_handles
                window1 = browser.current_window_handle
                for c_window in windows:
                    if c_window != window1:
                        browser.close()
                        browser.switch_to_window(windows[-1])
                        break
                time.sleep(1)
                browser.find_element_by_css_selector('#layui-layer1 div.layui-layer-btn a').click()
                browser.switch_to_frame('qyIndex')
                wait.until(lambda browser: browser.find_element_by_css_selector("#menu3_3_102001"))
                browser.find_element_by_css_selector('#menu3_3_102001').click()
                browser.switch_to_frame('qymain')
                time.sleep(2)
                dspage = browser.page_source
                dsroot = etree.HTML(dspage)
                dsjudge = dsroot.xpath('//*[@id="tbody"]/tr')
                b = 1
                for i in dsjudge:
                    xgm = i.xpath('.//text()')
                    if '自行申报' in xgm and '我要申报' in xgm and '个人所得税' in xgm:
                        ssrq = browser.find_element_by_xpath('//*[@id="tbody"]/tr[{}]/td[3]'.format(b)).text
                        rq = re.search(r'(.*?)至(.*)', ssrq)
                        ks = rq.group(1)
                        js = rq.group(2)
                        browser.find_element_by_xpath('//*[@id="tbody"]/tr[{}]/td[7]/a'.format(b)).click()
                        browser.find_element_by_css_selector("#confirmSbBtn").click()
                        browser.execute_script('document.title="地税-个人所得税"')
                        break
            except Exception as e:
                self.logger.info(e)

    def shuizhongchaxun(self, browser):
        if self.taxtype == '增值税' or self.taxtype == "全部":
            browser.find_element_by_css_selector("#sz .mini-buttonedit-input").clear()
            browser.find_element_by_css_selector("#sz .mini-buttonedit-input").send_keys("增值税")
            shuiming = "增值税"
            self.parse_biaoge(browser, shuiming)
            browser.execute_script('document.title="国税-增值税"')

        if self.taxtype == '财务报表' or self.taxtype == "全部" or self.taxtype == '财务报表年报':
            newwindow = 'window.open("http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/cxdy/sbcx.html")'
            browser.execute_script(newwindow)
            all = browser.window_handles
            curr = browser.current_window_handle
            for window in all:
                if window != curr:
                    browser.switch_to_window(all[-1])
                    break
            browser.find_element_by_css_selector("#sz .mini-buttonedit-input").clear()
            browser.find_element_by_css_selector("#sz .mini-buttonedit-input").send_keys("财务报表")
            shuiming = "财务报表"
            self.parse_biaoge(browser, shuiming)
            browser.execute_script('document.title="国税-财务报表"')

        if self.taxtype == '企业所得税' or self.taxtype == "全部":
            newwindow = 'window.open("http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/cxdy/sbcx.html")'
            browser.execute_script(newwindow)
            all = browser.window_handles
            curr = browser.current_window_handle
            for window in all:
                if window != curr:
                    browser.switch_to_window(all[-1])
                    break
            browser.find_element_by_css_selector("#sz .mini-buttonedit-input").clear()
            browser.find_element_by_css_selector("#sz .mini-buttonedit-input").send_keys("所得税")
            shuiming = "所得税"
            self.parse_biaoge(browser, shuiming)
            browser.execute_script('document.title="国税-企业所得税"')

    def parse_biaoge(self, browser, shuiming):
        self.logger.info("截取国税{}申报信息".format(shuiming))
        wait = ui.WebDriverWait(browser, 10)
        wait.until(lambda browser: browser.find_element_by_css_selector("#sbrqq .mini-buttonedit-input"))
        year = self.periodyear
        month = self.periodmonth
        days = self.days
        qsrq = '{}{}01'.format(year, month)
        zzrq = '{}{}{}'.format(year, month, days)
        browser.get(url='http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/cxdy/sbcx.html')
        browser.find_element_by_css_selector("#sz .mini-buttonedit-input").clear()
        browser.find_element_by_css_selector("#sz .mini-buttonedit-input").send_keys("{}".format(shuiming))
        browser.find_element_by_css_selector("#sbrqq .mini-buttonedit-input").clear()
        browser.find_element_by_css_selector("#sbrqq .mini-buttonedit-input").send_keys(qsrq)
        browser.find_element_by_css_selector("#sbrqz .mini-buttonedit-input").clear()
        browser.find_element_by_css_selector("#sbrqz .mini-buttonedit-input").send_keys(zzrq)
        browser.find_element_by_css_selector("#stepnext .mini-button-text").click()

    def qwds(self, browser):
        newwindow = 'window.open("http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/cxdy/sbcx.html")'
        browser.execute_script(newwindow)
        all = browser.window_handles
        curr = browser.current_window_handle
        for window in all:
            if window != curr:
                browser.switch_to_window(all[-1])
                break
        wait = ui.WebDriverWait(browser, 8)
        ds_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/djsxx.html'
        browser.get(url=ds_url)
        try:
            wait.until(lambda browser: browser.find_element_by_css_selector("#mini-29 .mini-button-text"))
            browser.find_element_by_css_selector("#mini-29 .mini-button-text").click()
        except Exception as e:
            print(e)
            print("弹出框与预设不一致")
        try:
            browser.find_element_by_css_selector("#mini-27 .mini-button-text").click()
        except Exception as e:
            print(e)
            print("弹出框与预设不一致")
        browser.find_element_by_xpath("//a[@href='javascript:gotoDs()']").click()
        time.sleep(3)
        windows = browser.window_handles
        window1 = browser.current_window_handle
        for c_window in windows:
            if c_window != window1:
                browser.close()
                browser.switch_to_window(windows[-1])
                break
        cont = browser.page_source
        if "地方税务局" in cont:
            # 个人
            newwindow = 'window.open("https://dzswj.szds.gov.cn/dzswj/sbxxcx.do?method=toSbxxCx&qyyhDzswjRandomNum=0.9806496945471579")'
            browser.execute_script(newwindow)
            windows = browser.window_handles
            window1 = browser.current_window_handle
            for c_window in windows:
                if c_window != window1:
                    # browser.close()
                    browser.switch_to_window(windows[-1])
                    break
            if self.taxtype == '全部' or self.taxtype == '个人所得税':
                self.dishuicx(browser)
                browser.execute_script('document.title="地税-个人所得税"')

            # 地税三项
            if self.taxtype == '全部' or self.taxtype == '地税三项':
                newwindow = 'window.open("https://dzswj.szds.gov.cn/dzswj/sbxxcx.do?method=toSbxxCx&qyyhDzswjRandomNum=0.9806496945471579")'
                browser.execute_script(newwindow)
                windows = browser.window_handles
                window1 = browser.current_window_handle
                for c_window in windows:
                    if c_window != window1:
                        browser.switch_to_window(windows[-1])
                        break
                self.dishuisx(browser)
                browser.execute_script('document.title="地税-地税三项"')

    def dishuicx(self, browser):
        wait = ui.WebDriverWait(browser, 8)
        wait.until(lambda browser: browser.find_element_by_css_selector('#sbqq'))
        time.sleep(0.5)
        browser.find_element_by_css_selector('#zsxmDm').find_element_by_xpath(
            '//option[@value="10106"]').click()  # 选择个人所得税
        sb_startd = browser.find_element_by_css_selector('#sbqq')
        sb_startd.clear()
        sb_startd.send_keys('{}-{}-01'.format(self.periodyear, self.periodmonth))
        sb_endd = browser.find_element_by_css_selector('#sbqz')
        sb_endd.clear()
        sb_endd.send_keys('{}-{}-{}'.format(self.periodyear, self.periodmonth, self.days))
        # time.sleep(1)
        browser.find_element_by_css_selector('#query').click()

    def dishuisx(self, browser):
        wait = ui.WebDriverWait(browser, 8)
        wait.until(lambda browser: browser.find_element_by_css_selector('#sbqq'))
        browser.find_element_by_css_selector('#zsxmDm').find_element_by_xpath(
            '//option[@value="10109"]').click()  # 选择城市建设税
        sb_startd = browser.find_element_by_css_selector('#sbqq')
        sb_startd.clear()
        sb_startd.send_keys('{}-{}-01'.format(self.periodyear, self.periodmonth))
        sb_endd = browser.find_element_by_css_selector('#sbqz')
        sb_endd.clear()
        sb_endd.send_keys('{}-{}-{}'.format(self.periodyear, self.periodmonth, self.days))
        # time.sleep(1)
        browser.find_element_by_css_selector('#query').click()

    def parse_jiaokuan(self, browser):
        browser.find_element_by_css_selector("#sssqq .mini-buttonedit-input").clear()
        browser.find_element_by_css_selector("#sssqq .mini-buttonedit-input").send_keys(
            '{}{}01'.format(self.periodyear, self.periodmonth))
        browser.find_element_by_css_selector("#sssqz .mini-buttonedit-input").clear()
        browser.find_element_by_css_selector("#sssqz .mini-buttonedit-input").send_keys(
            '{}{}{}'.format(self.periodyear, self.periodmonth, self.days))
        try:
            browser.find_element_by_css_selector("#mini-37 .mini-button-text").click()
        except Exception as e:
            self.logger.info(e)
            print("没有弹窗")
        wait = ui.WebDriverWait(browser, 10)
        wait.until(lambda browser: browser.find_element_by_css_selector("#stepnext .mini-button-text"))
        browser.find_element_by_css_selector("#stepnext .mini-button-text").click()
        browser.execute_script('document.title="国税-已缴款"')

    def dsjkcx(self, browser):
        wait = ui.WebDriverWait(browser, 8)
        wait = ui.WebDriverWait(browser, 8)
        ds_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/djsxx.html'
        browser.get(url=ds_url)
        try:
            wait.until(lambda browser: browser.find_element_by_css_selector("#mini-29 .mini-button-text"))
            browser.find_element_by_css_selector("#mini-29 .mini-button-text").click()
        except Exception as e:
            print(e)
            print("弹出框与预设不一致")
        try:
            browser.find_element_by_css_selector("#mini-27 .mini-button-text").click()
        except Exception as e:
            print(e)
            print("弹出框与预设不一致")
        browser.find_element_by_xpath("//a[@href='javascript:gotoDs()']").click()
        time.sleep(3)
        windows = browser.window_handles
        window1 = browser.current_window_handle
        for c_window in windows:
            if c_window != window1:
                browser.close()
                browser.switch_to_window(windows[-1])
                break
        cont = browser.page_source
        if "地方税务局" in cont:
            newwindow = 'window.open("https://dzswj.szds.gov.cn/dzswj/yjkxxcx.do?method=init&qyyhDzswjRandomNum=0.26304088553508564")'
            browser.execute_script(newwindow)
            windows = browser.window_handles
            window1 = browser.current_window_handle
            for c_window in windows:
                if c_window != window1:
                    # browser.close()
                    browser.switch_to_window(windows[-1])
                    break
            wait = ui.WebDriverWait(browser, 10)
            wait.until(lambda browser: browser.find_element_by_css_selector('#jkqq'))
            ds_start_date = browser.find_element_by_xpath('//*[@id="jkqq"]')
            ds_start_date.clear()
            ds_start_date.send_keys('{}-{}-01'.format(self.periodyear, self.periodmonth))
            ds_end_date = browser.find_element_by_xpath("//*[@id='jkqz']")
            ds_end_date.clear()
            ds_end_date.send_keys('{}-{}-{}'.format(self.periodyear, self.periodmonth, self.days))
            browser.find_element_by_css_selector('#query').click()
            browser.execute_script('document.title="地税-已缴款"')
        else:
            self.logger.info("地税进入失败")

    def excute_spider(self):
        try:
            cookies = self.login()
            jsoncookies = json.dumps(cookies, ensure_ascii=False)
            if "账号和密码不匹配" in jsoncookies:
                self.logger.warn("账号和密码不匹配")
                return
            with open('cookies/cookies.json', 'w') as f:  # 将login后的cookies提取出来
                f.write(jsoncookies)
                f.close()
        except Exception as e:
            self.logger.warn(e)
            self.logger.warn("登陆失败")
            return False
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('disable-infobars')
            options.add_argument("--start-maximized")
            sysname = platform.platform()
            if "XP" in sysname or "xp" in sysname:
                browser = webdriver.Chrome(executable_path='chromedriver_xp.exe', chrome_options=options)  # 添加driver的路径
            else:
                browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)  # 添加driver的路径
        except Exception as e:
            self.logger.warn(e)
            return False
        index_url = "http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html"
        browser.get(url=index_url)
        browser.delete_all_cookies()
        with open('cookies/cookies.json', 'r', encoding='utf8') as f:
            cookielist = json.loads(f.read())
        for (k, v) in cookielist.items():
            browser.add_cookie({
                'domain': '.szgs.gov.cn',  # 此处xxx.com前，需要带点
                'name': k,
                'value': v,
                'path': '/',
                'expires': None})
        browser.get(url="http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html")
        time.sleep(3)
        page = browser.page_source
        if self.opertype == 'APPLY':
            try:
                self.apply(browser)
                return browser
            except Exception as e:
                self.logger.info("apply失败")
                self.logger.warn(e)
                return browser

        elif self.opertype == 'APPLYSEARCH':
            if self.taxtype == '全部':
                try:  # 查询
                    shenbao_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/cxdy/sbcx.html'
                    browser.get(url=shenbao_url)
                    time.sleep(3)
                    self.shuizhongchaxun(browser)
                except Exception as e:
                    self.logger.info("customerid:{}GSYCX出错".format(self.customerid))
                    self.logger.warn(e)
                    self.logger.info("国税已申报查询失败")
                    return browser

                try:  # 查询
                    self.qwds(browser)
                    return browser
                except Exception as e:
                    self.logger.warn(e)
                    self.logger.info("地税查询失败")
                    return browser
            if self.taxtype == '增值税' or self.taxtype == '企业所得税' or self.taxtype == '财务报表' or self.taxtype == '财务报表年报':
                try:  # 查询
                    shenbao_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/cxdy/sbcx.html'
                    browser.get(url=shenbao_url)
                    time.sleep(3)
                    self.shuizhongchaxun(browser)
                    return browser
                except Exception as e:
                    self.logger.info("customerid:{}GSYCX出错".format(self.customerid))
                    self.logger.warn(e)
                    self.logger.info("国税已申报查询失败")
                    return browser
            if self.taxtype == '地税三项' or self.taxtype == '个人所得税':
                try:  # 查询
                    self.qwds(browser)
                    return browser
                except Exception as e:
                    self.logger.warn(e)
                    self.logger.info("地税查询失败")
                    return browser


        elif self.opertype == 'PAYSEARCH':
            if self.taxtype == '全部':
                try:
                    # 国税缴款查询
                    jk_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/jk_jsxxcx.html'
                    browser.get(url=jk_url)
                    self.parse_jiaokuan(browser)
                except Exception as e:
                    self.logger.warn(e)
                    return browser
                try:
                    # 地税缴款查询
                    newwindow = 'window.open("http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html")'
                    browser.execute_script(newwindow)
                    all = browser.window_handles
                    curr = browser.current_window_handle
                    for window in all:
                        if window != curr:
                            browser.switch_to_window(all[-1])
                            break
                    self.dsjkcx(browser)
                    return browser
                except Exception as e:
                    self.logger.warn(e)
                    return browser
            elif self.taxtype == '增值税' or self.taxtype == '企业所得税':
                try:
                    # 国税缴款查询
                    jk_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/jk_jsxxcx.html'
                    browser.get(url=jk_url)
                    self.parse_jiaokuan(browser)
                    return browser
                except Exception as e:
                    self.logger.warn(e)
                    return browser
            elif self.taxtype == '地税三项' or self.taxtype == '个人所得税':
                try:
                    # 地税缴款查询
                    newwindow = 'window.open("http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html")'
                    browser.execute_script(newwindow)
                    all = browser.window_handles
                    curr = browser.current_window_handle
                    for window in all:
                        if window != curr:
                            browser.switch_to_window(all[-1])
                            break
                    self.dsjkcx(browser)
                    return browser
                except Exception as e:
                    self.logger.warn(e)
                    return browser


logger = create_logger()
ksbs = ksbs(logger)
browser = ksbs.excute_spider()
sys.exit()

# while True:
#     time.sleep(3600)
while True:
    try:
        page = browser.page_source
    except Exception as e:
        logger.info(e)
        sys.exit()
