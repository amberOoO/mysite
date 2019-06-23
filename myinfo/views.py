from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
import json
from django.utils import timezone
from login.views import cookiesVerify
from affair.views import typeDic
import pymysql


# Create your views here.

def totalInfo(request):
    context = {"typeDic": typeDic}
    return render(request, "myinfo/myinfo.html", context)


def personalInfo(request):
    context = {"typeDic": typeDic}
    results = cookiesVerify(request)
    if (results == '0'):
        try:
            id = request.COOKIES['id']
            db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            select * 
            from login_accountinfo as info
            where info.id = {0}""".format(str(id))
            cursor.execute(sql)
            info = cursor.fetchone()

            context['statusCode'] = '0'
            context.update(info)
            print(context)
            return render(request, "myinfo/personalInfo.html", context)

        except Exception as e:
            print('personalInfo()数据库连接失败', e)
            context['statusCode'] = '2'
            return render(request, "myinfo/personalInfo.html", context)

    else:
        context['statusCode'] = '1'  # 登陆状态异常
        return render(request, "myinfo/personalInfo.html", context)


def changeBasicInfo(request):
    if request.method == 'POST':
        result = cookiesVerify(request)
        if (result == '0'):
            try:
                data = request.POST
                db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
                cursor = db.cursor(pymysql.cursors.DictCursor)

                sql = """
                update login_accountinfo as info
                set info.nickName = '{0}', info.school = '{1}', info.studentNo = '{2}'
                where info.id = {3}""".format(str(data['nickName']), str(data['school']), str(data['schoolNumber']), str(request.COOKIES['id']))

                cursor.execute(sql)
                db.commit()
                db.close()
                sendBack = {'statusCode': '0', 'nickName': data['nickName']}  # 修改成功
                return JsonResponse(sendBack)

            except Exception as e:
                print('personalInfo()数据库连接失败', e)
                db.rollback()
                db.close()
                sendBack = {'statusCode': '2'}  # 数据库连接失败
                return JsonResponse(sendBack)

        else:
            sendBack = {'statusCode': '1'}  # 登陆状态异常
            return JsonResponse(sendBack)


def changePassword(request):
    context = {'typeDic': typeDic}
    return render(request, 'myinfo/changePassword.html', context)

def processPasswordChange(request):
    if request.method == 'POST':
        result = cookiesVerify(request)
        if (result == '0'):
            try:
                data = request.POST
                db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
                cursor = db.cursor(pymysql.cursors.DictCursor)

                sql = """
                select passwd
                from login_accountinfo as info
                where info.id = {0}""".format(str(request.COOKIES['id']))
                cursor.execute(sql)
                passwd = cursor.fetchone()
                print(passwd)
                if(passwd['passwd']==data['rawPwd']):
                    sql = """
                    update login_accountinfo as info
                    set info.passwd = '{0}'
                    where info.id = {1}""".format(str(data['pwd']), str(request.COOKIES['id']))

                    cursor.execute(sql)
                    db.commit()
                    db.close()
                    sendBack = {'statusCode': '0', 'nickName': data['pwd']}  # 修改成功
                    return JsonResponse(sendBack)
                else:
                    db.close()
                    sendBack = {'statusCode': '3', 'nickName': data['pwd']}
                    return JsonResponse(sendBack)
            except Exception as e:
                print('processPasswordChange()数据库连接失败', e)
                db.rollback()
                db.close()
                sendBack = {'statusCode': '2'}  # 数据库连接失败
                return JsonResponse(sendBack)

        else:
            sendBack = {'statusCode': '1'}  # 登陆状态异常
            return JsonResponse(sendBack)

def changePhoneNumber(request):
    context = {"typeDic": typeDic}
    results = cookiesVerify(request)
    if (results == '0'):
        try:
            id = request.COOKIES['id']
            db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
            cursor = db.cursor(pymysql.cursors.DictCursor)

            sql = """
            select info.phoneNumber 
            from login_accountinfo as info
            where info.id = {0}""".format(str(id))
            cursor.execute(sql)
            info = cursor.fetchone()

            context['statusCode'] = '0'
            context['rawPhoneNumber'] = info['phoneNumber']
            return render(request, "myinfo/changePhoneNumber.html", context)

        except Exception as e:
            print('personalInfo()数据库连接失败', e)
            context['statusCode'] = '2'
            return render(request, "myinfo/changePhoneNumber.html", context)

    else:
        context['statusCode'] = '1'  # 登陆状态异常
        return render(request, "myinfo/changePhoneNumber.html", context)

def phoneNumberProcess(request):
    if request.method == 'POST':
        result = cookiesVerify(request)
        if (result == '0'):
            try:
                data = request.POST
                print(data)
                db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
                cursor = db.cursor(pymysql.cursors.DictCursor)

                sql = """
                select *
                from login_accountinfo as info
                where info.phoneNumber = {0}""".format(str(data['newPhoneNumber']))
                cursor.execute(sql)
                phoneNumber = cursor.fetchone()
                print(phoneNumber)
                # 为空说明数据库中不存在这样的电话号码，即不重复，可以修改电话号码
                if not phoneNumber:
                    sql = """
                    update login_accountinfo as info
                    set info.phoneNumber = '{0}'
                    where info.id = {1}""".format(str(data['newPhoneNumber']), str(request.COOKIES['id']))

                    cursor.execute(sql)
                    db.commit()
                    db.close()
                    sendBack = {'statusCode': '0', 'newPhoneNumber': data['newPhoneNumber']}  # 修改成功
                    return JsonResponse(sendBack)
                else:
                    db.close()
                    sendBack = {'statusCode': '3'}
                    return JsonResponse(sendBack)
            except Exception as e:
                print('processPasswordChange()数据库连接失败', e)
                db.rollback()
                db.close()
                sendBack = {'statusCode': '2'}  # 数据库连接失败
                return JsonResponse(sendBack)

        else:
            sendBack = {'statusCode': '1'}  # 登陆状态异常
            return JsonResponse(sendBack)