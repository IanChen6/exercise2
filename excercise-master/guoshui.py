# -*- coding:utf-8 -*-
import re

__author__ = 'IanChen'
# selinium需要专用的driver来调用浏览器
import os
from pyquery import PyQuery
from selenium import webdriver
from scrapy.selector import Selector  # 对页面提取用selector会比browser自带的元素查找更方便
import time
import requests
from PIL import Image, ImageEnhance
import json
from pyocr import pyocr
import xlwt
import base64
from lxml import etree

try:
    import urlparse as parse
except:
    from urllib import parse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# browser = webdriver.Chrome(executable_path='D:/BaiduNetdiskDownload/chromedriver.exe')#添加driver的路径

def save_png(browser, path):
    browser.get_screenshot_as_file(path)


def captcha():
    with open('captcha.jpg', 'rb') as f:
        base64_data = str(base64.b64encode(f.read()))
        base64_data = base64_data[2:-1]

        post_data = {"a": 1, "b": base64_data}
        post_data = json.dumps({"a": 1, "b": base64_data})
        res = requests.post(url="http://192.168.18.113:8002/mycode.ashx", data=post_data)
        return res.text


def login():
    try_times = 0
    while try_times <= 3:
        try_times += 1
        login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
        timestamp = str(int(time.time() * 1000))
        captcha_url = 'http://dzswj.szgs.gov.cn/JPEGServlet?d={}'.format(timestamp)
        session = requests.session()
        headers = {'Host': 'dzswj.szgs.gov.cn',
                   'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Content-Type': 'application/json; charset=UTF-8',
                   'Referer': 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                   'x-form-id': 'mobile-signin-form',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Origin': 'http://dzswj.szgs.gov.cn'
                   }
        with open("captcha.jpg", "wb") as f:
            f.write(session.get(url=captcha_url, headers=headers).content)
            f.close()

        tagger = captcha()
        # im=Image.open("captcha.jpg")
        # im.show()
        # im.close()
        # captcha=input('input captcha')
        time_l = time.localtime(int(time.time()))
        time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
        # login_data = {"nsrsbh": "440300771615767", "nsrpwd": "06fc3bcbd18ac83d45a8c369b7800d2e724f80c7",
        #               "tagger": tagger, "redirectURL": "", "time": time_l}
        login_data = {"nsrsbh": "440300754285743", "nsrpwd": "b68a74d266ec48553be35a8af4318e57e176b85b",
                      "tagger": tagger, "redirectURL": "", "time": time_l}
        resp = session.post(url=login_url, headers=headers, data=json.dumps(login_data))
        if resp.json()['success'] == True:
            print('登录成功')
            cookies = {}
            for (k, v) in zip(session.cookies.keys(), session.cookies.values()):
                cookies[k] = v
            return cookies, session
        else:
            time.sleep(3)


def parse_biaoge(browser):
    # 表格信息爬取
    content = browser.page_source
    root = etree.HTML(content)
    pages=root.xpath('//div[@class="mini-pager-right"]/text()')
    numbers=re.search(r'每页 10 条, 共 (\d+) 条',pages[0]).group(1)
    numbers=int(numbers)-1
    next_page=numbers//10
    a = -1
    for page in range(next_page+1):
        content = browser.page_source
        root = etree.HTML(content)
        select = root.xpath('//table[@id="mini-grid-table-bodysbqkGrid"]/tbody/tr')

        for i in select[1:]:
            shuizhong = i.xpath('.//text()')
            a += 1
            if "查询申报表" in shuizhong:
                print("需要点击查询")
                parse_shenbaobiao(browser, a)
            print(shuizhong)
        browser.find_element_by_xpath('//*[@id="mini-33"]/span').click()


