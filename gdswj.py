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
import re
import decimal
import sys
from lxml import etree
import time
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support import ui
import pymssql
from selenium.webdriver.common.action_chains import ActionChains

with open('guangdong.txt', 'r', encoding='utf8') as f:
    mess = f.read()
    if mess.startswith(u'\ufeff'):
        mess = mess.encode('utf8')[3:].decode('utf8')
    mess = json.loads(mess)
    f.close()

zh = mess['zh']
pwd = mess['pwd']
companyid = "18282900"
batchid = mess['batchid']
companyname = mess['companyname']
def insert_db(sql, params):
    conn = pymssql.connect(host='main01', port='1433', user='python', password='pl,okmPL<OKM',
                           database='ACTCenter', charset='utf8')
    cur = conn.cursor()
    if not cur:
        raise Exception("数据库连接失败")
    len(params)
    cur.callproc(sql, params)
    conn.commit()
    cur.close()


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
    browser.get(
        url='http://gs.etax-gd.gov.cn/sso/login?service=http://gs.etax-gd.gov.cn/xxmh/html/index.html?bszmFrom=1&t=1479433265984')
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
except:
    try:
        print("浏览器启动异常")
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
            sys.exit()
        except Exception as e:
            print(e)
            sys.exit()
    try:
        if '欢迎您' in page:
            pass
    except:
        try:
            print("浏览器异常关闭")
            sys.exit()
        except Exception as e:
            print(e)
            sys.exit()
    if '欢迎您' in page:
        try:
            try:
                browser.find_element_by_xpath('//li[@id="liM1_sscx"]/a').click()
            except:
                print("系统正常")
            # 国税
            browser.switch_to_frame('ifrMain')
            time.sleep(0.5)
            browser.switch_to_frame('cxtable')
            time.sleep(1)
            browser.switch_to_frame('nsrxxIframe')
            page1 = browser.page_source
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
            if '基本信息' in data_dict.keys():
                d1 = {}
                get_data = data_dict["基本信息"]
                for i in range(0, len(get_data), 2):
                    d1[get_data[i][0]] = get_data[i + 1][0]
                    end = i + 1
                    endflag = len(get_data) - 1
                    if end >= endflag:
                        break
                data_dict["基本信息"] = d1

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
                data_dict["登记状态信息"] = d1

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
                data_dict["注册资本"] = d1

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
                data_dict["投资总额"] = d3

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
                data_dict["总分机构情况"] = d3
            print(data_dict)
            # insert_db('[dbo].[Python_Serivce_GSTaxGuangDong_Add]',
            #           (batchid, companyname, zh, pwd, json.dumps(data_dict, ensure_ascii=False)))
            info={}
            info['国税']=data_dict

            # 地税
            browser.switch_to_default_content()
            browser.switch_to_frame('ifrMain')
            time.sleep(0.1)
            browser.switch_to_frame('cxtable')
            time.sleep(0.1)
            browser.find_element_by_link_text('地税').click()
            time.sleep(5)
            browser.switch_to_frame('nsrxxIframe')
            page1 = browser.page_source
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
            if '基本信息' in data_dict.keys():
                d1 = {}
                get_data = data_dict["基本信息"]
                for i in range(0, len(get_data), 2):
                    d1[get_data[i][0]] = get_data[i + 1][0]
                    end = i + 1
                    endflag = len(get_data) - 1
                    if end >= endflag:
                        break
                data_dict["基本信息"] = d1

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
                data_dict["登记状态信息"] = d1

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
                data_dict["注册资本"] = d1

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
                data_dict["投资总额"] = d3

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
                data_dict["总分机构情况"] = d3
            print(data_dict)
            info['地税']=data_dict
            insert_db('[dbo].[Python_Serivce_GSTaxGuangDong_Add]',
                      ((batchid, companyname, zh, pwd, json.dumps(info, ensure_ascii=False))))
            browser.quit()
            break


        except Exception as e:
            print('...www')
            print(e)
            ycgb = browser.window_handles
            dq = browser.current_window_handle
            for c_window in ycgb:
                if c_window != dq:
                    browser.switch_to_window(c_window)
                    browser.close()
                    browser.switch_to_window(dq)
            browser.get( 'http://gs.etax-gd.gov.cn/xxmh/html/index.html')
            time.sleep(1.5)
