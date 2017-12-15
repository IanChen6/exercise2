# -*- coding:utf-8 -*-
__author__ = 'IanChen'

import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import pymysql
import random
from get_proxy import get_all_proxie

MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "zhihu"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1029384756"
MYSQL_Port = "3306"
conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DBNAME, port=3306,
                       charset="utf8")
cursor = conn.cursor()
create_tb = """
 CREATE TABLE IF NOT EXISTS wangyi2(
    id INT UNSIGNED AUTO_INCREMENT,
    title VARCHAR(200),
    url VARCHAR(200),
    PRIMARY KEY(id)
)
    """
cursor.execute(create_tb)

url = 'http://www.163.com/'
session=requests.session()

#使用代理IP
proxy_list=get_all_proxie()
proxy=proxy_list[random.randint(0,len(proxy_list)-1)]
session.proxies=proxy

resp = session.get(url)
# soup= BeautifulSoup(resp.content,'html.parser')
# print(soup)
# data=soup.findAll('div',{'class':'bd'})
# match=re.findall(r'<a .*?>(.*?)</a>',str(data[0]))
# print(match)

# data=soup.findAll('div',{'class':"tab_panel current"})
# match=re.findall(r'<a href=(.*?)>(.*?)</a>',str(data[1]))
# print(match)

resp.encoding = 'utf-8'
root = etree.HTML(resp.content)  # 将request.content 转化为 Element
select = root.xpath('//div[@class="cm_area ns_area_top"]//div[@class="bd"]//li/a')
a = 1
for i in select:
    title = i.xpath('./text()')[0]
    url = i.xpath('./@href')[0].replace('1', 'a')
    # 当有多个属性时，用/./span[contains(@class,'vote')],意为span的class属性包含有值为vote
    # selec=selec.xpath('./@href')[0]

    params = (url, title)
    insert_sql = """
                INSERT INTO wangyi2(url,title)
                VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE url=VALUES(url),title=VALUES(title)
            """
    cursor.execute(insert_sql, params)

    conn.commit()

    print(title)
    print(url)

pass
