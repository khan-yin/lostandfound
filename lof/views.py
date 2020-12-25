import traceback

from django.shortcuts import render

# Create your views here.
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
from .models import Student, Event
from . import search, post_msg
import random
from .dbConnect import *
from .DB_Operations import *


def test(request):
    return HttpResponse('ok')


# @api_view(['POST'])

def wechatlogin(request):
    # 前端发送code到后端,后端发送网络请求到微信服务器换取openid
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
        return HttpResponse(json.dumps(response), content_type='application/json; charset=utf-8')
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
        return HttpResponse(json.dumps(response), content_type='application/json; charset=utf-8')


def updateinfo(request):
    try:
        openid = request.GET['openid']
        truename = request.GET['truename']
        college = request.GET['college']
        cardNumber = request.GET['cardNumber']
        phoneNumber = request.GET['phoneNumber']
        qqNumber = request.GET['qqNumber']
        email = request.GET['email']
        Update(openid=openid, truename=truename, college=college, cardNumber=cardNumber, phoneNumber=phoneNumber,
               qqNumber=qqNumber, email=email)
        user = Student.objects.get(openid=openid)
        if truename != '' and user.truename != truename:
            user.truename = truename
        if college != '' and user.college != college:
            user.college = college
        if cardNumber != '' and user.cardNumber != cardNumber:
            user.cardNumber = cardNumber
        if qqNumber != '' and user.qqNumber != qqNumber:
            user.qqNumber = qqNumber
        if phoneNumber != '' and user.phoneNumber != phoneNumber:
            user.phoneNumber = phoneNumber
        if email != '' and user.email != email:
            user.email = email
        user.save()
        return HttpResponse(json.dumps({'msg': '修改成功'}), status=200)
    except Exception:
        return HttpResponse(json.dumps({'msg': '修改失败'}), status=404)

def searchinfo(request):
    res = {'data': {}, 'status': 500}
    try:
        openid = request.GET['openid']
        user = Student.objects.get(openid=openid)
        data = {
            'truename': user.truename,
            'college': user.college,
            'cardNumber': user.cardNumber,
            'phoneNumber': user.phoneNumber,
            'qqNumber': user.qqNumber,
            'email': user.email
        }

        data = Search_By_Openid(openid)

        res['status'] = 200
        res['data'] = data
        return HttpResponse(json.dumps(res), content_type='application/json; charset=utf-8')
    except Exception:
        res['status'] = 404
        return HttpResponse(json.dumps(res), content_type='application/json; charset=utf-8')

class Test(APIView):
    def get(self, request):
        a = request.GET['a']
        res = {
            'success': True,
            'data': 'a'
        }
        return Response(res)


def writecnt(cnt):
    cnt = str(cnt)
    file = os.path.join(settings.STATICFILES_DIRS[0], "cnt.txt")
    print(file)
    with open(file, 'w') as f:
        f.writelines(cnt)
    f.close()

def readcnt():
    file = os.path.join(settings.STATICFILES_DIRS[0], "cnt.txt")
    print(file)
    with open(file, 'r') as f:
        a = f.readline()
    f.close()
    print(type(a))
    a = int(a)
    print(a)
    return a

def devide(photo):
    if photo is None:
        return []
    m = photo.split(';')
    print(m)
    com = []
    for i in range(len(m)):
        com.append(str(m[i]))
    print(com)
    return com


