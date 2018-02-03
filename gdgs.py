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
import json
import requests
import re
#广东省国税局字母验证码获取
def captcha():
    with open('captcha.jpg', 'rb') as f:
        base64_data = str(base64.b64encode(f.read()))
        base64_data = base64_data[2:-1]
        post_data = {"a": 1, "b": base64_data}
        post_data = json.dumps({"a": 1, "b": base64_data})
        res = requests.post(url="http://192.168.18.113:8002/mycode.ashx", data=post_data)
        return res.text
def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*",_jsonp,re.S).group(1))
    except:
	    raise ValueError('Invalid I nput')


if __name__ == "__main__":
    captcha_url = 'http://diablo.alibaba.com/captcha/image/get.jsonp?sessionid=0152JIZgtMjy7iQLwB8JakWY8UZ7HS8jWWsNsyEz5dmrlu9uaK-QGKdj00wlUQsrLyzH8WKLcucyEd_p06Gt_dNOcLbhAnOtptD8kqkym2S5CqV7nOF9WRkln5KcYuNGCjZD-kY6nPwEpBr0iLFqY3xZa8avS4V45v-iLM86kCuE0&identity=FFFF0000000001780246&token=FFFF0000000001780246%3A1517293499043%3A0.7221443396695064&style=bak_default&callback=jsonp_07245746838959426'
    session = requests.session()
    # headers = {'Host': 'dzswj.szgs.gov.cn',
    #            'Accept': 'application/json, text/javascript, */*; q=0.01',
    #            'Accept-Language': 'zh-CN,zh;q=0.8',
    #            'Content-Type': 'application/json; charset=UTF-8',
    #            'Referer': 'http://dzswj.szgs.gov.cn/BsfwtWeb/apps/views/login/login.html',
    #            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    #            'x-form-id': 'mobile-signin-form',
    #            'X-Requested-With': 'XMLHttpRequest',
    #            'Origin': 'http://dzswj.szgs.gov.cn'
    #            }
    resp=session.get(captcha_url)
    if resp.status_code ==200:
        resp=loads_jsonp(resp.text)
        yanzhenma=resp['result']['data'][0]
        post_data = {"a": 1, "b": yanzhenma}
        post_data = json.dumps({"a": 1, "b": yanzhenma})
        res = requests.post(url="http://192.168.18.113:8002/mycode.ashx", data=post_data)

    # with open("captcha.jpg", "w") as f:
    #     f.write(yanzhenma)
    #     f.close()

    tagger = captcha()