# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
author      : 蛙鳜鸡鹳狸猿
create_time : 2016年 11月 01日 星期二 17:38:06 CST
program     : *_* script of manipulating pdf *_*
"""
import os
import sys
import PyPDF2
import PythonMagick
import ghostscript
from tempfile import NamedTemporaryFile

# reader = PyPDF2.PdfFileReader(open("申报表详情10014417000004730680.pdf", 'rb'))
pdffilename = "申报表详情10014417000004730680.pdf"
pdf_im = PyPDF2.PdfFileReader(open(pdffilename, "rb"))

print(1)
npage = pdf_im.getNumPages()
print('Converting %d pages.' % npage)
for p in range(npage):
    im = PythonMagick.Image()
    im.density('50')
    im.read(pdffilename + '[' + str(p) + ']')
    im.write('file_out-' + str(p) + '.png')
    # print pdffilename + '[' + str(p) +']','file_out-' + str(p)+ '.png'
