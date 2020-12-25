# -*- coding: utf-8 -*-

"""have a nice day.

@author: Khan
@contact:  
@time: 2020/5/29 20:48
@file: post_msg.py
@desc:  
"""
import os
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def write_img(image, url):
    filename = os.path.join(settings.STATICFILES_DIRS[0], url)
    print(filename)
    with open(filename, 'wb') as f:
        f.write(image.read())
    f.close()


def add_event(event, request):
    event.openid = request.POST.get('openid')
    print(event.openid)
    event.truename = request.POST.get('truename')
    event.text = request.POST.get('text')
    print(event.text)
    event.type = request.POST.get('type')
    event.phoneNumber = request.POST.get('phoneNumber')
    event.status = request.POST.get('status')
    event.qqNumber = request.POST.get('qqNumber')
    event.time = request.POST.get('time')
    event.avatarURL = request.POST.get('avatarURL')
    print(event.avatarURL)
    event.save()
    return event


def emailto(to_addrs, subject, content):
    from_addr = '838278270@qq.com'  # 邮件发送账号
    qqCode = 'njlpqtmrykfrbajj'  # 授权码（这个要填自己获取到的）
    smtp_server = 'smtp.qq.com'  # 固定写死
    smtp_port = 465  # 固定端口

    # 配置服务器
    stmp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    stmp.login(from_addr, qqCode)

    # 组装发送内容
    message = MIMEText(content, 'plain', 'utf-8')  # 发送的内容
    message['From'] = Header("小程序系统消息", 'utf-8')  # 发件人
    message['To'] = Header("用户", 'utf-8')  # 收件人

    message['Subject'] = Header(subject, 'utf-8')  # 邮件标题

    try:
        stmp.sendmail(from_addr, to_addrs, message.as_string())
    except Exception as e:
        print('邮件发送失败--' + str(e))
        return False
    print('邮件发送成功')
    return True