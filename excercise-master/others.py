# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     data_10jqka_com_cn
   Description :
   Author :       tangxin
   date：          2017/11/22
-------------------------------------------------
   Change Activity:
                   2017/11/22:
-------------------------------------------------
"""

import sys

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pyquery import PyQuery

sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")

from sites.common.tx_session import proxy_session
from cStringIO import StringIO
from conf import m_settings
from libs.loghandler import getLogger
from libs.pybeanstalk import PyBeanstalk
from libs.taskbase import TaskBase
from libs.thrift_utils import thrift_object_generator, thrift_serialize

__author__ = 'tangxin'
BASIC_URL = "http://data.10jqka.com.cn/market/ggsd/board/2/order/asc/page/{}/"
MAX_RETRY = 10
TIME = 60


class data_10jqka_com_cn(TaskBase):
    def __init__(self):
        super(data_10jqka_com_cn, self).__init__()
        self.logger = getLogger(self.__class__.__name__, console_out=True, level="debug")
        self.session_id = None
        self.beanstalk = PyBeanstalk(m_settings.BEANSTALKD2.get('host'), m_settings.BEANSTALKD2.get('port'))
        self.output_tube = 'extract_info'
        self.topic_id = 226  # ,行业新闻
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
        }

    def start(self):
        """
        主函数
        :return:
        """
        self.logger.info("开始抓取")
        session = proxy_session()
        pages = self.get_pages()
        if pages is None:
            self.logger.error("初始化页码出错,程序退出")
            sys.exit()
        for i in xrange(1, pages + 1):
            url = BASIC_URL.format(i)
            resp = session.get(url=url, timeout=TIME, headers=self.headers)
            if resp is None or resp.content == '':
                self.logger.info("获取{}失败".format(url))
                continue
            self.parse(resp)
        self.logger.info("完成抓取,程序正常退出")

    def get_pages(self):
        """
        获取页码信息,失败直接退出
        :return: 页码 int类型
        """
        session = proxy_session()
        url = BASIC_URL.format(1)
        resp = None
        try:
            resp = session.get(url, timeout=TIME, headers=self.headers)
        except Exception as e:
            self.logger.error("访问{}出错".format(url))
            self.logger.exception(e)
        if resp is None:
            self.logger.error('访问{}出错'.format(url))
            return None
        doc = PyQuery(resp.content, parser='html')
        pages = doc.find("span.page_info").text()
        if pages is '':
            self.logger('未找到总页码')
            return None
        return int(pages.split('/')[1])

    def parse(self, resp):
        """
        对列表页html进行解析
        :param resp:
        :return:
        """
        try:
            doc = PyQuery(resp.content, parser="html")
        except:
            return
        all_url = doc.find("table[class='m-table J-ajax-table']").find("tr").items()
        for item in all_url:
            publish_time = item.find("td.tc").eq(0).text()
            if publish_time == "":
                continue
            sub_item = item.find("div.clearfix").find("a").items()
            self.parse_list(sub_item, publish_time)

    def parse_list(self, sub_item, publish_time):
        """
        解析函数,提取关键字段,构造data
        :param sub_item: 子链接(pdf链接)
        :param publish_time: 发布时间
        :return:
        """
        for item in sub_item:
            data = {}
            url = item.attr("href")
            title = item.text()
            if "pdf" not in url:
                continue
            summary = self.parse_detail(url)
            if summary is None:
                return
            if len(summary) < 10:
                return
            data["url"] = url
            data["title"] = title
            data["summary"] = summary
            data["_site_record_id"] = url
            data["publish_time"] = publish_time
            self.put_bean(url=url, data=data)

    def parse_detail(self, url):
        """
        详情页解析
        :param url:
        :return:
        """
        session = proxy_session()
        resp = None
        try:
            resp = session.get(url, timeout=TIME, headers=self.headers)
        except Exception as e:
            self.logger.error("访问{}出错".format(url))
            self.logger.exception(e)
        if resp is None:
            self.logger.info('获取{}失败'.format(url))
            return

        return self.pdf_parse(resp.content)

    def pdf_parse(self, content):
        """
        调用pdf转换函数
        :param content:
        :return:
        """
        with open("a.pdf", "w") as f:
            f.write(content)
        try:
            text = self.convert_pdf_2_text("a.pdf")
        except:
            self.logger.info("pdf转换出错")
            return None
        return text

    # 将一个pdf转换成txt
    @staticmethod
    def convert_pdf_2_text(path):
        """
        pdf转换为txt
        :param path: pdf路径
        :return: 解析完的正文信息
        """
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        with open(path, 'rb') as fp:
            for page in PDFPage.get_pages(fp, set()):
                interpreter.process_page(page)
            text = retstr.getvalue()
        device.close()
        retstr.close()
        return text

    def put_bean(self, url, data):
        """
        发送给beanstalk
        :param url:
        :param data: 需要发送的数据
        :return:
        """
        # pdb.set_trace()
        obj = thrift_object_generator.gen_pageparse_info(url, data, topic_id=self.topic_id)
        self.logger.info('put beanstalk url:%s title:%s' % (url, data.get('title', '')))
        self.beanstalk.put(self.output_tube, thrift_serialize.thriftobj2bytes(obj))


if __name__ == "__main__":
    worker = data_10jqka_com_cn()
    worker()