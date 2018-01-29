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
import random
from urllib.parse import quote
import requests

ip = ['121.31.159.197', '175.30.238.78', '124.202.247.110', '124.202.247.154', '166.202.247.110']
useragenr = ['Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
             'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3485.400 QQBrowser/9.6.12190.400',
             'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; LCTE; rv:11.0) like Gecko']
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://app02.szmqs.gov.cn',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'x-form-id': 'mobile-signin-form',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://app02.szmqs.gov.cn/outer/entSelect/gs.html',
    # 'X-Forwarded-For': ip[random.randint(0, 4)]
    # 'Cookie': 'Hm_lvt_5a517db11da5b1952c8edc36c230a5d6=1516416114; Hm_lpvt_5a517db11da5b1952c8edc36c230a5d6=1516416114; JSESSIONID=0000H--QDbjRJc2YKjpIYc_K3bw:-1'
}
session = requests.session()
proxy = {'https': 'http://bjhz:bjhz@114.215.112.138:7777', 'http': 'http://bjhz:bjhz@114.215.112.138:7777'}
session.proxies = proxy
# name='unifsocicrediden=&entname={}&flag=1'
# postdata='unifsocicrediden=&entname={}&flag=1'.format()
# s = 'aaaa'
# # s='aaa'
# if s.strip():
#     print('not null')
#     print(s)
name = '深圳市恒胜兴磁业有限公司'
urlname = quote(name)

# postdata='unifsocicrediden=91440300788330637R&entname=&flag=1'
postdata = 'unifsocicrediden=&entname={}&flag=1'.format(urlname)
resp = session.post('https://app02.szmqs.gov.cn/outer/entEnt/detail.do', headers=headers, data=postdata)
gswsj = resp.json()
gswsj = gswsj['data']
gswsj = gswsj[0]
gswsj = gswsj['data']
jbxx=gswsj[0]
if jbxx['opto']=="5000-01-01" or jbxx['opto']=="1900-01-01" or jbxx['opto'].strip():
    jbxx['营业期限']="永续经营"
else:
    jbxx['营业期限']="自"+jbxx['opfrom'] + "起至" + jbxx['opto']+ "止"

# gswsj = json.dumps(gswsj, ensure_ascii=False)
index_dict = gswsj[0]
id = index_dict['id']
regno = index_dict['regno']
opetype = index_dict['opetype']
unifsocicrediden = index_dict['unifsocicrediden']
pripid=index_dict['entflag']
header2 = {
    'Origin': 'https://app02.szmqs.gov.cn',
    # 'Cookie': 'Hm_lvt_5a517db11da5b1952c8edc36c230a5d6=1516416114,1516590080; Hm_lpvt_5a517db11da5b1952c8edc36c230a5d6=1516590080; JSESSIONID=0000CgpyMFWxBHU8MWpcnjFhHx6:-1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://app02.szmqs.gov.cn/outer/entSelect/gs.html',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
}
xqlist = ['许可经营信息',
          '股东信息',
          '成员信息',
          '变更信息',
          '股权质押信息',
          '动产抵押信息',
          '法院冻结信息',
          '经营异常信息',
          '严重违法失信信息']
tagid=1
djxx={}
postdata='pripid={}&opetype={}'.format(pripid,opetype)
nbresp = requests.post('https://app02.szmqs.gov.cn/outer/entEnt/nb.do', headers=header2, data=postdata)
if nbresp.status_code == 200:
    nb=nbresp.json()
    nb=nb['data']
    nb=nb[0]
    nb=nb['data']
    if len(nb) !=0:
        yearnb=''
        for n in nb:
            yearnb+=""+n['ancheyear']+"年报已公示、"
    else:
        yearnb="无年报信息"
jbxx["年报情况"]=yearnb
djxx["基本信息"]=jbxx
for i in xqlist:
    postdata = 'flag=1&tagId={}&id={}&regno={}&unifsocicrediden={}&opetype={}'.format(tagid, id, regno, unifsocicrediden,
                                                                                      opetype)
    dtresp = requests.post('https://app02.szmqs.gov.cn/outer/entEnt/tag.do', headers=header2, data=postdata)
    if dtresp.status_code==200:
        dt=dtresp.json()
        dt=dt['data']
        dt=dt[0]
        dt=dt['data']
        djxx[i]=dt
    tagid+=1
print(djxx)
print(gswsj)
