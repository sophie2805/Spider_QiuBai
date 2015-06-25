#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

__author__ = 'Sophie2805'

class SMail:
    def __init__(self):
        self.sender = '***@qq.com'
        self.receiver = ['222@163.com','333@qq.com']
        self.subject = '糗百热门20条推送'
        self.username = '***@qq.com'
        self.password = '******'

    def send_mail(self,msg):
        try:
            self.msg = MIMEText(msg,'plain','utf-8')
            self.msg['Subject'] = Header(self.subject,'utf-8')
            self.msg['To'] = ','.join(self.receiver)
            self.msg['From'] = self.sender
            self.smtp = smtplib.SMTP()
            self.smtp.connect('smtp.qq.com')
            self.smtp.login(self.username,self.password)
            self.smtp.sendmail(self.msg['From'],self.receiver,self.msg.as_string())
            self.smtp.quit()
            return '1'
        except Exception, e:
            return str(e)