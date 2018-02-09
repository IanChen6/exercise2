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
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support import ui
import time
options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
options.add_argument("--start-maximized")
zh=['yyp15','yyp16','yyp17','yyp18','yyp19','yyp20']
for i in zh:
    try:
        browser = webdriver.Chrome(executable_path='chromedriver.exe', chrome_options=options)
        browser.get('http://www.51cswy.com/e/member/login/index.php')
        browser.find_element_by_css_selector('#nickname').send_keys(i)
        browser.find_element_by_css_selector('#password').send_keys('123456')
        browser.find_element_by_css_selector('#get_acc').click()
        time.sleep(1)
        # browser.get('http://www.51cswy.com/e/member/cp/')
        browser.get('http://www.51cswy.com/e/DoInfo/ListInfo.php?mid=9')
        browser.find_element_by_link_text('修改').click()
        time.sleep(0.5)
        pianqu = browser.find_element_by_css_selector('#Block').get_attribute('value')
        jiedao = browser.find_element_by_css_selector('#street').get_attribute('value')
        # browser.get('http://www.51cswy.com/e/DoInfo/ChangeClass.php?mid=10')
        browser.get('http://www.51cswy.com/e/DoInfo/ChangeClass.php?mid=10')
        time.sleep(0.5)
        id = [25, 26, 27, 28, 140, 29, 30, 31, 135, 136, 137, 138, 139, 115, 116, 117, 118, 119, 120, 121, 122, 123,
              124, 125, 126, 127, 128, 129, 130, 134, 131, 132, 133, 40, 41, 109, 110, 111, 112, 113, 114, 104, 105,
              106, 107]
        for j in id:
            add_url = 'http://www.51cswy.com/e/DoInfo/AddInfo.php?mid=10&enews=MAddInfo&classid={}&Submit=%E6%B7%BB%E5%8A%A0%E4%BF%A1%E6%81%AF'.format(
                j)
            browser.get(add_url)
            mc = browser.find_element_by_xpath(
                '//*[@id="jmod_main_container"]/div/div/form/table[1]/tbody/tr[3]/td[2]/a[2]').text
            # mc=mc[0]
            browser.find_element_by_xpath('//input[@name="title"]').send_keys(mc)
            browser.find_element_by_css_selector('#Block').send_keys(pianqu)
            browser.find_element_by_css_selector('#street').send_keys(jiedao)
            browser.find_element_by_xpath('//input[@name="addnews"]').click()
            time.sleep(1)
        print(i)
        browser.quit()
    except Exception as e:
        print(i)
        print(e)