# 申报表截图
def parse_shenbaobiao(browser, a):
    browser.find_element_by_xpath('//*[@id="mini-25${}"]//a[1]'.format(a)).click()
    time.sleep(3)
    g_content = browser.page_source
    if "查询失败" in g_content:
        browser.find_element_by_xpath('//div[@class="mini-messagebox-buttons"]//span').click()
    elif "查询失败" not in g_content:
        browser.find_element_by_class_name('mini-tools-max').click()
        frame_element = browser.find_element_by_css_selector('.mini-window iframe')
        browser.switch_to_frame(frame_element)
        time.sleep(1)
        content_p = browser.page_source
        root2 = etree.HTML(content_p)
        select2 = root2.xpath('//table[@class="mini-tabs-header"]//span')
        b = 0
        for i in select2:
            b += 1
            browser.find_element_by_id('mini-1${}'.format(b)).click()
            time.sleep(2)
        # browser.save_screenshot('国税申报表截图{}{}.png'.format(a, b))
            save_png(browser, '国税申报表截图{}{}.png'.format(a, b))
        browser.switch_to.default_content()
        browser.find_element_by_class_name('mini-tools-close').click()
        time.sleep(3)


# 国税缴款
def parse_jiaokuan(browser):
    browser.find_element_by_css_selector("#sssqq .mini-buttonedit-input").clear()
    browser.find_element_by_css_selector("#sssqq .mini-buttonedit-input").send_keys('20170101')
    browser.find_element_by_css_selector("#sssqz .mini-buttonedit-input").clear()
    browser.find_element_by_css_selector("#sssqz .mini-buttonedit-input").send_keys('20171207')
    browser.find_element_by_css_selector("#mini-37 .mini-button-text").click()
    time.sleep(1)
    browser.find_element_by_css_selector("#stepnext .mini-button-text").click()
    browser.save_screenshot('缴税信息.png')
    # 表格信息爬取
    content = browser.page_source
    root = etree.HTML(content)
    select = root.xpath('//table[@id="mini-grid-table-bodyyjscx"]/tbody/tr')
    for i in select[1:]:
        jsxx = i.xpath('.//text()')
        print(jsxx)


