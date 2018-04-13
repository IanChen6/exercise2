# -*- coding:utf-8 -*-
__author__ = 'IanChen'


import requests
import time
import random

static_proxy_url = "http://112.74.163.187:23128/__static__/proxies.txt"



def get_all_proxie():
    try_times = 0
    while try_times <= 3:
        try_times += 1
        try:
            proxy_list = []
            r = requests.get(static_proxy_url, timeout=10)
            if r is None or r.status_code != 200:
                continue
            line_list = r.text.split("\n")
            for line in line_list:
                line = line.strip("\r").strip("\n").strip()
                # if '7777' in line:
                #     line = line.replace('7777', '55555')
                # elif '8088' in line:
                #     line = line.replace('8088', '1088')

                if len(line) <= 0:
                    continue

                proxies = {'http': 'http://{}'.format(line), 'https': 'http://{}'.format(line)}
                proxy_list.append(proxies)
            return proxy_list
        except Exception:
            time.sleep(5)
            pass

    raise Exception('重试获取代理失败...')


if __name__ == "__main__":
    # proxy_list=get_all_proxie()
    # proxy=proxy_list[random.randint(0,len(proxy_list)-1)]
    # print(proxy)
    sess=requests.session()

    sess.proxies=  {'http': 'http://47.106.138.4:6832', 'https': 'http://47.106.138.4:6832'}
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
    i=1
    sleep_time = [3, 4, 3.5, 4.5, 3.2, 3.8, 3.1, 3.7, 3.3, 3.6]
    time.sleep(sleep_time[random.randint(0, 9)])
    d = sess.get('https://www.szcredit.org.cn/web/gspt/newGSPTDetail3.aspx?ID=f3023f7fa002450f85e117c12b619908',
                 headers=headers)
    d.encoding = 'gbk'
    ccc=d.apparent_encoding
    if "深圳市芃博科技有限公司" in d.text:
        print("pass")
    else:
        print("failed")

