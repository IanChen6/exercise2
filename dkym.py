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
import base64
import decimal
import calendar
import hashlib
import json
import platform
import random
from decimal import *
from urllib.parse import urlparse, parse_qs
import queue
import execjs
import requests
from requests.adapters import HTTPAdapter
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

from urllib3 import Retry


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
        try:
            self.bookid = mess['bookid']
            self.applyyear = mess['applyyear']
            self.applymonth = mess['applymonth']
            self.acclaw = mess['acclaw']
            self.Companyid = mess['CompanyID']
        except:
            pass
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
    def get_js(self):
        # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
        # f = open("/home/mycode/localcredit/cdata.js", 'r', encoding='UTF-8')
        f = open("cdata.js", 'r', encoding='UTF-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr
    def tagger(self, tupian, md):
        while True:
            # formdata = {'CompanyID': 123456, 'BatchID': "1215454545", 'JobName': "pyj", 'CodeMD5': md, 'CodeData': tupian}
            # resp=requests.get(url="http://192.168.18.101:1421/SZYZService.asmx?wsdl",data=formdata)
            try:
                client = suds.client.Client(url="http://39.108.112.203:8701/SZYZService.asmx?wsdl")
                # client = suds.client.Client(url="http://192.168.18.101:1421/SZYZService.asmx?wsdl")
                auto = client.service.GetYZCodeForDll(tupian)
                if auto is not None:
                    result1 = str(auto)
                    return result1
                if auto is None:
                    return auto
                # result = client.service.SetYZImg(123456, "1215454545", "pyj", md, tupian)
                # # flag = login("91440300MA5DRRFB45", "10284784", result)
                # for i in range(30):
                #     result1 = client.service.GetYZCode(md)
                #     if result1 is not None:
                #         result1 = str(result1)
                #         return result1
                #     time.sleep(10)
            except Exception as e:
                self.logger.warn(e)
            break

    def login(self):
        try_times = 0
        user = self.user
        have_backup = True
        while try_times <= 20:
            self.logger.info('customerid:{},开始尝试登陆'.format(self.customerid))
            try_times += 1
            if try_times > 10:
                time.sleep(2)
            session = requests.session()
            # proxy_list = get_all_proxie()
            # proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]
            proxy_list = [
                {'http': 'http://112.74.37.197:6832', 'https': 'http://112.74.37.197:6832'},
                {'http': 'http://120.77.147.59:6832', 'https': 'http://120.77.147.59:6832'},
                {'http': 'http://120.79.188.47:6832', 'https': 'http://120.79.188.47:6832'},
                {'http': 'http://120.79.190.239:6832', 'https': 'http://120.79.190.239:6832'},
                {'http': 'http://39.108.220.10:6832', 'https': 'http://39.108.220.10:6832'},
                {'http': 'http://47.106.138.4:6832', 'https': 'http://47.106.138.4:6832'},
                {'http': 'http://47.106.142.153:6832', 'https': 'http://47.106.142.153:6832'},
                {'http': 'http://47.106.146.171:6832', 'https': 'http://47.106.146.171:6832'},
                {'http': 'http://47.106.136.116:6832', 'https': 'http://47.106.136.116:6832'},
                {'http': 'http://47.106.135.170:6832', 'https': 'http://47.106.135.170:6832'},
                {'http': 'http://47.106.137.245:6832', 'https': 'http://47.106.137.245:6832'},
                {'http': 'http://47.106.137.212:6832', 'https': 'http://47.106.137.212:6832'},
                {'http': 'http://39.108.167.244:6832', 'https': 'http://39.108.167.244:6832'},
                {'http': 'http://47.106.146.3:6832', 'https': 'http://47.106.146.3:6832'},
                {'http': 'http://47.106.128.33:6832', 'https': 'http://47.106.128.33:6832'}
            ]
            proxy = proxy_list[random.randint(0, 14)]
            session.proxies = proxy
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
            # logger.info("customerid:{},:{}".format(self.customerid,tupian))
            tag = self.tagger(tupian, md)
            self.logger.info("customerid:{}，获取验证码为：{}".format(self.customerid, tag))
            if tag is None:
                continue
            jyjg = session.post(url='http://dzswj.szgs.gov.cn/api/checkClickTipCaptcha', data=tag)
            self.logger.info("customerid:{}，验证验证码{}".format(self.customerid, tag))
            time_l = time.localtime(int(time.time()))
            time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
            self.logger.info("customerid:{}，转换tag".format(self.customerid))
            tag = json.dumps(tag)
            self.logger.info("customerid:{}，转换tag完成".format(self.customerid))
            self.logger.info("customerid:{}，{},{},{},{}".format(self.customerid, self.user, self.jiami(), tag, time_l))
            login_data = '{"nsrsbh":"%s","nsrpwd":"%s","redirectURL":"","tagger":%s,"time":"%s"}' % (
                user, self.jiami(), tag, time_l)
            login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
            resp = session.post(url=login_url, data=login_data)
            self.logger.info(login_data)
            self.logger.info("customerid:{},成功post数据".format(self.customerid))
            # panduan=resp.json()['message']
            # self.logger(panduan)
            try:
                if "验证码正确" in jyjg.json()['message']:
                    if "登录成功" in resp.json()['message']:
                        print('登录成功')
                        self.logger.info('customerid:{}pass'.format(self.customerid))
                        cookies = {}
                        for (k, v) in zip(session.cookies.keys(), session.cookies.values()):
                            cookies[k] = v
                        return cookies
                    elif "账户和密码不匹配" in resp.json()['message'] or "不存在" in resp.json()['message'] or "已注销" in \
                            resp.json()['message']:
                        print('账号和密码不匹配')
                        self.logger.info('customerid:{}账号和密码不匹配'.format(self.customerid))
                        status = "账号和密码不匹配"
                        return status
                    else:
                        time.sleep(3)
            except Exception as e:
                self.logger.warn("customerid:{}登录失败".format(self.customerid))
            self.logger.warn("customerid:{}登录失败,开始重试".format(self.customerid))
        self.logger.warn("{}登陆失败".format(self.customerid))
        return False

    def apply(self, browser):
        try:
            browser.find_element_by_xpath('//a[@id="mini-36"]/span').click()
            browser.find_element_by_xpath('//a[@id="mini-34"]/span').click()
            browser.find_element_by_xpath('//a[@id="mini-9"]/span').click()
            browser.find_element_by_xpath('//a[@id="mini-7"]/span').click()
        except:
            print("系统正常")
        try:
            browser.find_element_by_css_selector('#mini-4 span').click()
        except:
            print("无弹窗")
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
                try:
                    browser.find_element_by_css_selector('#layui-layer1 div.layui-layer-btn a').click()
                except:
                    pass
                try:
                    browser.find_element_by_xpath('//*[@id="layui-layer4"]/div[3]/a').click()
                except:
                    pass
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
                                    slirun = {
                                        "一、营业收入": ("002G1", "002J1",), "减：营业成本": ("002G2", "002J2",),
                                        "营业税金及附加": ("003G3", "003J3",),
                                        "其中：消费税": ("002G4", "002J4",), "营业税": ("002G5", "002J5",),
                                        "城市维护建设税": ("002G6", "002J6",), "资源税": ("002G7", "002J7",),
                                        "土地增值税": ("002G8", "002J8",),
                                        "城镇土地使用税、房产税、车船税、印花税": ("002G9", "002J9",),
                                        "教育费附加、矿产资源补偿费、排污费": ("002G10", "002J10",),
                                        "销售费用": ("002G11", "002J11",),
                                        "其中：商品维修费": ("002G12", "002J12",), "广告费和业务宣传费": ("002G13", "002J13",),
                                        "管理费用": ("002G14", "002J14",),
                                        "其中：开办费": ("002G15", "002J15",), "业务招待费": ("002G16", "002J16",),
                                        "研究费用": ("002G17", "002J17",),
                                        "财务费用": ("002G18", "002J18",), "其中：利息费用（收入以\" - \"号填列）": ("002G19", "002J19",),
                                        "加：投资收益（损失以\" - \"号填列）": ("002G20", "002J20",),
                                        "加：营业外收入": ("002G22", "002J22",), "其中：政府补助": ("002G23", "002J23",),
                                        "减：营业外支出": ("002G24", "002J24",),
                                        "其中：坏账损失": ("002G25", "002J25",), "无法收回的长期债券投资损失": ("002G26", "002J26",),
                                        "无法收回的长期股权投资损失": ("002G27", "002J27",),
                                        "自然灾害等不可抗力因素造成的损失": ("002G28", "002J28",), "税收滞纳金": ("002G29", "002J29",),
                                        "减：所得税费用": ("002G31", "002J31",),
                                    }
                                    fuzhai = {
                                        "货币资金": ["001C1", "001D1"], "短期借款": ["001G1", "001H1"],
                                        "短期投资": ["001C2", "001D2"],
                                        "应付票据": ["001G2", "001H2"], "应收票据": ["001C3", "001D3"],
                                        "应付账款": ["001G3", "001H3"], "应收账款": ["001C4", "001D4"],
                                        "预收账款": ["001G4", "001H4"],
                                        "预付账款": ["001C5", "001D5"], "应付职工薪酬": ["001G5", "001H5"],
                                        "应收股利": ["001C6", "001D6"], "应交税费": ["001G6", "001H6"],
                                        "应收利息": ["001C7", "001D7"], "应付利息": ["001G7", "001H7"],
                                        "其他应收款": ["001C8", "001D8"], "应付利润": ["001G8", "001H8"],
                                        "存货": ["001C9", "001D9"], "其他应付款": ["001G9", "001H9"],
                                        "其中：原材料": ["001C10", "001D10"], "其他流动负债": ["001G10", "001H10"],
                                        "在产品": ["001C11", "001D11"],
                                        "库存商品": ["001C12", "001D12"],
                                        "周转材料": ["001C13", "001D13"], "长期借款": ["001G13", "001H13"],
                                        "其他流动资产": ["001C14", "001D14"],
                                        "长期应付款": ["001G14", "001H14"],
                                        "递延收益": ["001G15", "001H15"], "其他非流动负债": ["001G45", "001H45"],
                                        "长期债券投资": ["001C16", "001D16"],
                                        "长期股权投资": ["001C17", "001D17"], "固定资产原价": ["001C18", "001D18"],
                                        "减:累计折旧": ["001C19", "001D19"],
                                        "在建工程": ["001C21", "001D21"], "工程物资": ["001C22", "001D22"],
                                        "固定资产清理": ["001C23", "001D23"],
                                        "生产性生物资产": ["001C24", "001D24"], "无形资产": ["001C25", "001D25"],
                                        "实收资本(或股本)": ["001G25", "001H25"],
                                        "开发支出": ["001C26", "001D26"],
                                        "资本公积": ["001G26", "001H26"], "长期待摊费用": ["001C27", "001D27"],
                                        "盈余公积": ["001G27", "001H27"],
                                        "其他非流动资产": ["001C28", "001D28"], "未分配利润": ["001G28", "001H28"]
                                    }
                                    for data in fzdata:
                                        if data['cSysItemName'] in fuzhai.keys():
                                            d1 = str(data["nEnd"])
                                            d2 = str(data["nBeg"])
                                            zuobiao=fuzhai[data['cSysItemName']]
                                            if data["nEnd"] != 0:
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[0])).clear()
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[0])).send_keys(d1)
                                            if data["nBeg"] != 0:
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[1])).clear()
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[1])).send_keys(d2)
                                    browser.execute_script(
                                        "window.scrollTo(0,-document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;return lenOfPage")
                                    time.sleep(0.5)
                                    browser.find_element_by_id('mini-1$2').click()
                                    time.sleep(0.5)
                                    for data in lrdata:
                                        if data['cSysItemName'] in slirun.keys():
                                            d1 = str(data["nYear"])
                                            d2 = str(data["nSeason"])
                                            zuobiao=slirun[data['cSysItemName']]
                                            if data["nYear"] != 0:
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[0])).clear()
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[0])).send_keys(d1)
                                            if data["nSeason"] != 0:
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[1])).clear()
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[1])).send_keys(d2)

                                if self.acclaw == "NORMAL":
                                    nlirun = {
                                        "一、营业收入": ("002E1", "002F1",), "减：营业成本": ("002E2", "002F2",),
                                        "营业税金及附加": ("002E3", "002F3",),
                                        "销售费用": ("002E4", "002F4",), "管理费用": ("002E5", "002F5",),
                                        "财务费用": ("002E6", "002F6",), "资产减值损失": ("002E7", "002F7",),
                                        "加：公允价值变动收益(损失以“-”号填列)": ("002E8", "002F8",),
                                        "投资收益(损失以\"－\"号填列)": ("002E9", "002F9",),
                                        "其中：对联营企业和合营企业的投资收益": ("002E10", "002F10",), "加：营业外收入": ("002E12", "002F12",),
                                        "其中：非流动资产处置利得": ("002E13", "002F13",),
                                        "减：营业外支出": ("002E14", "002F14",), "其中：非流动资产处置损失": ("002E15", "002F15",),
                                        "减：所得税费用": ("002E17", "002F17",),
                                        "1.重新计量设定收益计划净负债或净资产的变动": ("002E21", "002F21",),
                                        "2.权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额": ("002E22", "002F22",),
                                        "1.权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额": ("002E24", "002F24",),
                                        "2.可供出售金融资产公允价值变动损益": ("002E25", "002F25",),
                                        "3.将有至到期投资重分类可供出售金融资产损益": ("002E26", "002F26",),
                                        "4.现金流经套期损益的有效部分": ("002E27", "002F27",),
                                        "5.外币财务报表折算差额": ("002E28", "002F28",), "(一)基本每股收益": ("002E31", "002F31",),
                                        "(二)稀释每股收益": ("002E32", "002F32",),
                                    }
                                    nfuzhai = {
                                        "货币资金": ("001D2", "001E2",), "短期借款": ("001J2", "001K2",),
                                        "以公允价值计量且其变动计入当期损益的金融资产": ("001D3", "001E3",),
                                        "以公允价值计量且其变动计入当期损益的金融负债": ("001J3", "001K3",), "应收票据": ("001D4", "001E4",),
                                        "应付票据": ("001J4", "001K4",),
                                        "应收账款": ("001D5", "001E5",),
                                        "应付账款": ("001J5", "001K5",), "预付款项": ("001D6", "001E6",),
                                        "预收款项": ("001J6", "001K6",), "应收利息": ("001D7", "001E7",),
                                        "应付职工薪酬": ("001J7", "001K7",), "应收股利": ("001D8", "001E8",),
                                        "应交税费": ("001J8", "001K8",), "其他应收款": ("001D9", "001E9",),
                                        "应付利息": ("001J9", "001K9",), "存货": ("001D10", "001E10",),
                                        "应付股利": ("001J10", "001K10",), "一年内到期的非流动资产": ("001D11", "001E11",),
                                        "其他应付款": ("001J11", "001K11",),
                                        "其他流动资产": ("001D12", "001E12",),
                                        "一年内到期的非流动负债": ("001J12", "001K12",), "其他流动负债": ("001J13", "001K13",),
                                        "可供出售金融资产": ("001D15", "001E15",),
                                        "持有至到期投资": ("001D16", "001E16",),
                                        "长期借款": ("001J16", "001K16",), "长期应收款": ("001D17", "001E17",),
                                        "应付债券": ("001J17", "001K17",),
                                        "长期股权投资": ("001D18", "001E18",),
                                        "长期应付款": ("001J18", "001K18",), "投资性房地产": ("001D19", "001E19",),
                                        "专项应付款": ("001J19", "001K19",),
                                        "固定资产": ("001D20", "001E20",),
                                        "预计负债": ("001J20", "001K20",), "在建工程": ("001D21", "001E21",),
                                        "递延收益": ("001J21", "001K21",),
                                        "工程物资": ("001D22", "001E22",),
                                        "递延所得税负债": ("001J22", "001K22",), "固定资产清理": ("001D23", "001E23",),
                                        "其他非流动负债": ("001J23", "001K23",),
                                        "生产性生物资产": ("001D24", "001E24",),
                                        "油气资产": ("001D25", "001E25",), "无形资产": ("001D26", "001E26",),
                                        "开发支出": ("001D27", "001E27",),
                                        "实收资本(或股本)": ("001J27", "001K27",),
                                        "商誉": ("001D28", "001E28",), "资本公积": ("001J28", "001K28",),
                                        "长期待摊费用": ("001D29", "001E29",),
                                        "减：库存股": ("001J29", "001K29",),
                                        "递延所得税资产": ("001D30", "001E30",), "其他综合收益": ("001J30", "001K30",),
                                        "其他非流动资产": ("001D31", "001E31",),
                                        "盈余公积": ("001J31", "001K31",), "未分配利润": ("001J32", "001K32",),
                                    }
                                    for data in fzdata:
                                        if data['cSysItemName'] in nfuzhai.keys():
                                            d1 = str(data["nEnd"])
                                            d2 = str(data["nBeg"])
                                            zuobiao=nfuzhai[data['cSysItemName']]
                                            if data["nEnd"] != 0:
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[0])).clear()
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[0])).send_keys(d1)
                                            if data["nBeg"] != 0:
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[1])).clear()
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[1])).send_keys(d2)
                                    browser.execute_script(
                                        "window.scrollTo(0,-document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;return lenOfPage")
                                    time.sleep(0.5)
                                    browser.find_element_by_id('mini-1$2').click()
                                    time.sleep(0.5)
                                    for data in lrdata:
                                        if data['cSysItemName'] in nlirun.keys():
                                            d1 = str(data["nYear"])
                                            d2 = str(data["nSeason"])
                                            zuobiao=nlirun[data['cSysItemName']]
                                            if data["nYear"] != 0:
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[0])).clear()
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[0])).send_keys(d1)
                                            if data["nSeason"] != 0:
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[1])).clear()
                                                browser.find_element_by_xpath('//input[@id="{}"]'.format(zuobiao[1])).send_keys(d2)
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
                try:
                    browser.find_element_by_xpath('//*[@id="layui-layer4"]/div[3]/a').click()
                except:
                    pass
                try:
                    browser.find_element_by_css_selector('#layui-layer1 div.layui-layer-btn a').click()
                except:
                    pass
                browser.switch_to_frame('qyIndex')
                wait.until(lambda browser: browser.find_element_by_css_selector("#menu3_3_102001"))
                for a in range(2):
                    browser.find_element_by_css_selector('#menu3_3_102001').click()
                    try:
                        browser.find_element_by_xpath('//*[@id="layui-layer3"]/div[3]/a').click()
                        browser.find_element_by_css_selector('#menu3_3_102001').click()
                    except:
                        break
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
                try:
                    browser.find_element_by_css_selector('#layui-layer1 div.layui-layer-btn a').click()
                except:
                    pass
                try:
                    browser.find_element_by_xpath('//*[@id="layui-layer4"]/div[3]/a').click()
                except:
                    pass
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
        try:
            browser.find_element_by_xpath('//*[@id="layui-layer4"]/div[3]/a').click()
        except:
            pass
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
        try:
            browser.find_element_by_xpath('//*[@id="layui-layer4"]/div[3]/a').click()
        except:
            pass
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
        try:
            browser.find_element_by_xpath('//*[@id="mini-33"]/span').click()
            browser.find_element_by_xpath('//*[@id="mini-31"]/span').click()
            browser.find_element_by_xpath('//*[@id="mini-6"]/span').click()
            browser.find_element_by_xpath('//*[@id="mini-4"]').click()
        except:
            pass
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
