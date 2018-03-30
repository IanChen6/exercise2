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
#pdf2读取pdf
# from PyPDF2 import PdfFileReader, PdfFileWriter
# infn = '季度申报表详情91441900MA4UQGA86C.pdf'
# outfn = 'outfn.pdf'
# # 获取一个 PdfFileReader 对象
# pdf_input = PdfFileReader(open(infn, 'rb'))
# # 获取 PDF 的页数
# page_count = pdf_input.getNumPages()
# print(page_count)
# # 返回一个 PageObject
# page = pdf_input.getPage(1)
#
# # 获取一个 PdfFileWriter 对象
# pdf_output = PdfFileWriter()
# # 将一个 PageObject 加入到 PdfFileWriter 中
# pdf_output.addPage(page)
# # 输出到文件中
# pdf_output.write(open(outfn, 'wb'))

import os
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

#将一个pdf转换成txt(转换失败，部分内容未捕捉到)
# def pdfTotxt(filepath,outpath):
#     try:
#         fp = open(filepath, 'rb')
#         outfp=open(outpath,'w')
#         parse_pdf = PDFParser(fp)
#         # 创建一个PDF文档
#         doc = PDFDocument()
#         parse_pdf.set_document(doc)
#         doc.set_parser(parse_pdf)
#         doc.initialize()
#         #创建一个PDF资源管理器对象来存储共享资源
#         #caching = False不缓存
#         rsrcmgr = PDFResourceManager(caching = False)
#         # 创建一个PDF设备对象
#         laparams = LAParams()
#         device = TextConverter(rsrcmgr, outfp,laparams=laparams)
#         #创建一个PDF解析器对象
#         interpreter = PDFPageInterpreter(rsrcmgr, device)
#         for page in doc.get_pages():
#             page.rotate = page.rotate % 360
#             interpreter.process_page(page)
#         #关闭输入流
#         fp.close()
#         #关闭输出流
#         device.close()
#         outfp.flush()
#         outfp.close()
#     except Exception as e:
#          print ("Exception:%s",e)
# pdfTotxt('季度申报表详情91441900MA4UQGA86C.pdf','test.txt')

def with_pdf(pdf_doc, fn, pdf_pwd, *args):
    """Open the pdf document, and apply the function, returning the results"""
    result = None
    try:
        # open the pdf file
        fp = open(pdf_doc, 'rb')
        # create a parser object associated with the file object
        parser = PDFParser(fp)
        # create a PDFDocument object that stores the document structure
        doc = PDFDocument(parser, pdf_pwd)
        # connect the parser and document objects
        parser.set_document(doc)
        # supply the password for initialization

        if doc.is_extractable:
            # apply the function and return the result
            result = fn(doc, *args)

        # close the pdf file
        fp.close()
    except IOError:
        # the file doesn't exist or similar problem
        pass
    return result

def _parse_toc (doc):
    toc = []
    try:
        outlines = doc.get_outlines()
        for (level, title, dest, a, se) in outlines:
            toc.append((level, title))
    except:
        pass
    return toc
def get_toc(pdf_doc, pdf_pwd=''):
    return with_pdf(pdf_doc, _parse_toc, pdf_pwd)

get_toc("季度申报表详情91441900MA4UQGA86C.pdf")