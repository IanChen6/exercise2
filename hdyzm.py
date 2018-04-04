# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     
   Description :
   Author :       ianchen
   date：          
-------------------------------------------------
   Change Activity:
                   2018/04/02:
-------------------------------------------------
"""
import base64
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
import re

import time
from suds.client import Client
import suds

session = requests.session()
add = session.get("http://dzswj.szgs.gov.cn/api/auth/queryTxUrl?json&_=1522658530831")
query = urlparse(add.json()['data']).query
d = dict([(k, v[0]) for k, v in parse_qs(query).items()])
sess_url = "https://captcha.guard.qcloud.com/cap_union_prehandle?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=835414&forcestyle=undefined&collect=xV6XnEXCTYbfMkq3nBXtS0c%2FV5AAZtsYtOqYjNBVDwvu0DT8YIl0%2BdlKp2UjKu0nw9G%2FTRvlmFAxGhorC%2BMq4MBMdkhfEnITqxh7Bad0q7e0ffClmuKkyX15QuZqT42Ej1RCgowaxr6ltGKYPgkVX6Fx%2B9pf6brr%2FIXbyp5trWz5UYDqJQ%2B%2B%2But2YkbKEwsE7%2BazqQ7y1qM9HHGC28%2Bz0iWZ6bjExtUYlbSH1g7zqEuq1FbFd1O%2B6xFztsvzI8lPuYhqwh0zUf4%2Fitr4PxPMGPo7MwUy%2BiJzaG%2F7bPCPvGB%2F9hGrC5V6V9e0uad0iK0FDDhPn0Ge%2F8mMlN7BoJzFAXkNrG1Iax2r0YqqLCffVwuDr1pHyhpq8wySNEYl70BeaVWdeDhT5QQd9Sujkg4EeDp5AEKDKrcvEhfcXrmKVFsH35s0XsFRr67VOyfKi%2BGDuJz4xCXH66ySt2BTycTC55FdfQ0Ef5uTuNFLkPgki2x09ePD7cHJXV7T86%2FkP%2Fi9GSEXBOy31%2B%2BZuLYInfEeiZRbuNEBMwyPa1MNrIMnUun4Dk5m7qP3aaga3UV24bZEhNWE0rYX3XrKLCgcw1JyD%2BF%2B%2F%2BUwcrewMBKzWcceZULq033o9HCRVaDzWxeyUNc%2FYLoGmJBCAhKRuKI35yAcYPZvtfEb6s29jqgMRTNkxSvJfIEHvAdBFYs44%2Fkf0P%2FdwiIHol1TITJVsbmlNehuFt39dXR15aOxbd4L8rv6YxW2j3rxBkWhaZwhgFUR066icYpz6%2FYgcsYbCoSt1Vxaz%2Fu8Wm06dmvyElvOFW2gdQbQYez1ju5x%2FfPFRZR%2B%2FCgOGa7nu8iMQHabdKlwoCRFN5ZHmqRcs01mA4iFQg6MB10aI%2FeuwB4JmHufAT1l5gCWfs1HqJBMRt5flx9KOY0uRi7usyloLQXzXnnCkK%2BRx78gP5n7Ex0ciAVivXjqaxpQKpmgv94IplHxliSNfglULAYvzpr9kSS5saFYSNjP7w0HCyrbRbl6%2B2STCU1MKzRS8UxJ2anCrkyC4vfUeXZY6CIoGVsW9BloXO%2BD7ZSLBgZkPscWv%2FOt8TFywebfHm7YtMfjvCaWCnkT5MtkVrbTUp3vaycuMKB7z%2Fen7yfTP2vkEfmPWxQQtNDKjIKEGtno0EA0SSihw6pfk1hZHD%2BeOji0oQ4IHr2EjvXtibIvKLIOCLRMrMAlSxl%2Fy48utVt4LJa6%2BBLZhNzkuvbgoJL9ss1NZdIt7GIEOhY3HV%2FVnRbMv8zs7pKKqx5Mx%2BjQ61yCjmFHO6ldQrNuKb%2BMYKAennyD9XXd4hFguk13iFcb8luOyJvwg4%2BobY3X5lY975qsxK%2BYZfEwqNE7EatDGCqHCJnM23GdfMKq4ibSTMQe%2FOLziUHKZtI3x%2FvroZ4Fue0ygY5Lmt0cZCK7ik2Xu5U6jcxh1aegAFFzZh18aQPVyGL1Z%2B4Ugg4A0WDgkk0T%2Fzy6FRo8TWf0b%2BbN8Y6HEzty2HaRtU6y2SfifxTmo81uwqAV4GXhzwwNr2zJWoAFnL8pV1119CSXEcXeDxmTDnD4qMmgcBezHWthydUcK66XhZXIlwNQ6yoCTBS75ifUCD%2FImJfYPdClKurBU6MTIvHTIvhb5daodgCEJM%2BwQWPAGOs%2FjRrs7o2%2BopVMQLLDBqcyrDdJrI%2B1XM69Z5qXVxdhTVNayG22R545iv2tvafQr7Z4SAqJr6P7EYupMfgVTCuHyOMJEG0SJd4f3d4arqF%2Bg0gY5drdpJMp94P06X5YovTwldW3t8fIB2QhAqjSRCCr&firstvrytype=1&random=0.017271072963999323&_=1522664696316".format(
    d['asig'])
sess = session.get(sess_url)
vsig_url = "https://captcha.guard.qcloud.com/cap_union_new_show?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=835414&forcestyle=undefined&rand=0.4457241752210961&sess={}&firstvrytype=1&showtype=point".format(
    d['asig'], sess.json()["sess"])
vsig_r = session.get(vsig_url)
ad = re.search("Q=\"(.*?)\"", vsig_r.text)
vsig = ad.group(1)
image_url = "https://captcha.guard.qcloud.com/cap_union_new_getcapbysig?aid=1252097171&asig={}&captype=&protocol=https&clientype=2&disturblevel=&apptype=&curenv=open&ua=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS81My4wLjI3ODUuMTA0IFNhZmFyaS81MzcuMzYgQ29yZS8xLjUzLjM0ODUuNDAwIFFRQnJvd3Nlci85LjYuMTIxOTAuNDAw&uid=&cap_cd=&height=40&lang=2052&fb=1&theme=&rnd=835414&forcestyle=undefined&rand=0.4457241752210961&sess={}&firstvrytype=1&showtype=point&rand=0.5730110856415294&vsig={}&img_index=1".format(
    d['asig'], sess.json()["sess"], vsig)
query_for_ticket = urlparse(image_url).query
ticket_d = dict([(k, v[0]) for k, v in parse_qs(query_for_ticket).items()])
resp = session.get(image_url)
con = str(base64.b64encode(resp.content))[2:-1]
client = suds.client.Client(url="http://39.108.112.203:8023/yzmmove.asmx?wsdl")
# client = suds.client.Client(url="http://192.168.18.101:1421/SZYZService.asmx?wsdl")
auto = client.service.GetYZCodeForDll(con)
time_l = str(int(time.time() * 1000))
ticket_url = 'https://captcha.guard.qcloud.com/cap_union_new_verify?random={}'.format(time_l)
login_data = '{"aid":"1252097171","asig":"%s","captype":"","protocol":"https","clientype":"2","disturblevel":"",' \
             '"apptype":"","curenv":"open","ua":%s,"uid":"","cap_cd":"","height":"40","lang":"2052","fb":"1","theme":"","rnd":"669593",' \
             '"forcestyle": "undefined", ""rand": "0.9902325716079976","sess": "%s","firstvrytype":"1","showtype":"point","subcapclass":"10",' \
             '"vsig":"%s","ans":"%s,70;","cdata":"76","babcdb":"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","websig":"352fa10777672294121870268156c284b4094a04112ef5d66dcbd9f9a5de452d3be975a8ee4541b403c66995ce584a36ec64faeae1337a1c1d746765580eed65","fpinfo":"undefined","tlg":"1","vlg":"0_0_0","vmtime":"_","vmData":""}' % (ticket_d['asig'], ticket_d['ua'], ticket_d['sess'], ticket_d['vsig'],auto)
headers={'Host': 'captcha.guard.qcloud.com',
                       'Accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                       'Referer': vsig_url,
                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                       'X-Requested-With': 'XMLHttpRequest',
                       'Origin': 'https://captcha.guard.qcloud.com'}
tickek=session.post(ticket_url,data=login_data,headers=headers)
print(auto)
