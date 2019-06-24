from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, Http404
from django.core.files.storage import default_storage
import json
from django.utils import timezone
from login.views import cookiesVerify
from affair.views import typeDic, invertTypeDic
import pymysql


# Create your views here.

# 总后台显示界面
def totalInfo(request):
    context = {"typeDic": typeDic}
    return render(request, "myinfo/myinfo.html", context)


# 个人详情页面
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


# 修改个人信息的业务逻辑
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
                where info.id = {3}""".format(str(data['nickName']), str(data['school']), str(data['schoolNumber']),
                                              str(request.COOKIES['id']))

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


# 密码修改页面
def changePassword(request):
    context = {'typeDic': typeDic}
    return render(request, 'myinfo/changePassword.html', context)


# 修改密码的处理逻辑
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
                if (passwd['passwd'] == data['rawPwd']):
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


# 修改电话号码
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


# 修改电话的业务逻辑
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


# 自己创建的事务的详细界面
def myCreatedAffair(request):
    sql = """
    select affairId, affairName, receiverNum, needReceiverNum, affairCreateTime, statusFlag, type
    from affair_affairInfo as info
    where info.affairProviderId_id = {0}""".format(str(request.COOKIES['id']))

    # 开始在数据库中查找相关内容
    db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    data = cursor.fetchall()

    for affair in data:
        typeChiness = affair['type']
        typeEnglish = invertTypeDic[typeChiness]
        affair['typeEnglish'] = typeEnglish
    context = {'typeDic': typeDic, 'affairData': data}
    return render(request, 'myinfo/myCreatedAffair.html', context)


def myReceivedAffair(request):
    db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
    cursor = db.cursor(pymysql.cursors.DictCursor)

    sql = """
     select *
    from order_orderInfo, affair_affairInfo
    where order_orderInfo.orderId in 
    (
    select order_order_account.orderId_id
    from order_order_account
    where order_order_account.affairReceiverId_id = '{0}'
    ) and order_orderInfo.affairId = affair_affairInfo.affairId""".format(str(request.COOKIES['id']))

    # 开始在数据库中查找相关内容

    cursor.execute(sql)
    data = cursor.fetchall()
    context = {'typeDic': typeDic, 'affairData': data}
    return render(request, 'myinfo/myReceivedAffair.html', context)

def changeAffairStatus(request):
    db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
    cursor = db.cursor(pymysql.cursors.DictCursor)

    data = json.loads(request.body)
    affairId = data['affairId']
    print(data)

    # 先判断这个事务是不是这个人创建的
    sql = """
    select info.affairProviderId_id, info.statusFlag
    from affair_affairInfo as info
    where info.affairId = {0}""".format(str(affairId))
    cursor.execute(sql)
    result = cursor.fetchone()

    if(str(result['affairProviderId_id']) != str(request.COOKIES['id'])):
        return HttpResponseForbidden()

    if(result['statusFlag']=='0'):
        flag = '2'
    elif(result['statusFlag']=='2'):
        flag = '0'
    else:
        return Http404()

    sql = """
    update affair_affairInfo as info
    set info.statusFlag = {0}
    where info.affairId = {1}""".format(str(flag),str(affairId))
    cursor.execute(sql)
    db.commit()

    db.close()
    sendBack = {"statusCode": '0'}
    return JsonResponse(sendBack)

def changeOrderStatus(request):

    # 验证登录
    postData = json.loads(request.body)
    orderId = postData['orderId']
    result = cookiesVerify(request)
    if (result == '0'):

        db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # 安全检查，看这该用户是否有此订单
        sql = '''
        select affairReceiverId_id
        from order_order_account
        where order_order_account.orderId_id = {0}'''.format(str(orderId))

        cursor.execute(sql)
        data = cursor.fetchone()

        if (str(request.COOKIES['id']) != str(data['affairReceiverId_id'])):
            db.close()
            print("权限错误")
            return HttpResponseForbidden()

        # 开始在数据库中查找相关内容

        # 查看orderStatus
        sql = """
        select *
        from affair_order_receiver_condition as info
        where info.orderId = {0}""".format(str(orderId))

        cursor.execute(sql)
        data = cursor.fetchone()

        oldOrderStatus = data['orderStatus']
        newStatusCode = '1'
        if (oldOrderStatus != '0'):
            db.close()
            sendBack = {'statusCode': '0'}
            return JsonResponse(sendBack)

        # 修改orderStatus
        sql = """
        update affair_order_receiver_condition as info
        set info.orderStatus = {0}
        where info.orderId = {1}""".format(str(newStatusCode), str(orderId))
        cursor.execute(sql)
        db.commit()
        db.close
        sendBack = {'statusCode': '0'}
        return JsonResponse(sendBack)

    else:
        return HttpResponseForbidden()
