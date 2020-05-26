import traceback

from django.shortcuts import render

# Create your views here.
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
import json
import base64
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# from django_redis import get_redis_connection
import hashlib
import json
import requests
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from .models import Student,Event


def test(request):
    return HttpResponse('ok')


# @api_view(['POST'])

def wechatlogin(request):
    #前端发送code到后端,后端发送网络请求到微信服务器换取openid
    appid = 'wxb3a8c258fd1798f6'
    secret = 'd10e2068511e6e478013b5eaeae4267e'
    print(1)
    js_code = request.GET['code']
    print(js_code)
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)  # 将json数据包转成字典
    print(response)
    if 'errcode' in response:
        # 有错误码
        return HttpResponse(json.dumps(response),content_type='application/json; charset=utf-8')
    # 登录成功
    openid = response['openid']
    session_key = response['session_key']
    if not openid:
        return HttpResponse(json.dumps(response), content_type='application/json; charset=utf-8')

    # 判断用户是否第一次登录
    try:
        user = Student.objects.get(openid=openid)
    except Exception:
        # 微信用户第一次登陆,新建用户
        user = Student.objects.create(openid=openid)
        print("ok")
    finally:
        return HttpResponse(json.dumps(response),content_type='application/json; charset=utf-8')


def updateinfo(request):
    try:
        openid = request.GET['openid']
        truename = request.GET['truename']
        college = request.GET['college']
        cardNumber = request.GET['cardNumber']
        phoneNumber = request.GET['phoneNumber']
        qqNumber = request.GET['qqNumber']
        email = request.GET['email']
        user = Student.objects.get(openid=openid)
        if truename !='' and user.truename!=truename:
            user.truename=truename
        if college !='' and user.college!=college:
            user.college=college
        if cardNumber !='' and user.cardNumber!=cardNumber:
            user.cardNumber=cardNumber
        if qqNumber !='' and user.qqNumber!=qqNumber:
            user.qqNumber=qqNumber
        if phoneNumber !='' and user.phoneNumber != phoneNumber:
            user.phoneNumber = phoneNumber
        if email !='' and user.email!=email:
            user.email=email
        user.save()
        return HttpResponse(json.dumps({'msg':'修改成功'}),status=200)
    except Exception:
        return HttpResponse(json.dumps({'msg':'修改失败'}),status=404)

def searchinfo(request):
    res = {'data': {},'status': 500}
    try:
        openid = request.GET['openid']
        user = Student.objects.get(openid=openid)
        data={
              'truename': user.truename,
              'college': user.college,
              'cardNumber':user.cardNumber,
              'phoneNumber':user.phoneNumber,
              'qqNumber':user.qqNumber,
              'email':user.email
              }
        res['status'] = 200
        res['data'] = data
        return HttpResponse(json.dumps(res),content_type='application/json; charset=utf-8')
    except Exception:
        res['status']=404
        return HttpResponse(json.dumps(res),content_type='application/json; charset=utf-8')

class Test(APIView):
    def get(self, request):
        a = request.GET['a']
        res = {
            'success': True,
            'data': 'a'
        }
        return Response(res)

def writecnt(cnt):
    cnt=str(cnt)
    file=os.path.join(settings.STATICFILES_DIRS[0], "cnt.txt")
    print(file)
    with open(file, 'w') as f:
        f.writelines(cnt)
    f.close()

def readcnt():
    file=os.path.join(settings.STATICFILES_DIRS[0], "cnt.txt")
    print(file)
    with open(file, 'r') as f:
        a = f.readline()
    f.close()
    print(type(a))
    a=int(a)
    print(a)
    return a

def devide(photo):
    if photo is None:
        return []
    m = photo.split(';')
    print(m)
    com=[]
    for i in range(len(m)):
        com.append(str(m[i]))
    print(com)
    return com

class SEND2(APIView):
    count=readcnt()
    def post(self, request):
       try:
           if request.method == 'POST':
               hasimage = request.POST.get('hasimage')
               print(type(hasimage))
               event = Event()
               if(hasimage=='1'):
                   SEND.count+=1
                   image = request.FILES['image']
                   url='photo/'+str(SEND.count)+".jpg"
                   filename = os.path.join(settings.STATICFILES_DIRS[0],url)
                   print(filename)
                   with open(filename, 'wb') as f:
                       f.write(image.read())
                       f.close()
                   ones = '/static/' + url
                   print(ones)
                   event.photo=ones
                   print('ok')
               event.openid=request.POST.get('openid')
               print(event.openid)
               event.truename=request.POST.get('truename')
               event.text=request.POST.get('text')
               print(event.text)
               event.type = request.POST.get('type')
               event.phoneNumber = request.POST.get('phoneNumber')
               event.status = request.POST.get('status')
               event.qqNumber = request.POST.get('qqNumber')
               event.date = request.POST.get('date')
               event.time = request.POST.get('time')
               event.avatarURL=request.POST.get('avatarURL')
               print(event.avatarURL)
               event.save()
               return Response({"msg": "发送成功", "code": "200"})
       except Exception as e:
           traceback.print_exc()
           # SEND.count=back
           return Response({"msg": "发送失败"})
       finally:
           writecnt(SEND.count)

