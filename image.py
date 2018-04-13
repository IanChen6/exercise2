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
import requests
import base64
import json
import re
from suds.client import Client
import suds
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



def login():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('disable-infobars')
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
    # # browser = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)
    # browser.set_window_size(2200, 2200)
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = (
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
    # dcap["phantomjs.page.settings.loadImages"] = True
    # service_args = []
    # service_args.append('--webdriver=szgs')
    # browser = webdriver.PhantomJS(
    #     executable_path='D:/BaiduNetdiskDownload/phantomjs-2.1.1-windows/bin/phantomjs.exe',
    #     desired_capabilities=dcap, service_args=service_args)
    # # browser = webdriver.PhantomJS(
    # #     executable_path='/home/tool/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',
    # #     desired_capabilities=dcap)
    # browser.implicitly_wait(10)
    browser.viewportSize = {'width': 2200, 'height': 2200}
    browser.set_window_size(2200, 2200)
    browser.get(
        url='http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html?redirectURL=http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html')
    wait = ui.WebDriverWait(browser, 8)
    wait.until(lambda browser1: browser1.find_element_by_css_selector("#shlogin"))
    browser.find_element_by_xpath("//*[@id='shlogin']").click()
    browser.find_element_by_xpath("//*[@id='nsrsbh$text']").send_keys("440300771615767")  # send_keys：实现往框中输入内容
    browser.find_element_by_xpath("//*[@id='nsrpwd$text']").send_keys('83093013')
    time.sleep(0.3)
    cont = browser.page_source
    frame_capt = browser.find_element_by_css_selector("#TCaptcha2 iframe")
    browser.switch_to_frame(frame_capt)
    time.sleep(1)
    browser.find_element_by_xpath("//*[@id='tcaptcha_trigger_text_init']").click()
    browser.switch_to_default_content()
    time.sleep(1)
    browser.save_screenshot("点击验证码.png")
    frame_capt2 = browser.find_element_by_css_selector('#tcaptcha_container iframe')
    browser.switch_to_frame(frame_capt2)
    browser.save_screenshot("验证码图片.png")
    time.sleep(1)
    imageurl = browser.find_element_by_xpath("//*[@id='slideBkg']").get_attribute('src')
    resp = requests.get(imageurl)
    con = str(base64.b64encode(resp.content))[2:-1]
    client = suds.client.Client(url="http://39.108.112.203:8023/yzmmove.asmx?wsdl")
    # client = suds.client.Client(url="http://192.168.18.101:1421/SZYZService.asmx?wsdl")
    auto = client.service.GetYZCodeForDll(con)
    auto = int(auto)
    dragger = browser.find_element_by_css_selector('#tcaptcha_drag_thumb')
    action = ActionChains(browser)
    action.click_and_hold(dragger)
    offset = auto - 262
    s1 = offset - 170
    action.move_by_offset(25, 1)
    action.move_by_offset(30, 4)
    action.move_by_offset(15, 2)
    action.move_by_offset(22, 4)
    action.move_by_offset(18, 0)
    action.move_by_offset(12, 0)
    action.move_by_offset(16, 0)
    action.move_by_offset(22, 0)
    action.move_by_offset(20, 0)
    action.move_by_offset(s1, 0)
    action.release().perform()
    browser.save_screenshot("滑动后结果.png")
    time.sleep(1.5)
    browser.switch_to_default_content()
    time.sleep(0.5)
    browser.switch_to_frame(frame_capt)
    time.sleep(0.5)
    yzzt = browser.page_source
    if "验证成功" not in yzzt:
        browser.switch_to_default_content()
        time.sleep(0.5)
        browser.switch_to_frame(frame_capt2)
        time.sleep(1)
        action = ActionChains(browser)
        action.click_and_hold(dragger)
        offset = auto - 282
        s1 = offset - 150
        action.move_by_offset(25, 0)
        action.move_by_offset(13, 0)
        action.move_by_offset(17, 0)
        action.move_by_offset(15, 0)
        action.move_by_offset(22, 0)
        action.move_by_offset(18, 0)
        action.move_by_offset(12, 0)
        action.move_by_offset(16, 0)
        action.move_by_offset(22, 0)
        action.move_by_offset(s1, 0)
        action.release().perform()
        time.sleep(1.5)
        browser.switch_to_default_content()
        time.sleep(0.5)
        browser.switch_to_frame(frame_capt)
        time.sleep(0.5)
        yzzt = browser.page_source
        if "验证成功" not in yzzt:
            browser.quit()
            return False
    elif "验证成功" in yzzt:
        browser.switch_to_default_content()
        browser.find_element_by_xpath('//*[@id="login-form"]/div[5]/a').click()
        print("登录成功")
        return True
for i in range(10):
    st=login()
    if st:
        print("pass")
        break


