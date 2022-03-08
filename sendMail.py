#!/usr/bin/env python3
#  -*-  coding:utf-8  -*-
# 发送邮件模块 
import smtplib, re
from typing import List
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.utils import formataddr

FROMADDR='mail@foo.com'    # 发件人邮箱账号
PASSWORD = 'youpassword'         # 发件人邮箱密码
SMTP_SERVER = 'smtp.foo.com'    
SMTP_PORT = 465
 
#             #收件人              #主题           #邮件内容     # 附件
def sendmail(toaddress: List[str], subject: str, content: str, text_file: str=None):
    fromaddr = FROMADDR
    password = PASSWORD
    text_plain = MIMEText(content, 'plain', 'utf-8')
    m = MIMEMultipart()
    m.attach(text_plain)  # 添加普通文本
    if text_file:
        text_att = MIMEApplication(open(text_file, 'rb').read())
        # 去除附件路径
        filename = re.sub('.*/', '', text_file)
        text_att.add_header('Content-Disposition', 'attachment', filename=filename)
        m.attach(text_att)    # 添加附件
    m['Subject'] = Header(subject,'utf-8')
    m['From']=formataddr(["和对讲基础版运维", FROMADDR])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
    m['To']=  ','.join(toaddress)

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddress, m.as_string())
        server.quit()
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    content="""
    你好，
        this is test
    """
    send_log = sendmail(toaddress=["foo@bar.com"], subject="测试邮件", content=content, text_file="sendMail.py")
    print(send_log)