# d地税
def dishui(browser):
    time.sleep(2)
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
    browser.find_element_by_css_selector('#menu_110000_110109').click()
    time.sleep(2)
    browser.switch_to_frame('qyIndex')
    # page_source = browser.page_source
    time.sleep(1)
    browser.find_element_by_css_selector('#menu2_13_110200').click()
    time.sleep(1)
    browser.find_element_by_css_selector('#menu3_15_110202').click()
    browser.switch_to_frame('qymain')
    time.sleep(2)
    browser.find_element_by_css_selector('#zsxmDm').find_element_by_xpath('//option[@value="10109"]').click()  # 选择城市建设税
    browser.find_element_by_css_selector('#sbqq').clear()
    browser.find_element_by_css_selector('#sbqq').send_keys('2017-01-01')
    time.sleep(1)
    browser.find_element_by_css_selector('#query').click()
    time.sleep(2)
    browser.save_screenshot('地税已申报查询.png')
    # 表格信息爬取
    content = browser.page_source
    root = etree.HTML(content)
    select = root.xpath('//table[@id="ysbjl_table"]/tbody/tr')
    index = 0
    time.sleep(2)
    for i in select:
        c=browser.page_source
        browser.find_element_by_xpath(
            '//table[@id="ysbjl_table"]/tbody/tr[@data-index="{}"]//input[@name="btSelectItem"]'.format(index)).click()
        browser.find_element_by_css_selector('#print').click()
        # url=browser.find_element_by_name('sbbFormCj').get_attribute('action')
        jsxx = i.xpath('.//text()')
        pzxh = jsxx[0]
        print(jsxx)
        # Chrome对pdf页面截图（phantom截图失败？？？）
        # windows = browser.window_handles
        # window1 = browser.current_window_handle
        # for c_window in windows:
        #     if c_window != window1:
        #         browser.switch_to_window(c_window)
        #         # html=browser.page_source
        #         # time.sleep(3)
        #         # pdfkit.from_string(html,"申报表详情{}.png".format(pzxh))
        #         browser.save_screenshot("申报表详情{}.png".format(pzxh))
        #         browser.close()
        #         browser.switch_to_window(window1)
        #         time.sleep(1)
        #         browser.switch_to_frame('qyIndex')
        #         time.sleep(1)
        #         browser.switch_to_frame('qymain')
        #         time.sleep(1)

        b_ck = browser.get_cookies()
        ck = {}
        for x in b_ck:
            ck[x['name']] = x['value']
        post_url = parse.urljoin("https://dzswj.szds.gov.cn",
                                 browser.find_element_by_name('sbbFormCj').get_attribute('action'))
        post_data = {'SubmitTokenTokenId': '', 'yzpzxhArray': pzxh, 'btSelectItem': 'on'}
        headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
                   }
        with open("申报表详情{}.pdf".format(pzxh), 'wb') as w:
            w.write(requests.post(url=post_url, headers=headers, data=post_data, cookies=ck).content)

        index += 1

    # 已缴款查询
    page = browser.page_source
    # browser.switch_to_window(window1)
    browser.switch_to_default_content()
    browser.switch_to_frame('qyIndex')
    browser.find_element_by_css_selector('#menu3_17_110204').click()
    browser.switch_to_frame('qymain')
    time.sleep(1)
    browser.find_element_by_css_selector('#jkqq').clear()
    browser.find_element_by_css_selector('#jkqq').send_keys('2017-07-01')
    browser.find_element_by_css_selector('#jkqz').clear()
    browser.find_element_by_css_selector('#jkqz').send_keys('2017-09-30')
    time.sleep(1)
    browser.find_element_by_css_selector('#query').click()
    time.sleep(2)
    browser.save_screenshot('地税已缴款查询.png')
    # 缴款表格信息爬取
    content = browser.page_source
    root = etree.HTML(content)
    select = root.xpath('//table[@id="yjkxx_table"]/tbody/tr')
    index2 = 0
    pz_l = []
    for i in select:
        jkxx = i.xpath('.//text()')
        pz = jkxx[0]
        print(jkxx)
        index2 += 1
        pz_l.append(pz)
    for i in range(1, int(index2 / 3) + 1):
        browser.find_element_by_xpath(
            '//table[@id="yjkxx_table"]/tbody/tr[@data-index="{}"]//input[@name="btSelectItem"]'.format(
                i * 3 - 1)).click()
        time.sleep(1)
        browser.find_element_by_css_selector('#cxjkmx').click()
        windows = browser.window_handles
        window2 = browser.current_window_handle
        for c_window in windows:
            if c_window != window2:
                browser.switch_to_window(c_window)
                png_name = "缴款凭证号{}.png".format(pz_l[i * 3 - 1])
                browser.save_screenshot(png_name)
                browser.close()
                browser.switch_to_window(window2)
                time.sleep(1)
                browser.switch_to_frame('qyIndex')
                browser.switch_to_frame('qymain')


