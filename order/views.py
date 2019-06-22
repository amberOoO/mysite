from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from affair.models import *
from login.models import *
from django.utils import timezone

import json
import pymysql


# Create your views here.


def createOrder(request):
    sendBack = {}           # statusCode:'0'创建成功,'1'上传的数据错误，'2'数据库错误, '3'事务不存在, '4'人手已经够了哟
    try:
        data = json.loads(request.body)
        print(data)
    except:
        print("createOrder()中数据获取错误!")
        sendBack["statusCode"] = "1"
        return JsonResponse(sendBack)

    receiverId = data['receiverId']
    providerId = data['providerId']
    affairId = data['affairId']
    try:
        db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
        cursor = db.cursor(pymysql.cursors.DictCursor)
    except:
        print('createOrder()数据库连接错误!')
        sendBack["statusCode"] = "2"
        return JsonResponse(sendBack)

    try:
        sql = 'select receiverNum, needReceiverNum from affair_affairInfo as info where info.affairId=' + str(affairId)
        cursor.execute(sql)
        numInfo = cursor.fetchone()
        print(numInfo)

        if numInfo['receiverNum'] < numInfo['needReceiverNum']:
            try:
                # 应用Django自带的数据库插入方式，需要多查询三次，浪费时间和服务器性能
                # providerInfo = AccountInfo.objects.get(id=providerId)
                # receiverInfo = AccountInfo.objects.get(id=receiverId)
                # affairInfo = AffairInfo.objects.get(affairId=affairId)
                #
                # orderInfo = OrderInfo(affairId=affairInfo,
                #                       affairProviderId=providerInfo,
                #                       orderCreateTime=timezone.now(),
                #                       orderStatus='0', refundFlag='0')
                # orderInfo.save()
                #
                # order_account = Order_Account(affairProviderId=providerInfo,
                #                               affairReceiverId=receiverInfo,
                #                               orderId=orderInfo)
                # order_account.save()

                # 创建订单
                sql = """INSERT INTO
                        order_orderinfo( orderCreateTime, orderStatus, refundFlag, affairId, affairProviderId_id)
                        values ( '{0}', {1}, {2}, {3}, {4})""".format(str(timezone.now()), str("'0'"), str("'0'"), str(affairId), str(providerId))
                cursor.execute(sql)

                #获取orderId
                orderId = cursor.lastrowid


                # 在相关的订单—账户表中进行插入
                sql = """
                insert into order_order_account(affairProviderId_id, affairReceiverId_id, orderId_id)
                values({}, {}, {})""".format(str(providerId), str(receiverId), str(orderId))
                cursor.execute(sql)

                # 更新事务表中接受人数
                sql = """
                update affair_affairInfo as affairInfo
                set affairInfo.receiverNum = affairInfo.receiverNum + 1
                where affairInfo.affairId = {0}""".format(str(affairId))
                cursor.execute(sql)

                db.commit()
                #print('\n\n\n\n????\n\n\n\n')

            except Exception as e:
                print("createOrder插入、更新数据库时出错，详情：\n"+"Failed:", e)
                db.rollback()
                db.close()
                sendBack["statusCode"] = "2"
                return JsonResponse(sendBack)
        else:
            sql = 'select receiverNum from affair_affairInfo as info where info.affairId={0}'.format(str(affairId))
            cursor.execute(sql)
            numInfo = cursor.fetchone()

            sendBack["statusCode"] = "4"
            sendBack["receiverNum"] = str(numInfo['receiverNum'])
            db.close()
            return JsonResponse(sendBack)

    except:
        print("事务不存在！")
        db.close()
        sendBack["statusCode"] = "3"
        return JsonResponse(sendBack)

    sql = 'select receiverNum from affair_affairInfo as info where info.affairId={0}'.format(str(affairId))
    cursor.execute(sql)
    numInfo = cursor.fetchone()
    db.close()
    sendBack["statusCode"] = "0"
    sendBack["receiverNum"] = str(numInfo['receiverNum'])
    return JsonResponse(sendBack)
