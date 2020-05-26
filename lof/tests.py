from django.test import TestCase
import json
# Create your tests here.
import numpy as np
print(int('1')+1)
str="/static/photo/1.jpg;/static/photo/2.jpg;/static/photo/3.jpg;/static/photo/4.jpg;/static/photo/5.jpg;/static/photo/6.jpg"
str1="/static/photo/1.jpg"
m=str.split(';')
print(len(m))
for i in m:
    print(i)

with open('../templates/static/cnt.txt', 'r') as f:
    a=f.read()
f.close()
print(a)
print(type(a))

with open('../templates/static/cnt.txt', 'w') as f:
    f.writelines(a)
f.close()

byte=b'{"photo1":"","photo2":"","photo3":"","photo4":"","photo5":"","photo6":"","openid":"oTdQp49UU2enbIWN_CwTL6jiEdvk","truename":"\xe8\xb0\xa2\xe5\xb9\xbf\xe5\xb9\xb3","text":"","phoneNumber":"13720241937","status":1,"qqNumber":"oTdQp49UU2enbIWN_CwTL6jiEdvk","date":"2020/5/26","time":"\xe4\xb8\x8b\xe5\x8d\x888:18:40"}'
print(byte)
m=byte.decode()
print(m)
str='{"photo1":"","photo2":"","photo3":"","photo4":"","photo5":"","photo6":"","openid":"oTdQp49UU2enbIWN_CwTL6jiEdvk","truename":"\xe8\xb0\xa2\xe5\xb9\xbf\xe5\xb9\xb3","text":"","phoneNumber":"13720241937","status":1,"qqNumber":"oTdQp49UU2enbIWN_CwTL6jiEdvk","date":"2020/5/26","time":"\xe4\xb8\x8b\xe5\x8d\x888:18:40"}'
re=json.loads(m)
print(re['openid'])