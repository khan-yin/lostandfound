import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random

from_addr = 'xx'  # 邮件发送账号
to_addrs = 'xx'  # 接收邮件账号
qqCode = 'xxx'  # 授权码（这个要填自己获取到的）
smtp_server = 'smtp.qq.com'  # 固定写死
smtp_port = 465  # 固定端口

# 配置服务器
stmp = smtplib.SMTP_SSL(smtp_server, smtp_port)
stmp.login(from_addr, qqCode)

digit = random.randint(1000, 9999)
print(digit)
# 组装发送内容
message = MIMEText('你的验证码是{}'.format(digit), 'plain', 'utf-8')  # 发送的内容
message['From'] = Header("小程序系统消息", 'utf-8')  # 发件人
message['To'] = Header("用户", 'utf-8')  # 收件人
subject = '验证码提醒'
message['Subject'] = Header(subject, 'utf-8')  # 邮件标题

try:
    stmp.sendmail(from_addr, to_addrs, message.as_string())
except Exception as e:
    print('邮件发送失败--' + str(e))
print('邮件发送成功')