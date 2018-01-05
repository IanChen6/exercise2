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
customerid=int(mess["customerid"])

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
options.add_argument("--start-maximized")
# D:/BaiduNetdiskDownload/chromedriver.exe
browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
browser.get(url='http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html')
wait = ui.WebDriverWait(browser, 10)
wait.until(lambda browser: browser.find_element_by_css_selector("#shlogin"))
browser.find_element_by_xpath('//li[@id="shlogin"]').click()
browser.find_element_by_xpath("//*[@id='nsrsbh$text']").send_keys(user)  # send_keys：实现往框中输入内容
browser.find_element_by_xpath("//*[@id='nsrpwd$text']").send_keys(pwd)

while True:
    page = browser.page_source
    if '我的定制功能' in page:
        try:
            browser.get('http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html')
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
                        hds = browser.window_handles
                        cr = browser.current_window_handle
                        for c_window in hds:
                            if c_window != cr:
                                browser.switch_to_window(c_window)
                                wait.until(lambda browser: browser.find_element_by_css_selector('#cekcWindow iframe'))
                                frame_element = browser.find_element_by_css_selector('#cekcWindow iframe')
                                browser.switch_to_frame(frame_element)
                                browser.find_element_by_css_selector("#unexist span").click()
                                browser.switch_to.default_content()
                                if fw1 > 0:
                                    wait.until(lambda browser: browser.find_element_by_xpath('//*[@id="B2$text"]'))
                                    browser.find_element_by_xpath('//*[@id="B2$text"]').clear()
                                    fw1 = str(fw1)
                                    browser.find_element_by_xpath('//*[@id="B2$text"]').send_keys(fw1)

                                if fw2 > 0:
                                    browser.find_element_by_xpath('//*[@id="B3$text"]').clear()
                                    fw2 = str(fw2)
                                    browser.find_element_by_xpath('//*[@id="B3$text"]').send_keys(fw2)
                                if hw1 > 0:
                                    browser.find_element_by_xpath('//*[@id="A2$text"]').clear()
                                    hw1 = str(hw1)
                                    browser.find_element_by_xpath('//*[@id="A2$text"]').send_keys(hw1)
                                if hw2 > 0:
                                    browser.find_element_by_xpath('//*[@id="A3$text"]').clear()
                                    hw2 = str(hw2)
                                    browser.find_element_by_xpath('//*[@id="A3$text"]').send_keys(hw2)

                                browser.find_element_by_css_selector('#nextStep').click()
                                wait.until(lambda browser: browser.find_element_by_css_selector('.mini-tools-close'))
                                browser.find_element_by_css_selector('.mini-tools-close').click()
                                if fwms > 0:
                                    try:
                                        browser.find_element_by_xpath('//*[@id="B18$text"]').clear()
                                        try:
                                            browser.find_element_by_xpath('//span[@id="0"]').click()
                                        except:
                                            print("无弹出框")
                                        fwms = str(fwms)
                                        browser.find_element_by_xpath('//*[@id="B18$text"]').send_keys(fwms)
                                    except:
                                        print("无法输入")
                                if fwyj > 0:
                                    try:
                                        browser.find_element_by_xpath('//*[@id="B21$text"]').clear()
                                        try:
                                            browser.find_element_by_xpath('//span[@id="0"]').click()
                                        except:
                                            print("无弹出框")
                                        fwyj = str(fwyj)
                                        browser.find_element_by_xpath('//*[@id="B21$text"]').send_keys(fwyj)
                                    except:
                                        print("无法输入")
                                if hwms > 0:
                                    try:
                                        browser.find_element_by_xpath('//*[@id="A18$text"]').clear()
                                        try:
                                            browser.find_element_by_xpath('//span[@id="0"]').click()
                                        except:
                                            print("无弹出框")
                                        hwms = str(hwms)
                                        browser.find_element_by_xpath('//*[@id="A18$text"]').send_keys(hwms)
                                    except:
                                        print("无法输入")
                                if hwyj > 0:
                                    try:
                                        browser.find_element_by_xpath('//*[@id="A21$text"]').clear()
                                        try:
                                            browser.find_element_by_xpath('//span[@id="0"]').click()
                                        except:
                                            print("无弹出框")
                                        hwyj = str(hwyj)
                                        browser.find_element_by_xpath('//*[@id="A21$text"]').send_keys(hwyj)
                                    except:
                                        print("无法输入")

                                browser.find_element_by_css_selector('#nextStep').click()
                                time.sleep(0.2)
                                browser.find_element_by_css_selector('#nextStep').click()
                                wait.until(lambda browser: browser.find_element_by_css_selector('#pbbd'))
                                browser.find_element_by_css_selector('#pbbd').click()
                                time.sleep(10)
                                ycdb = browser.page_source
                                if "不通过" not in ycdb:
                                    wait.until(lambda browser: browser.find_element_by_css_selector("#mini-213"))
                                    browser.find_element_by_css_selector("#mini-213").click()
                                    time.sleep(5)
                                    browser.find_element_by_css_selector('#nextStep').click()
                                    frame_element = browser.find_element_by_css_selector('#sjyzmWindow iframe')
                                    browser.switch_to_frame(frame_element)
                                    browser.find_element_by_xpath('//*[@onclick="normalSubmit()"]').click()
                                    time.sleep(10)
                                elif "不通过" in ycdb:
                                    dbbtg = etree.HTML(ycdb)
                                    dbbtg1 = dbbtg.xpath('//*[@id="mini-212"]//table/tbody/tr')
                                    fail_dict={}
                                    for r in dbbtg1:
                                        t = r.xpath('.//text()')
                                        fail_dict[t[0]]=t[1]
                                    fail_json=json.dumps(fail_dict,ensure_ascii=False)
                                    gsparams = (customerid, "GS", "小规模增值税", fail_json)
                                    insert_db(host, port, db, "[dbo].[Python_Serivce_ShenZhen_TaxApplyCheckError]",
                                              gsparams)
                                    browser.quit()
                                    sys.exit()

                                browser.close()
                                browser.switch_to_window(cr)
                        gsdict = {}
                        gsdict["开始期间"] = gsks
                        gsdict["结束期间"] = gsjs
                        gsdict["申报金额"] = str(fw1)
                        gsdict["申报状态"] = "已申报"
                        gsjson = json.dumps(gsdict, ensure_ascii=False)
                        gsparams = (customerid, "GS", "小规模增值税", gsjson)
                        insert_db(host, port, db, "[dbo].[Python_Serivce_ShenZhen_TaxApplyUpdate]", gsparams)
                    except Exception as e:
                        print(e)
                        gsdict = {}
                        gsdict["开始期间"] = gsks
                        gsdict["结束期间"] = gsjs
                        gsdict["申报金额"] = str(fw1)
                        gsdict["申报状态"] = "申报失败"
                        gsjson = json.dumps(gsdict, ensure_ascii=False)
                        gsparams = (customerid, "GS", "小规模增值税", gsjson)
                        insert_db(host, port, db, "[dbo].[Python_Serivce_ShenZhen_TaxApplyUpdate]", gsparams)
                a += 1

            ds_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/djsxx.html'
            browser.get(url=ds_url)
            djzs = mess['djzs']
            djms = mess['djms']
            dfzs = mess['dfzs']
            dfms = mess['dfms']
            dczs = mess['dczs']
            dcms = mess['dcms']
            wait.until(lambda browser: browser.find_element_by_css_selector("#mini-29 .mini-button-text"))
            browser.find_element_by_css_selector("#mini-29 .mini-button-text").click()
            browser.find_element_by_css_selector("#mini-27 .mini-button-text").click()
            browser.find_element_by_xpath("//a[@href='javascript:gotoDs()']").click()
            time.sleep(3)
            windows = browser.window_handles
            window1 = browser.current_window_handle
            for c_window in windows:
                if c_window != window1:
                    browser.close()
                    browser.switch_to_window(c_window)
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
                    # browser.switch_to_frame
                    browser.switch_to.default_content()
                    time.sleep(3)
                    cont = browser.page_source
                    browser.switch_to_frame('layui-layer-iframe3')
                    cont = browser.page_source
                    browser.find_element_by_css_selector("#sbxx0_2").clear()
                    browser.find_element_by_css_selector("#sbxx0_2").send_keys(djzs)
                    browser.find_element_by_css_selector("#sbxx0_3").clear()
                    browser.find_element_by_css_selector("#sbxx0_3").send_keys(djms)
                    browser.find_element_by_css_selector("#sbxx1_2").clear()
                    browser.find_element_by_css_selector("#sbxx1_2").send_keys(dfzs)
                    browser.find_element_by_css_selector("#sbxx1_3").clear()
                    browser.find_element_by_css_selector("#sbxx1_3").send_keys(dfms)
                    browser.find_element_by_css_selector("#sbxx2_2").clear()
                    browser.find_element_by_css_selector("#sbxx2_2").send_keys(dczs)
                    browser.find_element_by_css_selector("#sbxx2_3").clear()
                    browser.find_element_by_css_selector("#sbxx2_3").send_keys(dcms)
                    per1 = browser.find_element_by_css_selector("#sbxx0_7").get_attribute("value")
                    per2 = browser.find_element_by_css_selector("#sbxx1_7").get_attribute("value")
                    per3 = browser.find_element_by_css_selector("#sbxx2_7").get_attribute("value")
                    djzs = float(djzs)
                    djms = float(djms)
                    djprice = (djzs + djms) * float(per1)
                    dfzs = float(dfzs)
                    dfms = float(dfms)
                    dfprice = (dfzs + dfms) * float(per2)
                    dczs = float(dczs)
                    dcms = float(dcms)
                    dcprice = (dczs + dcms) * float(per3)
                    sbprice = djprice + dfprice + dcprice
                    browser.switch_to.default_content()
                    cc = browser.page_source
                    browser.find_element_by_link_text("正式申报").click()
                    browser.switch_to_frame('layui-layer-iframe3')
                    pdsb = browser.page_source
                    if "正式申报成功" in pdsb:
                        sb_status = "成功"
                        dsdict = {}
                        dsdict["开始期间"] = ks
                        dsdict["结束期间"] = js
                        dsdict["申报金额"] = str(sbprice)
                        dsdict["申报状态"] = sb_status
                        dsjson = json.dumps(dsdict, ensure_ascii=False)
                        dsparams = (customerid, "DS", "教育费附加、地方教育附加、城市维护建设税", dsjson)
                        insert_db(host, port, db, "[dbo].[Python_Serivce_ShenZhen_TaxApplyUpdate]", dsparams)
                    else:
                        sb_status = "失败"
                        dsdict = {}
                        dsdict["开始期间"] = ks
                        dsdict["结束期间"] = js
                        dsdict["申报金额"] = str(sbprice)
                        dsdict["申报状态"] = sb_status
                        dsjson = json.dumps(dsdict, ensure_ascii=False)
                        dsparams = (customerid, "DS", "教育费附加、地方教育附加、城市维护建设税", dsjson)
                        insert_db(host, port, db, "[dbo].[Python_Serivce_ShenZhen_TaxApplyUpdate]", dsparams)

                    break
                b += 1

            browser.quit()
            sys.exit()
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
            browser.get('http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html')
            fw1 = float(fw1)
            fw2 = float(fw2)
            hw1 = float(hw1)
            hw2 = float(hw2)
            fwms = float(fwms)
            fwyj = float(fwyj)
            hwms = float(hwms)
            hwyj = float(hwyj)