class SEND2(APIView):
    count = readcnt()

    def post(self, request):
        try:
            event = Event()
            if request.method == 'POST':
                hasimage = request.POST.get('hasimage')
                print(hasimage)
                print(type(hasimage))
                if hasimage is None:
                    return Response({"msg": "发送失败"}, content_type="'application/json; charset=utf-8'")
                if hasimage == '0':
                    event = post_msg.add_event(event, request)
                    return Response({"msg": "发送成功", "code": "200", "id": event.id},
                                    content_type="'application/json; charset=utf-8'")
                elif hasimage == '1':
                    SEND.count += 1
                    image = request.FILES['image']
                    url = 'photo/' + str(SEND.count) + ".jpg"
                    post_msg.write_img(image, url)
                    ones = '/static/' + url
                    print(ones)
                    event.photo = ones
                    print('ok')
                    event = post_msg.add_event(event, request)
                    return Response({"msg": "发送成功", "code": "200", "id": event.id},
                                    content_type="'application/json; charset=utf-8'")
                elif hasimage == '2':
                    openid = request.POST.get('openid')
                    if openid is not None:
                        SEND.count += 1
                        image = request.FILES['image']
                        url = 'photo/' + str(SEND.count) + ".jpg"
                        post_msg.write_img(image, url)
                        ones = '/static/' + url
                        print(ones)
                        event.photo = ones
                        print('ok')
                        event = post_msg.add_event(event, request)
                    else:
                        id = request.POST.get('id')
                        id = int(id)
                        event = Event.objects.get(id=id)
                        SEND.count += 1
                        image = request.FILES['image']
                        url = 'photo/' + str(SEND.count) + ".jpg"
                        print(url)
                        filename = os.path.join(settings.STATICFILES_DIRS[0], url)
                        print(filename)
                        with open(filename, 'wb') as f:
                            f.write(image.read())
                        f.close()
                        one = ';/static/' + url
                        event.photo += one
                        event.save()
                    return Response({"msg": "发送成功", "code": "200", "id": event.id},
                                    content_type='application/json; charset=utf-8')
        except Exception as e:
            traceback.print_exc()
            return Response({"msg": "发送失败"}, content_type='application/json; charset=utf-8')
        finally:
            writecnt(SEND.count)

class SEND(APIView):
    count = readcnt()

    def post(self, request):
        try:
            back = SEND.count
            if request.method == 'POST':
                # s=str(request.body)
                # re=json.loads(s)
                # print(re['openid'])
                print(request.body)
                event = Event()
                event.openid = request.POST.get('openid')
                print(event.openid)
                event.truename = request.POST.get('truename')
                print(event.truename)
                event.text = request.POST.get('text')
                event.qqNumber = request.POST.get('qqNumber')
                event.phoneNumber = request.POST.get('phoneNumber')
                event.type = request.POST.get('type')
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
                event.photo = urls[:-1]
                writecnt(SEND.count)
                event.save()
                return Response({"msg": "发送成功", "code": "200"})
        except Exception as e:
            traceback.print_exc()
            SEND.count = back
            return Response({"msg": "发送失败"})
        finally:
            writecnt(SEND.count)


# getlost获取丢失的所有信息
class GETLOST(APIView):
    result = Event.objects.filter(status__in=['1'])
    lenth = len(result)
    def get(self, request):
        self.result = Event.objects.filter(status__in=['1'])
        self.lenth = len(self.result)
        page = int(request.GET['page'])
        print(page)
        print(self.lenth)
        comments = []
        if page * 5 > self.lenth:
            res = self.result[(page - 1) * 5:self.lenth]
        else:
            res = self.result[(page - 1) * 5:page * 5]
        for one in res:
            com = {}
            com['id'] = one.id
            com['truename'] = one.truename
            com['photo'] = devide(one.photo)
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
        comments2 = getMsgsql(page, "1")
        res2 = Response(comments2)
        res = Response(comments)
        print(type(res))
        print(type(res2))
        return Response(comments2)


#getfind获取招领的所有信息
class GETFIND(APIView):
    result = Event.objects.filter(status__in=['3'])
    lenth = len(result)
    def get(self, request):
        page = int(request.GET['page'])
        print(page)
        self.result = Event.objects.filter(status__in=['3'])
        self.lenth = len(self.result)
        comments = []
        if page * 5 > self.lenth:
            res = self.result[(page - 1) * 5:self.lenth]
        else:
            res = self.result[(page - 1) * 5:page * 5]
        for one in res:
            com = {}
            com['id'] = one.id
            com['truename'] = one.truename
            com['photo'] = devide(one.photo)
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
        comments2 = getMsgsql(page, "3")
        res2 = Response(comments2)
        return Response(comments2)


class MYLOST(APIView):
    result = None
    len = 0

    def get(self, request):
        openid = request.GET['openid']
        page = int(request.GET['page'])
        MYLOST.result = Event.objects.filter(status__in=['1', '2']).filter(openid=openid)
        MYLOST.lenth = len(MYLOST.result)
        print(MYLOST.result)
        comments = []
        if page * 5 > MYLOST.lenth:
            res = MYLOST.result[(page - 1) * 5:MYLOST.lenth]
        else:
            res = MYLOST.result[(page - 1) * 5:page * 5]
        print("res:", res)
        for one in res:
            com = {}
            com['id'] = one.id
            com['truename'] = one.truename
            com['photo'] = devide(one.photo)
            com['time'] = one.time
            com['phoneNumber'] = one.phoneNumber
            com['qqNumber'] = one.qqNumber
            com['status'] = one.status
            com['text'] = one.text
            com['type'] = one.type
            com['avatarURL'] = one.avatarURL
            com['count'] = len(MYLOST.result)
            # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
            comments.append(com)
        comments2 = getMyinfo(page, openid, "lost")

        return Response(comments2)


