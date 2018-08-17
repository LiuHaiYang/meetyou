# -*- coding: utf-8 -*-
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
def send_email(email,sub):
    print(email,sub)
    msg = MIMEMultipart()
    content = '''<html><body>
            <h4>你好！</h4>'''
    content += '''<br>已成功推荐请您及时查看！
    </body></html>'''

    txt = MIMEText(content, 'html', 'utf-8')
    msg.attach(txt)
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"

    msg['from'] = 'oceango@126.com'
    msg['subject'] = str(sub)
    mail_to = email
    msg['To'] = mail_to
    mail_from = "oceango@126.com"
    smtp = smtplib.SMTP()
    smtp.connect('smtp.126.com',25)
    smtp.login('oceango@126.com', '799899onA')
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    smtp.quit()