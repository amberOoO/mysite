from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.files.storage import default_storage
import json
from django.utils import timezone
from affair.models import AffairImg, AffairInfo
from login.models import AccountInfo
from login.views import cookiesVerify
import pymysql

def discussProcess(request):
    try:
        data = json.loads(request.body)

        db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # 把评论信息插入
        sql = """
        insert into discuss_discuss(createTime, content, affairId_id)
        values('{0}','{1}', {2})""".format(str(timezone.now()), str(data['discussContent']), str(data['affairId']))
        cursor.execute(sql)
        # 把相关信息插入账户信息表
        disscussId = cursor.lastrowid
        sql = """
        insert into discuss_discuss_account(createrId, discussId_id)
        values({0},{1})""".format(str(request.COOKIES['id']), str(disscussId))
        cursor.execute(sql)

        db.commit()

        sendBack = {'statusCode': '0'}
        return JsonResponse(sendBack)
    except Exception as e:
        print("数据库错误：\n", e)
        sendBack = {'statusCode': '1'}
        return JsonResponse(sendBack)