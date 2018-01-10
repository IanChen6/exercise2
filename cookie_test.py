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
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

dlck = [{'expiry': 1515487456.516183, 'secure': False, 'httpOnly': False, 'path': '/', 'domain': 'dzswj.szgs.gov.cn',
         'value': '4fee556f5c4f7b5ed58f4a250441dd19', 'name': 'tgw_l7_route'},
        {'secure': False, 'httpOnly': True, 'path': '/', 'domain': 'dzswj.szgs.gov.cn',
         'value': '4E418AF34446B56000C0FFCBAB31E368', 'name': 'JSESSIONID'},
        {'secure': False, 'httpOnly': False, 'path': '/', 'domain': 'dzswj.szgs.gov.cn',
         'value': '1a85544c9a914161bfa35821739e30f6', 'name': 'DZSWJ_TGC'},
        {'expiry': 1515487158.785185, 'secure': False, 'httpOnly': False, 'path': '/', 'domain': 'dzswj.szgs.gov.cn',
         'value': '"NTI1MDRBNDFCOEI3RjAxQjY3M0ZDNDg5QjQ2QzYyNTkzOUQwQjhGMTFCOEY5RUM1QzJCRDVCMTdCNjZEMzc1QTI4QkE1MkI4QjVGNzRFNkZFNjQ1QjI4OUI0OTk2RjUyNEQwMjU1QzFBRERGMzlENjMxNTg5MDdDNTAxMjI0NEI="',
         'name': 'CNZXDATA'}]
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
dcap["phantomjs.page.settings.loadImages"] = True
browser = webdriver.PhantomJS(executable_path='D:/BaiduNetdiskDownload/phantomjs-2.1.1-windows/bin/phantomjs.exe',
                              desired_capabilities=dcap)
browser.implicitly_wait(10)
browser.get(url='http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html')
browser.delete_all_cookies()
# for d in dlck:
#     for (k, v) in d.items():
#         browser.add_cookie({
#             'domain': '.szgs.gov.cn',  # 此处xxx.com前，需要带点
#             'name': k,
#             'value': v,
#             'path': '/',
#             'expires': None})
browser.add_cookie(
    {'domain': '.szgs.gov.cn', 'name': 'tgw_l7_route', 'value': dlck[0]['value'], 'path': '/', 'expires': None})
browser.add_cookie(
    {'domain': '.szgs.gov.cn', 'name': 'JSESSIONID', 'value': dlck[1]['value'], 'path': '/', 'expires': None})
browser.add_cookie(
    {'domain': '.szgs.gov.cn', 'name': 'DZSWJ_TGC', 'value': dlck[2]['value'], 'path': '/', 'expires': None})

browser.get('http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html')
page = browser.page_source
browser.find_element_by_css_selector("#wqwsbspan").click()
pa=browser.page_source
if '我的定制功能' in page:
    print("登录成功")