class SEND(APIView):
    count=readcnt()
    def post(self, request):
       try:
           back=SEND.count
           if request.method == 'POST':
               # s=str(request.body)
               # re=json.loads(s)
               # print(re['openid'])
               print(request.body)
               event=Event()
               event.openid = request.POST.get('openid')
               print(event.openid)
               event.truename = request.POST.get('truename')
               print(event.truename)
               event.text = request.POST.get('date')
               event.qqNumber = request.POST.get('qqNumber')
               event.phoneNumber = request.POST.get('phoneNumber')
               event.type = request.POST.get('type')
               event.date = request.POST.get('date')
               event.time = request.POST.get('time')
               event.status = request.POST.get('status')
               event.iscard = request.POST.get('iscard')
               event.avatarURL = request.POST.get('avatarURL')
               urls = ''
               photolist = ['photo1', 'photo2', 'photo3', 'photo4', 'photo5', 'photo6']
               for i in photolist:
                   re = request.POST.get(i, '')
                   if re != '':
                       SEND.count += 1
                       img = re.split(',')[1]
                       img = bytes(img, encoding='utf-8')
                       data = base64.b64decode(img)
                       url = "photo/" + str(SEND.count) + ".jpg"
                       filename = os.path.join(settings.STATICFILES_DIRS[0], url)
                       print(filename)
                       with open(filename, 'wb') as f:
                           f.write(data)
                       ones = '/static/' + url
                       ones += ';'
                       print(ones)
                       urls += ones
                       print(urls)
               event.photo=urls[:-1]
               writecnt(SEND.count)
               event.save()
               return Response({"msg": "发送成功", "code": "200"})
       except Exception as e:
           traceback.print_exc()
           SEND.count=back
           return Response({"msg": "发送失败"})
       finally:
           writecnt(SEND.count)

class GETLOST(APIView):
    result = Event.objects.filter(status__in=['1'])
    lenth = len(result)
    def get(self, request):
        page = int(request.GET['page'])
        print(page)
        print(self.lenth)
        comments = []
        if page*5>self.lenth:
            res = self.result[(page - 1) * 5:self.lenth]
        else:
            res=self.result[(page-1)*5:page*5]
        for one in res:
            com = {}
            com['id'] = one.id
            com['truename'] = one.truename
            com['photo'] = devide(one.photo)
            com['date'] = one.date
            com['time'] = one.time
            com['phoneNumber'] = one.phoneNumber
            com['qqNumber'] = one.qqNumber
            com['status'] = one.status
            com['text'] = one.text
            com['type'] = one.type
            com['avatarURL'] = one.avatarURL
            # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
            comments.append(com)
        # print(comments)
        return Response(comments)

class GETFIND(APIView):
    result = Event.objects.filter(status__in=['3'])
    lenth = len(result)
    def get(self, request):
        page = int(request.GET['page'])
        print(page)
        comments = []
        if page*5>self.lenth:
            res = self.result[(page - 1) * 5:self.lenth]
        else:
            res=self.result[(page-1)*5:page*5]
        for one in res:
            com = {}
            com['id'] = one.id
            com['truename'] = one.truename
            com['photo'] = devide(one.photo)
            com['date'] = one.date
            com['time'] = one.time
            com['phoneNumber'] = one.phoneNumber
            com['qqNumber'] = one.qqNumber
            com['status'] = one.status
            com['text'] = one.text
            com['type'] = one.type
            com['avatarURL'] = one.avatarURL
            # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
            comments.append(com)
        print(comments)
        return Response(comments)

class MYLOST(APIView):
    result=None
    lenth=0
    def get(self, request):
        openid = request.GET['openid']
        page = int(request.GET['page'])
        if(page==1):
            MYLOST.result = Event.objects.filter(status__in=['1', '2']).filter(openid=openid)
            MYLOST.lenth = len(MYLOST.result)
        print(MYLOST.result)
        comments = []
        if page*5>MYLOST.lenth:
            res = MYLOST.result[(page - 1) * 5:MYLOST.lenth]
        else:
            res=MYLOST.result[(page-1)*5:page*5]
        print("res:",res)
        for one in res:
            com = {}
            com['id'] = one.id
            com['truename'] = one.truename
            com['photo'] = devide(one.photo)
            com['date'] = one.date
            com['time'] = one.time
            com['phoneNumber'] = one.phoneNumber
            com['qqNumber'] = one.qqNumber
            com['status'] = one.status
            com['text'] = one.text
            com['type'] = one.type
            com['avatarURL'] = one.avatarURL
            # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
            comments.append(com)
        return Response(comments)


class MYFIND(APIView):
    result = None
    lenth = 0

    def get(self, request):
        openid = request.GET['openid']
        page = int(request.GET['page'])
        if (page == 1):
            MYFIND.result = Event.objects.filter(status__in=['3', '4']).filter(openid=openid)
            MYFIND.lenth = len(MYFIND.result)
        comments = []
        if page*5>MYFIND.lenth:
            res = MYFIND.result[(page - 1) * 5:MYFIND.lenth]
        else:
            res=MYFIND.result[(page-1)*5:page*5]
        for one in res:
            com = {}
            com['id'] = one.id
            com['truename'] = one.truename
            com['photo'] = devide(one.photo)
            com['date'] = one.date
            com['time'] = one.time
            com['phoneNumber'] = one.phoneNumber
            com['qqNumber'] = one.qqNumber
            com['status'] = one.status
            com['text'] = one.text
            com['type'] = one.type
            com['avatarURL'] = one.avatarURL
            # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
            comments.append(com)
        return Response(comments)





def changeStatus(request):
    pass

def searchevent(request):
    pass

