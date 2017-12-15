# -*- coding:utf-8 -*-
from email import encoders

__author__ = 'IanChen'

import time
import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart,MIMEBase
from email.mime.application import MIMEApplication

content='使用smtp和email模块发送邮件'
msg= MIMEMultipart()
content1=MIMEText(content,'utf8')
msg.attach(content1)

msg_from='626614767@qq.com'
passwd=''#密码
msg_to='626614767@qq.com'

subject='附件测试'
msg['Subject']=subject
msg['From']=msg_from
msg['To']=msg_to


with open('F:\python 学习\excercise\captcha\code.jpg','rb') as f:
    #jpg类型的附件
    # jpgatt=MIMEApplication(f.read())
    # jpgatt.add_header('Content-Disposition', 'attachment', filename='code.jpg')
    # msg.attach(jpgatt)
    mimeatt=MIMEBase('image','jpg',filename='ceshi.jpg')
    mimeatt.add_header('Content-Disposition', 'attachment', filename='ceshi.jpg')
    mimeatt.set_payload(f.read())
    encoders.encode_base64(mimeatt)
    msg.attach(mimeatt)

# 首先是xlsx类型的附件
# xlsxpart = MIMEApplication(open('test.xlsx', 'rb').read())
# xlsxpart.add_header('Content-Disposition', 'attachment', filename='test.xlsx')
# msg.attach(xlsxpart)

# mp3类型的附件
# mp3part = MIMEApplication(open('kenny.mp3', 'rb').read())
# mp3part.add_header('Content-Disposition', 'attachment', filename='benny.mp3')
# msg.attach(mp3part)

# pdf类型附件
# part = MIMEApplication(open('foo.pdf', 'rb').read())
# part.add_header('Content-Disposition', 'attachment', filename="foo.pdf")
# msg.attach(part)



s=smtplib.SMTP_SSL('smtp.qq.com',465)
s.login(msg_from,passwd)
s.sendmail(msg_from,msg_to,msg.as_string())
print('发送成功')
