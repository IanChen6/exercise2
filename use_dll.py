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
import time
from urllib.parse import urlparse
from urllib.parse import parse_qs
import execjs
from suds.client import Client
import suds
import json
import requests
import re

def get_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("cdata.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr
def jiami_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("encrypt.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr
session = requests.session()
add = session.get("http://dzswj.szgs.gov.cn/api/auth/queryTxUrl?json&_=1522658530831")
query = urlparse(add.json()['data']).query
d = dict([(k, v[0]) for k, v in parse_qs(query).items()])
sess_url = "https://captcha.guard.qcloud.com/cap_union_prehandle?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw==&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=835414&forcestyle=undefined&collect=xV6XnEXCTYbfMkq3nBXtS0c%2FV5AAZtsYtOqYjNBVDwvu0DT8YIl0%2BdlKp2UjKu0nw9G%2FTRvlmFAxGhorC%2BMq4MBMdkhfEnITqxh7Bad0q7e0ffClmuKkyX15QuZqT42Ej1RCgowaxr6ltGKYPgkVX6Fx%2B9pf6brr%2FIXbyp5trWz5UYDqJQ%2B%2B%2But2YkbKEwsE7%2BazqQ7y1qM9HHGC28%2Bz0iWZ6bjExtUYlbSH1g7zqEuq1FbFd1O%2B6xFztsvzI8lPuYhqwh0zUf4%2Fitr4PxPMGPo7MwUy%2BiJzaG%2F7bPCPvGB%2F9hGrC5V6V9e0uad0iK0FDDhPn0Ge%2F8mMlN7BoJzFAXkNrG1Iax2r0YqqLCffVwuDr1pHyhpq8wySNEYl70BeaVWdeDhT5QQd9Sujkg4EeDp5AEKDKrcvEhfcXrmKVFsH35s0XsFRr67VOyfKi%2BGDuJz4xCXH66ySt2BTycTC55FdfQ0Ef5uTuNFLkPgki2x09ePD7cHJXV7T86%2FkP%2Fi9GSEXBOy31%2B%2BZuLYInfEeiZRbuNEBMwyPa1MNrIMnUun4Dk5m7qP3aaga3UV24bZEhNWE0rYX3XrKLCgcw1JyD%2BF%2B%2F%2BUwcrewMBKzWcceZULq033o9HCRVaDzWxeyUNc%2FYLoGmJBCAhKRuKI35yAcYPZvtfEb6s29jqgMRTNkxSvJfIEHvAdBFYs44%2Fkf0P%2FdwiIHol1TITJVsbmlNehuFt39dXR15aOxbd4L8rv6YxW2j3rxBkWhaZwhgFUR066icYpz6%2FYgcsYbCoSt1Vxaz%2Fu8Wm06dmvyElvOFW2gdQbQYez1ju5x%2FfPFRZR%2B%2FCgOGa7nu8iMQHabdKlwoCRFN5ZHmqRcs01mA4iFQg6MB10aI%2FeuwB4JmHufAT1l5gCWfs1HqJBMRt5flx9KOY0uRi7usyloLQXzXnnCkK%2BRx78gP5n7Ex0ciAVivXjqaxpQKpmgv94IplHxliSNfglULAYvzpr9kSS5saFYSNjP7w0HCyrbRbl6%2B2STCU1MKzRS8UxJ2anCrkyC4vfUeXZY6CIoGVsW9BloXO%2BD7ZSLBgZkPscWv%2FOt8TFywebfHm7YtMfjvCaWCnkT5MtkVrbTUp3vaycuMKB7z%2Fen7yfTP2vkEfmPWxQQtNDKjIKEGtno0EA0SSihw6pfk1hZHD%2BeOji0oQ4IHr2EjvXtibIvKLIOCLRMrMAlSxl%2Fy48utVt4LJa6%2BBLZhNzkuvbgoJL9ss1NZdIt7GIEOhY3HV%2FVnRbMv8zs7pKKqx5Mx%2BjQ61yCjmFHO6ldQrNuKb%2BMYKAennyD9XXd4hFguk13iFcb8luOyJvwg4%2BobY3X5lY975qsxK%2BYZfEwqNE7EatDGCqHCJnM23GdfMKq4ibSTMQe%2FOLziUHKZtI3x%2FvroZ4Fue0ygY5Lmt0cZCK7ik2Xu5U6jcxh1aegAFFzZh18aQPVyGL1Z%2B4Ugg4A0WDgkk0T%2Fzy6FRo8TWf0b%2BbN8Y6HEzty2HaRtU6y2SfifxTmo81uwqAV4GXhzwwNr2zJWoAFnL8pV1119CSXEcXeDxmTDnD4qMmgcBezHWthydUcK66XhZXIlwNQ6yoCTBS75ifUCD%2FImJfYPdClKurBU6MTIvHTIvhb5daodgCEJM%2BwQWPAGOs%2FjRrs7o2%2BopVMQLLDBqcyrDdJrI%2B1XM69Z5qXVxdhTVNayG22R545iv2tvafQr7Z4SAqJr6P7EYupMfgVTCuHyOMJEG0SJd4f3d4arqF%2Bg0gY5drdpJMp94P06X5YovTwldW3t8fIB2QhAqjSRCCr&firstvrytype=1&random=0.017271072963999323&_=1522664696316".format(
    d['asig'])
sess = session.get(sess_url)
vsig_url = "https://captcha.guard.qcloud.com/cap_union_new_show?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw==&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=835414&forcestyle=undefined&rand=0.4457241752210961&sess={}&firstvrytype=1&showtype=point".format(
    d['asig'], sess.json()["sess"])
vsig_r = session.get(vsig_url)
ad = re.search("Q=\"(.*?)\"", vsig_r.text)
websig=re.search("websig\:\"(.*?)\"", vsig_r.text)
websig=websig.group(1)
et=re.search("et=\"(.*?)\"", vsig_r.text)
et=et.group(1)
vsig = ad.group(1)
jsstr = get_js()
ctx = execjs.compile(jsstr)
cdat=ctx.call('cdata', et)
image_url = "https://captcha.guard.qcloud.com/cap_union_new_getcapbysig?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw==&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=835414&forcestyle=undefined&rand=0.4457241752210961&sess={}&firstvrytype=1&showtype=point&rand=0.5730110856415294&vsig={}&img_index=1".format(
    d['asig'], sess.json()["sess"], vsig)
y_locte=re.search("Z=Number\(\"(.*?)\"", vsig_r.text)
y_locte=int(y_locte.group(1))
post_url="https://captcha.guard.qcloud.com/template/new_placeholder.html?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw==&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=102579&forcestyle=undefined".format(d['asig'])
holder=session.get(post_url)
if "tdc.js" in holder.text or "TDC.js" in holder.text:
    ase=False
else:
    ase=True
jsstr = jiami_js()
ctx = execjs.compile(jsstr)
cdat=ctx.call('getEncryptData','123')
client = suds.client.Client(url="http://120.79.184.213:8023/yzmmove.asmx?wsdl")
x_locate = client.service.GetTackXForDll(image_url,y_locte)
track=client.service.GetTackDataForDll(int(x_locate),cdat,ase)
track=json.loads(track)["Data"]
time_l = str(int(time.time() * 1000))
ticket_url = 'https://captcha.guard.qcloud.com/cap_union_new_verify?random={}'.format(time_l)
login_data='aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw==&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=846062&forcestyle=undefined&rand=0.388811798088319&sess={}&firstvrytype=1&showtype=point&subcapclass=10&vsig={}&ans={},{};&cdata=68&badbdd={}&websig={}&fpinfo=undefined&tlg=1&vlg=0_0_0&vmtime=_&vmData='.format(d['asig'], sess.json()["sess"], vsig,x_locate,y_locte,track,websig)
headers={'Host': 'captcha.guard.qcloud.com',
                       'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Language': 'zh-CN,zh;q=0.9',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Accept-Encoding': 'gzip, deflate, br',
                       'Referer': vsig_url,
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                       'X-Requested-With': 'XMLHttpRequest',
                       'Origin': 'https://captcha.guard.qcloud.com'}
tickek=session.post(ticket_url,data=login_data,headers=headers)
tickek=json.loads(tickek.text)["ticket"]
if not tickek:
    pass
headers = {'Host': 'captcha.guard.qcloud.com',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Content-Type': 'application/json; charset=UTF-8',
           'Accept-Encoding': 'gzip, deflate',
           'Referer': 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest',
           'x-form-id': 'mobile-signin-form',
           'Origin': 'http://dzswj.szgs.gov.cn'}
time_l = time.localtime(int(time.time()))
time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
login_data = '{"nsrsbh":"%s","nsrpwd":"%s","tagger":"%s","redirectURL":"","time":"%s"}' % (
    "440300771615767", '06fc3bcbd18ac83d45a8c369b7800d2e724f80c7', tickek, time_l)
login_url = 'http://dzswj.szgs.gov.cn/api/auth/txClientWt'
dl=session.post(login_url,data=login_data)
pass
# headers = {'Host': 'dzswj.szgs.gov.cn',
#            'Accept': 'application/json, text/javascript, */*; q=0.01',
#            # 'Cookie': 'DZSWJ_TGC = d412d6f36d0e4ee99e81018e53030bd8;tgw_l7_route = b94834e2974fcc2d07f1104d31093469;JSESSIONID = AB9D6CD57ECE264151B938716744BE7D',
#            'Accept-Language': 'zh-CN,zh;q=0.9',
#            'Content-Type': 'application/json; charset=UTF-8',
#            'Accept-Encoding': 'gzip, deflate',
#            'Referer': 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
#            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
#            'X-Requested-With': 'XMLHttpRequest',
#            'x-form-id': 'mobile-signin-form',
#            'Origin': 'http://dzswj.szgs.gov.cn'}
# time_l = time.localtime(int(time.time()))
# time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
# login_data = '{"mobile":"%s","password":"%s","tagger":"%s","redirectURL":"","time":"%s"}' % (
#     "13590240680", base64.b64encode("abcd1234".encode('utf8')).decode(), "rvU0tuqdXb8NUrbfm7VokN9Z_pgg5XXZMzaamCL20ImmUxThdSOzFP1143tm5F6gy4OVjMhsogE*", time_l)
# # self.logger.info(login_data)
# login_url = 'http://dzswj.szgs.gov.cn/api/web/general/txLogin'
# resp = requests.post(login_url, data=login_data,headers=headers)
# pass