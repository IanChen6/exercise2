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
import time
from suds.client import Client
import suds
import requests
import hashlib
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from proxy_ceshi import get_all_proxie
import sys

def jiami(pwd):
    h = hashlib.sha1(pwd.encode('utf8')).hexdigest()
    return h

def tagger2(tupian,md):
    while True:
        # formdata = {'CompanyID': 123456, 'BatchID': "1215454545", 'JobName': "pyj", 'CodeMD5': md, 'CodeData': tupian}
        # resp=requests.get(url="http://192.168.18.101:1421/SZYZService.asmx?wsdl",data=formdata)
        client = suds.client.Client(url="http://39.108.112.203:8701/SZYZService.asmx?wsdl")

        result = client.service.SetYZImg(123456, "1215454545", "pyj", md, tupian)
        # flag = login("91440300MA5DRRFB45", "10284784", result)
        for i in range(30):
            result1 = client.service.GetYZCode(md)
            if result1 is not None:
                result1 = str(result1)
                return result1
            time.sleep(10)
        break

def tagger(tupian,md):
    while True:
        # formdata = {'CompanyID': 123456, 'BatchID': "1215454545", 'JobName': "pyj", 'CodeMD5': md, 'CodeData': tupian}
        # resp=requests.get(url="http://192.168.18.101:1421/SZYZService.asmx?wsdl",data=formdata)
        client = suds.client.Client(url="http://39.108.112.203:8701/SZYZService.asmx?wsdl")
        auto = client.service.GetYZCodeForDll(tupian)
        if auto is not None:
            result1 = str(auto)
            return result1
        if auto is None:
            return auto


        break

