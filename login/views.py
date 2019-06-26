from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
import json
from .models import *

def loginVerify(request):
    data = json.loads(request.body)
    print(str(data['loginPhoneNumber']))
    try:
        info = AccountInfo.objects.get(phoneNumber=data['loginPhoneNumber'])
        print(info)

        if (info.passwd == data['loginPassword']):
            # 登录成功
            sendBack = {'id': info.id, 'nickName': info.nickName, 'phoneNumber': info.phoneNumber, 'pwd': info.passwd,
                        'statusCode': '0'}
            return JsonResponse(sendBack)
        else:
            # 密码不正确
            sendBack = {'nickName': info.nickName, 'phoneNumber': info.phoneNumber,
                        'statusCode': '2'}
            return JsonResponse(sendBack)
    except:
        # 用户电话不存在
        sendBack = {'statusCode': '1'}
        return JsonResponse(sendBack)


def cookiesVerify(data):
    try:
        if (data.COOKIES['phoneNumber'] == ''):  # 未登录
            return '3'
        info = AccountInfo.objects.get(phoneNumber=data.COOKIES['phoneNumber'])

        if (info.passwd == data.COOKIES['password']):
            return '0'  # 账号正确
        else:
            return '2'  # 密码不正确
    except:
        return '1'  # 账号不存在


def register(request):
    data = json.loads(request.body)
    passwd = data['pwd']

    try:
        info = AccountInfo.objects.get(phoneNumber=data['phone'])
        sendBack = {'statusCode': '2', 'content': '用户电话已被注册'}
        return JsonResponse(sendBack)
    except:
        try:
            accountInfo = AccountInfo(passwd=data['pwd'], nickName=data['nickName'], phoneNumber=data['phone'],
                                      mailAddress=data['email'])
            accountInfo.save()
            sendBack = {'statusCode': '0', 'content': '注册成功'}
            return JsonResponse(sendBack)
        except:
            sendBack = {'statusCode': '1', 'content': '注册失败'}
            return JsonResponse(sendBack)


