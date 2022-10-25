#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
-------------------------------------------------
@File    :   notice.py
@Time    :   2022/10/25 14:00:34
@Author  :   Rhythm-2019 
@Version :   1.0
@Contact :   rhythm_2019@163.com
@Desc    :   通知
-------------------------------------------------
Change Activity:
-------------------------------------------------
'''
__author__ = 'Rhythm-2019'

# here put the import lib
import logging
import config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


logger = logging.getLogger('notcie')

def email_notice(receiver_email_list, subject, content, attach_file=None):
    msg = MIMEMultipart()
    
    msg.attach(MIMEText(content))
    
    # 添加附件
    if attach_file is not None: #最开始的函数参数我默认设置了None ，想添加附件，自行更改一下就好
        docFile = attach_file
        docApart = MIMEApplication(open(docFile, 'rb').read())
        docApart.add_header('Content-Disposition', 'attachment', filename=docFile)
        msg.attach(docApart)    
    
    for receiver_email in receiver_email_list:
        msg['Subject'] = subject
        msg['From'] = config.SENDER_EMAIL
        msg['To'] = receiver_email
    
        try:
            s = smtplib.SMTP_SSL(config.STMP_SERVER_ADDR, config.STMP_SERVER_PORT)
            s.login(config.SENDER_EMAIL, config.SENDER_STMP_SECRET)
            s.sendmail(config.SENDER_EMAIL, receiver_email, msg.as_string())
            logger.info("send a email to %s" % receiver_email)
        except smtplib.SMTPException as e:
            logger.info("failed to send email to %s, eror is %s" % receiver_email, e)
        finally:
            s.quit()
      