def login(user, pwd):
    try_times = 0
    while try_times <= 5:
        try_times += 1
        session = requests.session()
        # proxy_list = get_all_proxie()
        # proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]

        # proxy=sys.argv[1]
        # session.proxies = {'http': 'http://39.108.220.10:6832', 'https': 'http://39.108.220.10:6832'}
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
        if tag is None:
            continue
        jyjg = session.post(url='http://dzswj.szgs.gov.cn/api/checkClickTipCaptcha', data=tag)
        time_l = time.localtime(int(time.time()))
        time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
        tag = json.dumps(tag)
        login_data = '{"nsrsbh":"%s","nsrpwd":"%s","redirectURL":"","tagger":%s,"time":"%s"}' % (
            user, jiami(pwd), tag, time_l)
        login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
        resp = session.post(url=login_url, data=login_data)
        # panduan=resp.json()['message']
        # self.logger(panduan)
        try:
            if "验证码正确" in jyjg.json()['message']:
                if "登录成功" in resp.json()['message']:
                    print('登录成功')
                    cookies = {}
                    for (k, v) in zip(session.cookies.keys(), session.cookies.values()):
                        cookies[k] = v
                    postdata = 'djxh=10114403000027667394&sxDm=&sqrqq=20171026&sqrqz=20180126&sxlxDm=&blztDm=1'
                    resp = session.post("http://dzswj.szgs.gov.cn/wycx/wycxAction_queryWsxx.do", data=postdata,
                                        timeout=30)
                    data=resp.json()
                    data=data['data']
                    for i in data:
                        if "发票代开" in i['dbsxmc']:
                            sxmc=i['dbsxmc']
                            sxlx=i['zlsfqq']
                            if 'N'==sxlx:
                                sxlx="全流程无纸化"
                            else:
                                sxlx="预申请"
                            sqrq=i['dbsxrq']
                            blzt=i['dbsxzt']
                            if i['swsxDm']!="110897":
                                if blzt == "10" or blzt == "03":
                                    blzt = "正在受理，已发审核部门审批，请耐心等待审批结果"
                                elif blzt == "05" or blzt == "04" or blzt == "01":
                                    blzt = "已办结待签收"
                                elif blzt == "00":
                                    blzt = "待审查资料"
                                elif blzt == "02":
                                    blzt = "不予受理"
                                elif blzt == "06":
                                    blzt = "待补正资料"
                                elif blzt == "11":
                                    blzt = "结束"
                            else:
                                blzt="已办结"
                            xqdata='sqxh={}'.format(i['sqxh'])
                            ckxq=session.post("http://dzswj.szgs.gov.cn/wycx/wycxAction_viewSwsqyl.do",data=xqdata)
                            xq=ckxq.json()
                            xq=xq['data']
                            xq=xq['data']
                            sum={}
                            dkfp={}
                            dkfp["普通发票：服务"]=xq['dkfpjefw']
                            dkfp["普通发票：货物"]=xq['dkfpje']
                            dkfp["专用发票：服务"]=xq['zpdkjefw']
                            dkfp["专用发票：货物"]=xq['zpdkjehw']
                            sum["代开发票信息概览"]=dkfp
                            xf={}
                            xf['纳税人识别号']=xq['xfnsrsbh']
                            xf['纳税人名称']=xq['xfnsrmc']
                            xf['地址']=xq['xfdz']
                            xf['经营范围']=xq['xfjyfw']
                            xf['开户银行']=xq['nsrxx']['xhfkhyhMc']
                            xf['银行账号']=xq['xfyhzh']
                            xf['经办人']=xq['xfjbr']
                            xf['联系电话']=xq['xflxdh']
                            xf['备注']=xq['bz']
                            sum["销售方纳税人信息"]=xf
                            gf={}
                            gf['纳税人识别号']=xq['gfnsrsbh']
                            gf['纳税人名称']=xq['gfnsrmc']
                            gf['地址']=xq['gfdz']
                            gf['银行营业网点名称']=xq['ghfyhyywdmc']
                            gf['开户银行']=xq['gfkhyhText']
                            gf['银行账号']=xq['gfyhzh']
                            gf['经办人']=xq['xfjbr']
                            gf['联系电话']=xq['gflxdh']
                            gf['代开类型']=xq['dkfplxText']
                            gf['征收品目']=xq['zspmText']
                            sum["购买方纳税人信息"]=gf
                            fwmc={}
                            fwlist=xq["zzsdkfpGrid"]
                            trans={}
                            a=1
                            for j in fwlist:
                                trans['货物或应税劳务名称、服务名称'] = fwlist['hwlwmc']
                                trans['金额'] = fwlist['je']
                                trans['数量'] = fwlist['hlsl']
                                trans['单位'] =fwlist['jldwMc']
                                trans['单价'] = fwlist['hldj']
                                trans['规格型号'] = fwlist['ggxh']
                                trans['金额合计']=xq['jehj']
                                fwmc[a]=trans
                                a+=1
                            sum["货物或应税劳务名称、服务名称"] = fwmc
                            ynsk={}
                            skxx=xq['nsrxx']







                    return cookies
                else:
                    time.sleep(3)
        except Exception as e:
            print("登录出错")
        print("重试")
    try_times = 0
    while try_times <= 10:
        try_times += 1
        session = requests.session()
        # proxy_list = get_all_proxie()
        # proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]

        # proxy=sys.argv[1]
        # session.proxies = {'http': 'http://39.108.220.10:6832', 'https': 'http://39.108.220.10:6832'}
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
        tag=tagger2(tupian,md)
        # tag_data=json.dumps(tag,ensure_ascii=False)
        # for i in tag:
        # tag=tag.replace("\"","'")
        if tag is None:
            continue
        jyjg = session.post(url='http://dzswj.szgs.gov.cn/api/checkClickTipCaptcha', data=tag)
        time_l = time.localtime(int(time.time()))
        time_l = time.strftime("%Y-%m-%d %H:%M:%S", time_l)
        tag = json.dumps(tag)
        login_data = '{"nsrsbh":"%s","nsrpwd":"%s","redirectURL":"","tagger":%s,"time":"%s"}' % (
            user, jiami(pwd), tag, time_l)
        login_url = 'http://dzswj.szgs.gov.cn/api/auth/clientWt'
        resp = session.post(url=login_url, data=login_data)
        # panduan=resp.json()['message']
        # self.logger(panduan)
        try:
            if "验证码正确" in jyjg.json()['message']:
                if "登录成功" in resp.json()['message']:
                    print('登录成功')
                    cookies = {}
                    for (k, v) in zip(session.cookies.keys(), session.cookies.values()):
                        cookies[k] = v
                    postdata = 'djxh=&sxDm=&sqrqq=20171026&sqrqz=20180126&sxlxDm=&blztDm='
                    resp = session.post("http://dzswj.szgs.gov.cn/wycx/wycxAction_queryWsxx.do", data=postdata,
                                        timeout=30)
                    return cookies

                else:
                    time.sleep(3)
        except Exception as e:
            print("登录出错")
        print("重试")
    return False

def get_ck(dlck):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
    dcap["phantomjs.page.settings.loadImages"] = True
    browser = webdriver.PhantomJS(executable_path='D:/BaiduNetdiskDownload/phantomjs-2.1.1-windows/bin/phantomjs.exe',
                                  desired_capabilities=dcap)
    browser.implicitly_wait(10)
    browser.get(url='http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html')
    browser.delete_all_cookies()

    for (k, v) in dlck.items():
        browser.add_cookie({
                'domain': '.szgs.gov.cn',  # 此处xxx.com前，需要带点
                'name': k,
                'value': v,
                'path': '/',
                'expires': None})

    browser.get('http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/myoffice/myoffice.html')
    page = browser.page_source
    browser.find_element_by_css_selector("#wqwsbspan").click()
    pa = browser.page_source
    if '我的定制功能' in page:
        print("登录成功")



if __name__ == "__main__":
    dlck=login("9144030008389925X7", "y20170410")


    jsoncookies = json.dumps(dlck)
    if "账号和密码不匹配" in jsoncookies:
        print("bpp")
    get_ck(dlck)
    pass
