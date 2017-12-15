# -*- coding:utf-8 -*-
__author__ = 'IanChen'

import time
import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText

content='使用smtp和email模块发送邮件'
msg= MIMEText(content)
msg_from='626614767@qq.com'
passwd='rnvozihepwbsbfef'
msg_to='626614767@qq.com'

subject='邮件测试'
msg['Subject']=subject
msg['From']=msg_from
msg['To']=msg_to
# try:
s=smtplib.SMTP_SSL('smtp.qq.com',465)
s.login(msg_from,passwd)
s.sendmail(msg_from,msg_to,msg.as_string())
print('发送成功')
# except Exception as e:
#     print('发送失败')
# finally:
#     s.quit()