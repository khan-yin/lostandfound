from django.test import TestCase

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