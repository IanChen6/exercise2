# -*- coding:utf-8 -*-
from scrapy import crawler

__author__ = 'IanChen'


# def get_page(url, user_verify=True, need_login=True):
#     """
#     :param url: 待抓取url
#     :param user_verify: 是否为可能出现验证码的页面(ajax连接不会出现验证码，如果是请求微博或者用户信息可能出现验证码)，否为抓取转发的ajax连接
#     :param need_login: 抓取页面是否需要登录，这样做可以减小一些账号的压力
#     :return: 返回请求的数据，如果出现404或者403,或者是别的异常，都返回空字符串
#     """
#     crawler.info('本次抓取的url为{url}'.format(url=url))
#     count = 0
#
#     while count < max_retries:
#
#         if need_login:
#             # 每次重试的时候都换cookies,并且和上次不同,如果只有一个账号，那么就允许相同
#             name_cookies = Cookies.fetch_cookies()
#
#             if name_cookies is None:
#                 crawler.warning('cookie池中不存在cookie，正在检查是否有可用账号')
#                 rs = get_login_info()
#
#                 # 选择状态正常的账号进行登录，账号都不可用就停掉celery worker
#                 if len(rs) == 0:
#                     crawler.error('账号均不可用，请检查账号健康状况')
#                     # 杀死所有关于celery的进程
#                     if 'win32' in sys.platform:
#                         os.popen('taskkill /F /IM "celery*"')
#                     else:
#                         os.popen('pkill -f "celery"')
#                 else:
#                     crawler.info('重新获取cookie中...')
#                     login.excute_login_task()
#                     time.sleep(10)
#
#         try:
#             if need_login:
#                 resp = requests.get(url, headers=headers, cookies=name_cookies[1], timeout=time_out, verify=False)
#
#                 if "$CONFIG['islogin'] = '0'" in resp.text:
#                     crawler.warning('账号{}出现异常'.format(name_cookies[0]))
#                     freeze_account(name_cookies[0], 0)
#                     Cookies.delete_cookies(name_cookies[0])
#                     continue
#             else:
#                 resp = requests.get(url, headers=headers, timeout=time_out, verify=False)
#
#             page = resp.text
#             if page:
#                 page = page.encode('utf-8', 'ignore').decode('utf-8')
#             else:
#                 continue
#
#             # 每次抓取过后程序sleep的时间，降低封号危险
#             time.sleep(interal)
#
#             if user_verify:
#                 if 'unfreeze' in resp.url or 'accessdeny' in resp.url or 'userblock' in resp.url or is_403(page):
#                     crawler.warning('账号{}已经被冻结'.format(name_cookies[0]))
#                     freeze_account(name_cookies[0], 0)
#                     Cookies.delete_cookies(name_cookies[0])
#                     count += 1
#                     continue
#
#                 if 'verifybmobile' in resp.url:
#                     crawler.warning('账号{}功能被锁定，需要手机解锁'.format(name_cookies[0]))
#
#                     freeze_account(name_cookies[0], -1)
#                     Cookies.delete_cookies(name_cookies[0])
#                     continue
#
#                 if not is_complete(page):
#                     count += 1
#                     continue
#
#                 if is_404(page):
#                     crawler.warning('url为{url}的连接不存在'.format(url=url))
#                     return ''
#
#         except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, AttributeError) as e:
#             crawler.warning('抓取{}出现异常，具体信息是{}'.format(url, e))
#             count += 1
#             time.sleep(excp_interal)
#
#         else:
#             Urls.store_crawl_url(url, 1)
#             return page
#
#     crawler.warning('抓取{}已达到最大重试次数，请在redis的失败队列中查看该url并检查原因'.format(url))
#     Urls.store_crawl_url(url, 0)
#     return ''

#redis分布式
# coding=utf-8
import urllib
import re
import time
import redis

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'}
job_redis = redis.Redis(host='192.168.235.80') # host为主机的IP，port和db为默认值


class Clawer(object):

    identity = 'master'  # 或slaver

    def __init__(self):
        if self.identity == 'master':
            for i in range(20):  # 将需爬取的糗事百科前20页的url并存入urls集合
                url = 'http://www.qiushibaike.com/hot/page/%d/' % (i + 1)
                job_redis.sadd('urls', url)
        self.main()

    def get_content(self):
        """
        从糗事百科中获取故事
        :return: 故事列表
        """
        stories = []
        content_pattern = re.compile('<div class="content">([\w\W]*?)</div>([\w\W]*?)class="stats"') # 匹配故事内容（第一空）和是否含有图片（第二空）的模板
        pattern = re.compile('<.*?>') # 匹配包括括号及括号内无关内容的模板
        url = job_redis.spop('urls')
        while url: # 当数据库还存在网页url，取出一个并爬取
            try:
                request = urllib.Request(url, headers=headers)
                response = urllib.urlopen(request)
                text = response.read()
            except urllib.URLError as e: # 若出现网页读取错误捕获并输出
                if hasattr(e, "reason"):
                    print(e.reason)
            content = re.findall(content_pattern, text) # 获取含模板内容的列表
            for x in content:
                if "img" not in x[1]: # 过滤含图片的故事
                    x = re.sub(pattern, '', x[0])
                    x = re.sub('\n', '', x)
                    stories.append(x)
            url = job_redis.spop('urls')
            time.sleep(3)

        return stories

    def main(self):
        self.get_content()

if __name__ == '__main__':
    Clawer()