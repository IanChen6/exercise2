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

import time
# from urllib.parse import urlencode
from oauthlib.common import urldecode
from suds.client import Client
import suds
import requests
import hashlib


def jiami(pwd):
    h = hashlib.sha1(pwd.encode('utf8')).hexdigest()
    return h

def tagger(tupian,md):
    while True:
        # formdata = {'CompanyID': 123456, 'BatchID': "1215454545", 'JobName': "pyj", 'CodeMD5': md, 'CodeData': tupian}
        # resp=requests.get(url="http://192.168.18.101:1421/SZYZService.asmx?wsdl",data=formdata)
        client = suds.client.Client(url="http://39.108.112.203:8701/SZYZService.asmx?wsdl")
        auto = client.service.GetYZCodeForDll(tupian)
        if auto is not None:
            tagger = str(auto)
            flag = login("91440300MA5DRRFB45", "10284784", tagger)
            break
        result = client.service.SetYZImg(123456, "1215454545", "pyj", md, tupian)
        # flag = login("91440300MA5DRRFB45", "10284784", result)

        for i in range(10):
            result1 = client.service.GetYZCode(md)
            result1 = str(result1)
            return result1
            time.sleep(10)
        break

def login(user, pwd):
    try_times = 0
    while try_times <= 5:
        try_times += 1
        session = requests.session()
        # headers = {'Host': 'dzswj.szgs.gov.cn',
        #            'Accept': 'application/json, text/javascript, */*; q=0.01',
        #            'Accept-Language': 'zh-CN,zh;q=0.9',
        #            'Accept-Encoding': 'gzip, deflate',
        #            'Connection': 'keep - alive',
        #            # 'Cookie': 'JSESSIONID = DD75E6C40F846782C33094C5837BDEEE;tgw_l7_route = 41b5a189c640d63f085c449f4ffcdefa;DZSWJ_TGC = ba5105cc969045fd85b540206737a7d0',
        #            'Content-Type': 'application/json; charset=UTF-8',
        #            'Referer': 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
        #            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        #            'x-form-id': 'mobile-signin-form',
        #            'X-Requested-With': 'XMLHttpRequest',
        #            'Origin': 'http://dzswj.szgs.gov.cn'
        #            }
        headers = {'Host':'dzswj.szgs.gov.cn',
                   'Accept':'application/json, text/javascript, */*; q=0.01',
                   'Accept-Language': 'zh-CN,zh;q=0.8',
                   'Content-Type':'application/json; charset=UTF-8',
                   'Referer':'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                    'x-form-id':'mobile-signin-form',
                    'X-Requested-With':'XMLHttpRequest',
                   'Origin':'http://dzswj.szgs.gov.cn'}
        session.get("http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html",headers=headers)
        captcha_url = 'http://dzswj.szgs.gov.cn/tipCaptcha'
        # tupian_resp = session.get(url=captcha_url,headers=headers,timeout=10)
        tupian_resp = session.get(url=captcha_url,timeout=10)
        tupian_resp.encoding = 'utf8'
        tupian = tupian_resp.json()
        image = tupian['image']
        tipmessage = tupian["tipMessage"]
        tupian = json.dumps(tupian, ensure_ascii=False)
        m = hashlib.md5()
        tupian1 = tupian.encode(encoding='utf8')
        m.update(tupian1)
        md = m.hexdigest()
        print(md)
        tag=tagger(tupian,md)
        # tag_data=json.dumps(tag,ensure_ascii=False)
        # for i in tag:
        # tag=tag.replace("\"","'")
        jyjg=session.post(url='http://dzswj.szgs.gov.cn/api/checkClickTipCaptcha',data=tag)
        time_l = time.localtime(int(time.time()))
        time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
        tagg=json.dumps(tag)
        login_data = {"nsrsbh": user, "nsrpwd": jiami(pwd), "redirectURL": "", "tagger": tag, "time": time_l}
        login_data=json.dumps(login_data,ensure_ascii=False)
        # login_data['tagger']="[{\"x\":227,\"y\":76},{\"x\":82,\"y\":104},{\"x\":283,\"y\":24}]"
        # login_data=login_data.replace("\\\"","'")
        # login_data=json.loads(login_data)
        login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
        resp = session.post(url=login_url,data=login_data)
        if resp.json()['success'] == True:
            print('登录成功')
            cookies = {}
            for (k, v) in zip(session.cookies.keys(), session.cookies.values()):
                cookies[k] = v
            return cookies, session
        else:
            time.sleep(3)
    return False


if __name__ == "__main__":
    login("91440300MA5DRRFB45", "10284784")
