# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     
   Description :
   Author :       ianchen
   date：          
-------------------------------------------------
   Change Activity:
                   2017/01/02:
-------------------------------------------------
"""
import base64
import json
from lxml import etree

import requests

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Accept-Encoding': 'gzip, deflate, br',
           'Connection': 'keep-alive',
           'Host': 'www.szcredit.org.cn',
           'Cookie': 'UM_distinctid=160a1f738438cb-047baf52e99fc4-e323462-232800-160a1f73844679; ASP.NET_SessionId=4bxqhcptbvetxqintxwgshll',
           'Origin': 'https://www.szcredit.org.cn',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Referer': 'https://www.szcredit.org.cn/web/gspt/newGSPTList.aspx?keyword=%u534E%u88D4&codeR=28',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest',
           }

yzm_url = 'https://www.szcredit.org.cn/web/WebPages/Member/CheckCode.aspx?'
session=requests.session()
yzm = session.get(url=yzm_url, headers=headers)

# 处理验证码
with open("yzm.jpg", "wb") as f:
    f.write(yzm.content)
    f.close()
with open('yzm.jpg', 'rb') as f:
    base64_data = str(base64.b64encode(f.read()))
    base64_data = "data:image/jpg;base64," + base64_data[2:-1]
    post_data = {"a": 2, "b": base64_data}
    post_data = json.dumps({"a": 2, "b": base64_data})
    res = session.post(url="http://39.108.112.203:8002/mycode.ashx", data=post_data)
    # print(res.text)
    f.close()

postdata = {'action': 'GetEntList',
            'keyword': '深圳市艺林达纸品有限公司',
            'type': 'query',
            'ckfull': 'false',
            'yzmResult': res.text
            }
resp1 = session.post(url='https://www.szcredit.org.cn/web/AJax/Ajax.ashx', headers=headers, data=postdata)
resp = resp1.json()
# if len(resp['resultlist']!=0):
#     result = resp['resultlist']
result = resp['resultlist']
if resp1 is not None and resp1.status_code == 200 and result:
    result_dict = result[0]
    print(result_dict["RecordID"])  # 获取ID
    detai_url = 'https://www.szcredit.org.cn/web/gspt/newGSPTDetail3.aspx?ID={}'.format(result_dict["RecordID"])
    detail = session.get(url=detai_url, headers=headers, timeout=30)
    detail.encoding=detail.apparent_encoding
    root = etree.HTML(detail.text)  # 将request.content 转化为 Element

    title = root.xpath('//*[@id="Table31"]//li[@class="current"]')
    t_list = []
    for t in title:
        tt = t.xpath(".//a[1]/text()")
        print(tt[0])
        t_list.append(tt[0])

    tb_list = []
    tb = root.xpath('//*[@id="Table31"]//table')#抓取table31
    for i in tb:
        data_json = []
        tb_detail = i.xpath(".//tr")
        for j in tb_detail:
            t = j.xpath('./td//text()')
            # lianjie = j.xpath('./td//@href')
            data_json.append(t)
            # data_json[t[0]]=t[1]
        # data_json=json.dumps(data_json,ensure_ascii=False)
        # print(data_json)
        tb_list.append(data_json)

    data_dict = {}
    for i in range(len(t_list)):
        data_dict[t_list[i]] = tb_list[i]
    print(data_dict)

    # if "登记备案信息" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["登记备案信息"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["登记备案信息"]=d1
    #     # dm = {}
    #     # dm["登记备案信息"] = d1
    #     # print(dm)
    #
    if "股东登记信息" in data_dict.keys():
        d1 = {}
        get_data = data_dict["股东登记信息"]
        d2 = {}
        for i in get_data[1:]:
            d3 = {}
            d3['出资额'] = i[1]
            d3['出资比例'] = i[2]
            d2[i[0]] = d3
        d1['股东名称'] = d2
        data_dict["股东登记信息"] = d1
        dm = {}
        dm["股东登记信息"] = d1
        print(dm)
    #
    # if "成员登记信息" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["成员登记信息"]
    #     for i in get_data[1:]:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["成员登记信息"]=d1
    #     # dm = {}
    #     # dm["成员登记信息"] = d1
    #     # print(dm)
    #
    # if "税务登记信息(国税)" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["税务登记信息(国税)"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["税务登记信息(国税)"]=d1
    #     # dm = {}
    #     # dm["税务登记信息(国税)"] = d1
    #     # print(dm)
    #
    # if "税务登记信息(地税)" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["税务登记信息(地税)"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["税务登记信息(地税)"]=d1
    #     # dm = {}
    #     # dm["税务登记信息(地税)"] = d1
    #     # print(dm)
    #
    # if "机构代码信息" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["机构代码信息"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["机构代码信息"]=d1
    #     # dm = {}
    #     # dm["机构代码信息"] = d1
    #     # print(dm)
    #
    # if "印章备案信息" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["印章备案信息"]
    #     d2 = {}
    #     for i in get_data[1:]:
    #         d3 = {}
    #         d3['印章编码'] = i[1]
    #         d3['审批日期'] = i[2]
    #         d3['备案日期'] = i[3]
    #         d3['备案情况'] = i[4]
    #         d3['详情'] = i[5]
    #         d2[i[0]] = d3
    #     d1['印章名称'] = d2
    #     data_dict["印章备案信息"] = d1
    #     # dm = {}
    #     # dm["印章备案信息"] = d1
    #     # print(dm)
    #
    # if "企业参保信息" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["企业参保信息"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["企业参保信息"]=d1
    #     # dm = {}
    #     # dm["企业参保信息"] = d1
    #     # print(dm)
    #
    # if "海关企业基本登记信息" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["海关企业基本登记信息"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["海关企业基本登记信息"]=d1
    #     # dm = {}
    #     # dm["海关企业基本登记信息"] = d1
    #     # print(dm)
    #
    # if "高新技术企业认定信息" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["高新技术企业认定信息"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["高新技术企业认定信息"]=d1
    #     # dm = {}
    #     # dm["高新技术企业认定信息"] = d1
    #     # print(dm)
    #
    # if "对外贸易经营者备案登记资料" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["对外贸易经营者备案登记资料"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["对外贸易经营者备案登记资料"]=d1
    #     # dm = {}
    #     # dm["对外贸易经营者备案登记资料"] = d1
    #     # print(dm)
    #
    # if "住房公积金缴存数据表" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["住房公积金缴存数据表"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["住房公积金缴存数据表"]=d1
    #     # dm = {}
    #     # dm["住房公积金缴存数据表"] = d1
    #     # print(dm)
    #
    # if "电子商务认证企业信息" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["电子商务认证企业信息"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["电子商务认证企业信息"]=d1
    #     # dm = {}
    #     # dm["电子商务认证企业信息"] = d1
    #     # print(dm)
    #
    # if "电子商务认证企业网站信息" in data_dict.keys():
    #     d1 = {}
    #     get_data = data_dict["电子商务认证企业网站信息"]
    #     for i in get_data:
    #         try:
    #             d1[i[0]] = i[1]
    #         except:
    #             d1[i[0]] = ""
    #     data_dict["电子商务认证企业网站信息"]=d1
    #     # dm = {}
    #     # dm["电子商务认证企业网站信息"] = d1
    #     # print(dm)
    #
    # if "企业年报信息" in data_dict.keys():
    #     get_data = data_dict["企业年报信息"]
    #     d2 = {}
    #     for i in range(int(len(get_data)/2)):
    #         d3 = {}
    #         d3['报送年度'] = get_data[i*2][1]
    #         d3['发布日期'] = get_data[i*2+1][1]
    #         d2[i+1] = d3
    #     data_dict["企业年报信息"] = d1
    #     # dm = {}
    #     # dm["企业年报信息"] = d2
    #     # print(dm)

    #企业变更信息
    try:
        title = root.xpath('//*[@id="Table123"]//li[@class="current"]')
        t_list = []
        for t in title:
            tt = t.xpath("./text()")
            print(tt[0])
            t_list.append(tt[0])

        tb_list = []
        tb = root.xpath('//*[@id="Table123"]//table')#抓取table31

        for i in tb:
            data_json = []
            tb_detail = i.xpath(".//tr")
            for j in tb_detail:
                t = j.xpath('./td//text()')
                data_json.append(t)
                # data_json[t[0]]=t[1]
            # data_json=json.dumps(data_json,ensure_ascii=False)
            # print(data_json)
            tb_list.append(data_json)

        data_dict = {}
        for i in range(len(t_list)):
            data_dict[t_list[i]] = tb_list[i]
        print(data_dict)

        if "企业变更信息" in data_dict.keys():
            d1 = {}
            get_data = data_dict["企业变更信息"]
            d2 = {}

            for i in get_data[1:]:
                d2['变更日期'] = i[1]
                d2['变更事项'] = i[2]
                d1[i[0]] = d2
            data_dict["企业变更信息"] = d1

    except:
        print("No exist")

    all_urls=[]
    all_gd=[]
    gdjg={}
    gdxx=root.xpath('//*[@id="tb_1"]//tr')
    for i in gdxx[1:]:
        lianjie=i.xpath('.//@href')[0]
        lianjie=lianjie.strip()
        gdm=i.xpath('./td[1]/text()')[0]
        print(lianjie)
        all_urls.append(lianjie)
        all_gd.append(gdm)
    for j in range(len(all_urls)):
        clean_dict={}
        gd_url="https://www.szcredit.org.cn/web/gspt/{}".format(all_urls[j])
        gd_resp=requests.get(url=gd_url,headers=headers)
        s=gd_resp.text
        if isinstance(s,str):
            s.encode(gd_resp.apparent_encoding)

        # gd_resp.encoding = 'utf8'
        root = etree.HTML(s)
        gdxq = root.xpath('//table[@class="list"]//tr')
        a=1
        for xq in gdxq[1:]:
            sb={}
            xx=xq.xpath('.//text()')
            clean=[]
            for s in xx:
                s=s.strip()
                if s.strip and s is not "":
                    clean.append(s)
            print(clean)
            sb["qymc"]=clean[0]
            sb["qyzch"]=clean[1]
            sb["qylx"]=clean[2]
            sb["clrq"]=clean[3]
            clean_dict["{}".format(a)]=sb
            a+=1
        gdjg[all_gd[j]]=clean_dict
    print(gdjg)


