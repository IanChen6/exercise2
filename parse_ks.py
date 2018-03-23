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
import re
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument


def parse_ndpdf(pdf_path):
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
        pagemumber=0
        for page in doc.get_pages():
            # 使用页面解释器来读取
            interpreter.process_page(page)
            # 使用聚合器获取内容
            layout = device.get_result()
            results_last = ""
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            a = 0
            gd = []
            zj = []
            hm = []
            xingzhi = []
            bili = []
            guoji = []
            pagemumber+=1
            for out in layout:
                # 判断是否含有get_text()方法，图片之类的就没有
                # if hasattr(out,"get_text"):
                a += 1
                if isinstance(out, LTTextBoxHorizontal):
                    results = out.get_text()
                    # 解析亏损表
                    if a == 1:
                        if results != "A106000企业所得税弥补亏损明细表\n" and results != "中华人民共和国企业所得税年度纳税申报表（A类）\n" and results != "A000000企业基础信息表\n" and pagemumber!=3:
                            break
                        else:
                            if pagemumber==3:
                                biaoge="A000000企业基础信息表\n"
                            else:
                                biaoge = results
                            gd = False
                    # print(results)
                    # results_last = results
                    if biaoge == "A106000企业所得税弥补亏损明细表\n" and results_last == '前五年度\n前四年度\n前三年度\n前二年度\n前一年度\n本年度\n可结转以后年度弥补的亏损额合计\n':
                        nf = results.strip("").split("\n")
                        print(nf)
                    if biaoge == "A106000企业所得税弥补亏损明细表\n":
                        if results_last == '2\n' or results_last == "2011\n2012\n2013\n2014\n2015\n2016\n":
                            nstzhs = results.strip("").split("\n")
                            if len(nstzhs) == 7:
                                nstzhsd = nstzhs
                                print(nstzhsd)
                    # 解析年度纳税申报表
                    if biaoge == "中华人民共和国企业所得税年度纳税申报表（A类）\n":
                        if results_last == '金额\n' and a == 11:
                            sz = results.strip("").split("\n")
                            print(sz)
                        elif a==10 and "%" in results and  "0.00" in results:
                            sz = results.strip("").split("\n")
                            print(sz)
                    # 解析基础信息表
                    if biaoge == "A000000企业基础信息表\n":
                        if "备抵法" in results or "直接核销法" in results:
                            cbjj = results.strip("").split("\n")
                            print(cbjj)
                    if biaoge == "A000000企业基础信息表\n" and a == 8:
                        kjzz = results.strip("").split("\n")
                        try:
                            # match = re.search(r'201适用的会计准则或会计制度 (.*?)', kjzz[0])
                            # print(match.group(1))
                            kjzzz = kjzz[0].split(" ")
                            kjzzzd = kjzzz[1]
                            print(kjzzzd)
                        except:
                            kjzzzd = ""
                            print(kjzzzd)
                    if biaoge == "A000000企业基础信息表\n" and "否" in results:
                        jcx = results.strip("").split("\n")
                        if len(jcx) == 6:
                            jcxx = jcx
                            print(jcxx)
                        else:
                            continue
                    if biaoge == "A000000企业基础信息表\n" and "301企业主要股东" in results:
                        gd = True
                        gdxx = []
                    if biaoge == "A000000企业基础信息表\n" and gd:
                        if "证件种类" not in results and "主要股东" not in results and "经济性质" not in results and "投资比例" not in results and "国籍" not in results and "302中国境内" not in results and "公司财务室" not in results \
                                and "备抵法" not in results and "直接核销法" not in results and "人民币" not in results and "单位财务室" not in results and "证件号码" not in results:
                            gdxx.append(results)
                    results_last = results
    pdf_dict = {}
    try:
        pdf_dict['所属行业明细'] = jcxx[2]
        pdf_dict['从业人数'] = jcxx[3]
        pdf_dict['存货计价方法'] = cbjj[1]
        pdf_dict['企业会计准则为'] = kjzzzd
        index = 0
        for gl in gdxx:
            index += 1
            if "居民身份证" in gl or "营业执照" in gl or "其他单位证件" in gl:
                zjhm = gl.replace("\n", "")
                if "居民身份证" in zjhm[:8]
                    zjhm = zjhm.split('居民身份证')[1:]

                clean = []
                for g in zjhm:
                    if "营业执照" in g:
                        yy = g.split("营业执照")
                        if len(yy[0]) != 0:
                            clean.append("居民身份证")
                            clean.append(yy[0])
                        for zz in yy[1:]:
                            clean.append("营业执照")
                            clean.append(zz)
                    elif "其他单位证件" in g:
                        yy = g.split("其他单位证件")
                        if len(yy[0]) != 0:
                            clean.append("居民身份证")
                            clean.append(yy[0])
                        for zz in yy[1:]:
                            clean.append("其他单位证件")
                            clean.append(zz)
                    else:
                        clean.append("居民身份证")
                        clean.append(g)
                break
        tzxx = []
        end = index + len(clean)
        for tz in gdxx[index:end]:
            tz = tz.replace("\n", "")
            tzxx.append(tz)
        gj = []
        end2 = end + int(len(clean) / 2)
        for country in gdxx[end:end2]:
            country = country.replace("\n", "")
            gj.append(country)
        xm = []
        gs = int(len(clean) / 2)
        if index - 1 == gs:
            for mc in gdxx[:index - 1]:
                mc = mc.replace("\n", "")
                xm.append(mc)
        else:
            for mc in gdxx[:index - 1]:
                mc = mc.replace("\n", "")
                xm.append(mc)
            for mc in gdxx[end2:]:
                mc = mc.replace("\n", "")
                xm.append(mc)
        zhenghe = {}
        sb = 0
        for j in range(0, len(clean), 2):
            gdxxdict = {}
            gdxxdict["证件种类"] = clean[j]
            gdxxdict["证件号码"] = clean[j + 1]
            gdxxdict["经济性质"] = tzxx[j]
            gdxxdict["投资比例"] = tzxx[j + 1]
            gdxxdict["国籍"] = gj[sb]
            gdxxdict["股东名称"] = xm[sb]
            wc = gdxxdict
            sb += 1
            zhenghe["{}".format(sb)] = wc
        pdf_dict['股东信息'] = zhenghe
        tzfxx2, tzfxx3, tzfxx4, tzfxx5, tzfxx6, tzfxx7, tzfxx8, tzfxx9, tzfxx10 = {}, {}, {}, {}, {}, {}, {}, {}, {}
        tzfxx1 = json.dumps(zhenghe, ensure_ascii=False)
        tzfxx2 = json.dumps(tzfxx2, ensure_ascii=False)
        tzfxx3 = json.dumps(tzfxx3, ensure_ascii=False)
        tzfxx4 = json.dumps(tzfxx4, ensure_ascii=False)
        tzfxx5 = json.dumps(tzfxx5, ensure_ascii=False)
        tzfxx6 = json.dumps(tzfxx6, ensure_ascii=False)
        tzfxx7 = json.dumps(tzfxx7, ensure_ascii=False)
        tzfxx8 = json.dumps(tzfxx8, ensure_ascii=False)
        tzfxx9 = json.dumps(tzfxx9, ensure_ascii=False)
        tzfxx10 = json.dumps(tzfxx10, ensure_ascii=False)
        # params = (
        #     self.batchid, "0", "0", self.companyid, self.customerid, tzfxx1, tzfxx2, tzfxx3, tzfxx4, tzfxx5,
        #     tzfxx6, tzfxx7, tzfxx8, tzfxx9, tzfxx10)
        # self.insert_db("[dbo].[Python_Serivce_GSTaxInfo_AddParent]", params)
    except:
        pdf_dict['所属行业明细'] = ""
        pdf_dict['从业人数'] = ""
        pdf_dict['存货计价方法'] = ""
        pdf_dict['企业会计准则为'] = ""
    pdf_dict['纳税调整后所得'] = sz[18]
    ksmx = {}
    try:
        for i in range(len(nf) - 1):
            try:
                if nf[i] == "2016":
                    ksmx[nf[i]] = sz[18]
                else:
                    ksmx[nf[i]] = nstzhsd[i]
            except:
                ksmx[nf[i]] = nstzhsd[i]
    except:
        print("ksmx")
    pdf_dict["亏损明细"] = ksmx
    print(pdf_dict)
    return pdf_dict

# parse_ndpdf('年度申报表详情10024417000014718405.pdf')
# parse_ndpdf('年度申报表详情10024417000014709743.pdf')
# parse_ndpdf("年度申报表详情10024417000013589901.pdf")
parse_ndpdf('年度申报表详情10024417000014827345.pdf')

# import tabula
#
# df=tabula.read_pdf('D:\\新建文件夹\\excercise-master\\年度申报表详情10024417000014718405.pdf')
# print(df)