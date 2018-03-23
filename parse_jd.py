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
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

def parse_pdf(pdf_path):
    fp = open(pdf_path, "rb")
    # 用文件对象创建一个pdf文档分析器
    parse_pdf = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    parse_pdf.set_document(doc)
    doc.set_parser(parse_pdf)
    doc.initialize()
    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF参数分析器
        laparams = LAParams()
        # 创建聚合器
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF页面解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # 循环遍历列表，每次处理一页的内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            # 使用页面解释器来读取
            interpreter.process_page(page)
            # 使用聚合器获取内容
            layout = device.get_result()
            results_last = ""
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            a = 0
            for out in layout:
                # 判断是否含有get_text()方法，图片之类的就没有
                # if hasattr(out,"get_text"):
                a += 1
                if isinstance(out, LTTextBoxHorizontal):
                    results = out.get_text()
                    if a == 21 or "%" in results_last:
                        pp = results.strip("").split("\n")
                        if len(pp) ==17:
                            sz=pp
                            print(sz)
                            break
                    results_last = results
            break
    pdf_dict = {}
    pdf_dict['实际已预缴所得税额'] = sz[11]
    pdf_dict['应补(退)所得税额'] = sz[13]
    pdf_dict['应纳所得税额'] = sz[9]
    pdf_dict['减:减免所得税额（请填附表3）'] = sz[10]
    print(pdf_dict)
    return pdf_dict

# parse_pdf("申报表详情10024418000001404474.pdf")
# parse_pdf("申报表详情10024418000003358200.pdf")