class MYFIND(APIView):
    def get(self, request):
        openid = request.GET['openid']
        page = int(request.GET['page'])
        result = Event.objects.filter(status__in=['3', '4']).filter(openid=openid)
        lenth = len(result)
        comments = []
        if page * 5 > lenth:
            res = result[(page - 1) * 5:lenth]
        else:
            res = result[(page - 1) * 5:page * 5]
        for one in res:
            com = {}
            com['id'] = one.id
            com['truename'] = one.truename
            com['photo'] = devide(one.photo)
            com['time'] = one.time
            com['phoneNumber'] = one.phoneNumber
            com['qqNumber'] = one.qqNumber
            com['status'] = one.status
            com['text'] = one.text
            com['type'] = one.type
            com['avatarURL'] = one.avatarURL
            com['count'] = len(result)
            # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
            comments.append(com)
        comments2 = getMyinfo(page, openid, "find")
        return Response(comments2)


@api_view(['GET'])
def changeStatus(request):
    try:
        id = int(request.GET['id'])
        print(type(id))
        print(id)
        # event=Event.objects.get(id=id)
        # event.status=str(int(event.status)+1)
        # event.save()
        ChangeSta(id)
        return Response({"msg": "操作成功"})
    except Exception:
        traceback.print_exc()
        return Response({"msg": "操作失败"})


@api_view(['GET'])
def deleterequest(request):
    try:
        id = int(request.GET['id'])
        Delete(id)
        # Event.objects.get(id=id).delete()
        return Response({"msg": "操作成功"})
    except Exception:
        traceback.print_exc()
        return Response({"msg": "操作失败"})


@api_view(['GET'])
def searchevent(request):
    try:
        msg = request.GET['content']
        status = request.GET['status']
        print(msg)
        res = Event.objects.filter(status__in=[status])
        comments = []
        for one in res:
            if search.findintext(msg, one.truename) or search.findintext(msg, one.text) or search.findtime(msg,
                                                                                                           one.time):
                com = {}
                com['id'] = one.id
                com['truename'] = one.truename
                com['photo'] = devide(one.photo)
                com['time'] = one.time
                com['phoneNumber'] = one.phoneNumber
                com['qqNumber'] = one.qqNumber
                com['status'] = one.status
                com['text'] = one.text
                com['type'] = one.type
                com['avatarURL'] = one.avatarURL
                com['count'] = len(res)
                # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
                comments.append(com)
        return Response(comments)
    except Exception:
        traceback.print_exc()
        return Response({"msg": "查询失败"})


@api_view(['GET'])
def sendcardmsg(request):
    appid = 'wxb3a8c258fd1798f6'
    secret = 'd10e2068511e6e478013b5eaeae4267e'
    wx_accesstoken_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + appid + "&secret=" + secret
    response = json.loads(requests.get(wx_accesstoken_url).content)  # 将json数据包转成字典
    print(response)
    if 'errcode' in response:
        # 有错误码
        return HttpResponse(json.dumps(response), content_type='application/json; charset=utf-8')


@api_view(['GET'])
def cardattention(request):
    try:
        card = request.GET['card']
        qq = request.GET['qqNumber']
        phone = request.GET['phoneNumber']
        stu = Student.objects.get(cardNumber=card)

        data = Search_By_CardNumber(cardNumber=card)
        # msg = '请问您是{}同学吗，你的校园卡被这位同学捡到了，请联系TA来领取,TA的qq是{},电话是{}' \
        #     .format(stu.truename, qq, phone)
        msg = '请问您是{}同学吗，你的校园卡被这位同学捡到了，请联系TA来领取,TA的qq是{},电话是{}' \
            .format(data["truename"], data["qqNumber"], data["phoneNumber"])
        if stu is not None:
            flag = post_msg.emailto(stu.email, '校园卡提醒', msg)
            # flag = post_msg.emailto(data["email"],'校园卡提醒',msg)
            if flag:
                return Response({"msg": "发送成功"})
            else:
                return Response({"msg": "发送失败"})
    except Exception:
        return Response({'msg': '该系统中暂时还没有这位同学的信息'})