if __name__ == '__main__':
    start_time=time.time()
    cookies, session = login()
    jsoncookies = json.dumps(cookies)
    with open('cookies.json', 'w') as f:  # 将login后的cookies提取出来
        f.write(jsoncookies)
        f.close()
    # chrome_options = Options()
    # chrome_options.add_argument("--window-size=1280,2000")
    #设置无头chrome
    # options=webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("window-size=1200x1600")
    #
    # browser = webdriver.Chrome(executable_path='D:/BaiduNetdiskDownload/chromedriver.exe',chrome_options=options)  # 添加driver的路径
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
    dcap["phantomjs.page.settings.loadImages"] = True
    browser = webdriver.PhantomJS(executable_path='D:/BaiduNetdiskDownload/phantomjs-2.1.1-windows/bin/phantomjs.exe',
                                  desired_capabilities=dcap)  # 添加driver的路径
    browser.maximize_window()
    browser.viewportSize = {'width': 2200, 'height': 2200}
    browser.set_window_size(1020, 1600)  # Chrome无法使用这功能
    index_url = "http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html"
    browser.get(url=index_url)
    browser.delete_all_cookies()
    with open('cookies.json', 'r', encoding='utf8') as f:
        cookielist = json.loads(f.read())
    for (k, v) in cookielist.items():
        browser.add_cookie({
            'domain': '.szgs.gov.cn',  # 此处xxx.com前，需要带点
            'name': k,
            'value': v,
            'path': '/',
            'expires': None})
    shenbao_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/cxdy/sbcx.html'
    browser.get(url="http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html")
    browser.get(url=shenbao_url)

    time.sleep(3)
    browser.find_element_by_css_selector("#sbrqq .mini-buttonedit-input").clear()
    browser.find_element_by_css_selector("#sbrqq .mini-buttonedit-input").send_keys('20170101')
    browser.find_element_by_css_selector("#stepnext .mini-button-text").click()
    time.sleep(3)
    # browser.save_screenshot('国税申报结果截图.png')
    save_png(browser, '国税申报结果截图.png')
    parse_biaoge(browser)

    # 国税缴款查询
    jk_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/jk_jsxxcx.html'
    browser.get(url=jk_url)
    # parse_jiaokuan(browser)

    # 地税查询
    ds_url = 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/sb/djsxx/djsxx.html'
    browser.get(url=ds_url)
    # dishui(browser)

    end_time=time.time()
    expended_time=end_time-start_time
    print(expended_time)

    # 表格信息爬取
    # content = browser.page_source
    #
    # doc = PyQuery(content, parser='html')
    # sssb = doc.find('table#mini-grid-table-bodysbqkGrid').find('tr').items()
    # for i in sssb:
    #     data=i.text()
    #     parse_shenbaobiao(browser,i)
    #     print(data)
    # 列表信息爬取
    # shuizhong_list = []
    # # sum_list=[]
    # # while
    # # for i in range(1,8):
    # # shuizhong=browser.find_element_by_xpath('//tr[@id="mini-25$0"]/td[@id="mini-25$0${}"]'.format(i)).text
    # list=browser.find_element_by_xpath('//table[@id="mini-grid-table-bodysbqkGrid"]/tbody').find_element_by_tag_name('tr').text
    #
    # # shuizhong_list.append(shuizhong)
    # # sum_list.append(shuizhong_list)
    # print(list)
    # 创建工作簿
    # wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # # 创建工作表
    # sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
    # # 表头（table_top_list包含表头每一列的值）
    # table_top_list = browser.find_element_by_xpath('//table[@id="mini-grid-table-bodysbqkGrid"]/tbody/tr').find_elements_by_tag_name('td')
    # # 写入表头到sheet 1中，第0行第c列
    # for c, top in enumerate(table_top_list):
    #     sheet.write(0, c, top.text)
    #
    #     # 表的内容
    # # 将表的每一行存在table_tr_list中
    # table_tr_list = browser.find_element_by_xpath( '//table[@id="mini-grid-table-bodysbqkGrid"]/tbody').find_elements_by_tag_name('tr')
    # for r, tr in enumerate(table_tr_list, 1):
    #     # 将表的每一行的每一列内容存在table_td_list中
    #     table_td_list = tr.find_elements_by_tag_name('td')
    #     # 写入表的内容到sheet 1中，第r行第c列
    #     for c, td in enumerate(table_td_list):
    #         sheet.write(r, c, td.text)
    #         # 保存表格到已有的 excel
    # wbk.save(r'test.xls')

    # workbook = xlwt.Workbook(encoding='utf8')
    # worksheet = workbook.add_sheet('My Worksheet')  # 创表
    # worksheet.write(0, 0, label='Row 0, Column 0 Value')
    # workbook.save('Excel_Workbook.xls')
