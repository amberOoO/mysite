from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.files.storage import default_storage
import json
from django.utils import timezone
from affair.models import AffairImg, AffairInfo
from login.models import AccountInfo
from login.views import cookiesVerify
import pymysql

typeDic = {'study': '学习帮助',
           'life': '日常帮助',
           'restThing': '闲置物品',
           'techNeed': '技术帮助',
           'groupNeed': '组队需求',
           'other': '其他'}

invertTypeDic = dict([(v, k) for (k, v) in typeDic.items()])

typeArray = ['学习帮助', '日常帮助', '闲置物品', '技术帮助', '组队需求', '其他']

tagDic = {'errand': '跑腿',
          'takeOut': '外卖',
          'express': '快递',
          'tutor': '辅导',
          'findGroup': '组队',
          'competition': '竞赛',
          'findTheOtherPart': '找伴',
          'findFriend': '找伴'}

tagArray = ['跑腿', '外卖', '快递', '辅导', '组队', '竞赛', '找伴']


def createAffair(request):
    num = []
    temp = 1
    for i in range(10):
        num.append(temp)
        temp = temp * 2

    context = {'typeDic': typeDic, 'typeArray': typeArray, 'num': num, 'tagArray': tagArray}
    return render(request, 'affair/createAffair.html', context)


def processSubmit(request):
    if request.method == 'POST':
        result = cookiesVerify(request)
        print(request.POST)
        data = request.POST

        if (result == '0'):  # 密码认证正确
            accountInfo = AccountInfo.objects.get(phoneNumber=request.COOKIES['phoneNumber'])



        affairInfo = AffairInfo(affairProviderId=accountInfo,
                                type=data['type'],
                                affairName=data['affairName'],
                                affairDetail=data['affairDetail'],
                                affairCreateTime=timezone.now(),
                                lastUpdateTime=timezone.now(),
                                needReceiverNum=int(data['receiverNum'])
                                )

        if (data['reward'] == ''):
            affairInfo.rewardType = '0'
            affairInfo.rewardMoney = 0
        else:
            judge = '0'  # 0代表全是数字，则判断酬劳为RMB
            for c in data['reward']:
                if ((c <= '0' or c >= '9') and c != '.'):
                    judge = '1'
                    break
            affairInfo.rewardType = '0'
            if (judge == '0'):
                affairInfo.rewardMoney = float(data['reward'])
                print(float(data['reward']))
            else:
                affairInfo.rewardType = '1'
                affairInfo.rewardThing = data['reward']

        print(data.getlist('tag'))
        temp = ''
        for tag in data.getlist('tag'):  # 里边会有多个标签
            temp = temp + tag + ';'
        affairInfo.tag = temp
        affairInfo.save()

        count = 0
        for imgFile in request.FILES.getlist('img_file'):
            count = count + 1
            new_img = affairInfo.affairimg_set.create(
                img=imgFile,
                name=imgFile.name
            )
        sendBack = {'statusCode': '0'}
        return JsonResponse(sendBack)

    if (result == '1' or result == '2'):
        sendBack = {'statusCode': result}
        return JsonResponse(sendBack)

    sendBack = {'statusCode': '3'}
    return JsonResponse(sendBack)




def affairDisplay(request, affairType):
    db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # 为各个表创建视图
    createDatabaseView(db, cursor)

    # 开始正式查询相关类别的数据
    sql = "select * from view_affair_type_{0} ORDER BY affairCreateTime DESC".format(str(affairType))
    cursor.execute(sql)
    affairData = cursor.fetchall()
    previousId = -1

    # 解决一个事务有多个图片，前台展示时展示多个同样事务的问题
    for data in affairData:
        if (data['statusFlag'] == '0'):
            if (data['affairId'] != previousId):
                previousId = data['affairId']
                continue
            else:
                affairData.remove(data)

        else:
            affairData.remove(data)
    print(affairData)
    db.commit()
    db.close()

    context = {'affairData': affairData, 'defaultImgPath': 'affairImg/default.png', "typeDic": typeDic,
               'affairType': affairType}
    return render(request, 'affair/affairDisplay.html', context)


def createDatabaseView(db, cursor):
    for type in typeDic.keys():
        try:
            # 为每一个类别建立视图
            sql = "drop view if exists view_affair_type_" + type
            cursor.execute(sql)
            print(type)

            sql = "drop view if exists view_affair_type_briefInfo_" + type
            cursor.execute(sql)

            sql = "create view view_affair_type_briefInfo_{0}  as (select * from affair_affairinfo where affair_affairinfo.type = '{1}' )".format(
                str(type), str(typeDic[type]))
            cursor.execute(sql)

            sql = "create view view_affair_type_{0} as (select info.affairId, info.type, info.tag, info.affairDetail, info.affairCreateTime, info.rewardType, info.rewardMoney, info.rewardThing, info.needReceiverNum, info.receiverNum, info.affairProviderId_id, info.statusFlag, info.affairName, img.id, img.img, img.name from view_affair_type_briefInfo_{1} as info left join affair_affairimg as img on info.affairid = img.affair_id)".format(
                str(type), str(type))
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            db.close()
            print("创建视图错误：\n" + str(e))


def affairDetail(request, affairType, affairId):
    db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from view_affair_type_' + str(affairType) + ' as info where info.affairId = ' + str(affairId)
    cursor.execute(sql)
    affairData = cursor.fetchall()

    print(affairData)

    imgArray = []
    for img in affairData:
        temp = {'img': img['img'], 'name': img['name']}
        imgArray.append(temp)

    print(imgArray)

    # 评论信息
    sql = """
    select login_accountInfo.nickName as 'nickName', discuss_discuss.content as 'content', discuss_discuss.createTime as createTime 
    from discuss_discuss, discuss_discuss_account, login_accountInfo
    where discuss_discuss.id = discuss_discuss_account.discussId_id and discuss_discuss.affairId_id = {0} and login_accountInfo.id = discuss_discuss_account.createrId""".format(
        str(affairId))

    cursor.execute(sql)
    discussContent = cursor.fetchall()
    print(discussContent)

    db.commit()
    db.close()
    context = {'affairData': affairData[0], 'imgArray': imgArray, "typeDic": typeDic, "discussContent": discussContent}
    return render(request, 'affair/affairDetail.html', context)


def editAffair(request, affairId):
    db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
    cursor = db.cursor(pymysql.cursors.DictCursor)

    sql = '''
    select *
    from affair_affairInfo as info
    where info.affairId = {0}'''.format(str(affairId))

    cursor.execute(sql)
    data = cursor.fetchone()

    # 安全检查，看这事务是否属于该用户
    if (str(request.COOKIES['id']) != str(data['affairProviderId_id'])):
        print(data['affairProviderId_id'])
        print(request.COOKIES['id'])
        context = {"typeDic": typeDic}
        return HttpResponseForbidden()

    needReceiverNum = data['needReceiverNum']
    receiverNum = data['receiverNum']

    tag = data['tag']
    tag = tag.split(';')
    tag.pop()
    data['tag'] = tag

    num = []
    temp = 1
    for i in range(1,11):
        temp = temp * 2
        if (temp < receiverNum):
            print(temp)
            continue
        num.append(temp)
    context = {'typeDic': typeDic, 'typeArray': typeArray, 'num': num, 'tagArray': tagArray}
    context['previousedData'] = data

    db.close()
    return render(request, "affair/editAffair.html", context)


def processEditAffair(request, affairId):
    result = cookiesVerify(request)
    print(result)
    if (result == '0'):
        try:
            db = pymysql.connect('127.0.0.1', 'root', '522087905', 'mysite')
            cursor = db.cursor(pymysql.cursors.DictCursor)

            data = request.POST
            print(data)
            affairName = data['affairName']
            affairType = data['type']
            needReceiverNum = data['receiverNum']
            reward = data['reward']
            affairDetail = data['affairDetail']

            temp = ''
            for tag in data.getlist('tag'):  # 里边会有多个标签
                temp = temp + tag + ';'
            tag = temp
            print(tag)

            if (data['reward'] == ''):
                rewardType = '0'
                rewardMoney = 0
                rewardThing = 'nothing'
            else:
                judge = '0'  # 0代表全是数字，则判断酬劳为RMB
                for c in data['reward']:
                    if ((c <= '0' or c >= '9') and c != '.'):
                        judge = '1'
                        break
                rewardType = '0'
                if (judge == '0'):
                    rewardMoney = float(data['reward'])
                    rewardThing = 'nothing'
                else:
                    rewardType = '1'
                    rewardThing = data['reward']
                    rewardMoney = 0

            sql = """
                    update affair_affairInfo as info
                    set info.affairName = '{0}', info.needReceiverNum = {1}, info.tag = '{2}', info.affairDetail = '{3}', info.type = '{4}', info.rewardType = '{5}', info.rewardMoney = {6}, info.rewardThing = '{7}'
                    where info.affairId = {8}""".format(str(affairName), str(needReceiverNum),
                                                        str(affairDetail), str(affairDetail), str(affairType),
                                                        str(rewardType), str(rewardMoney), str(rewardThing),
                                                        str(affairId))
            print(sql)
            cursor.execute(sql)
            db.commit()
            if (request.FILES.getlist('img_file')):
                affairInfo = AffairInfo.objects.get(affairId=affairId)
                previousImg = AffairImg.objects.filter(affair_id=4)
                for img in previousImg:
                    img.delete()

                for imgFile in request.FILES.getlist('img_file'):
                    new_img = affairInfo.affairimg_set.create(
                        img=imgFile,
                        name=imgFile.name
                    )
            db.close()
            sendBack = {"statusCode": "0"}
            return JsonResponse(sendBack)

        except Exception as e:
            db.rollback()
            db.close()
            print("processEditAffair()数据库操作失败：\n", e)
            sendBack = {"statusCode": "2"}
            return JsonResponse(sendBack)
    else:
        sendBack = {"statusCode": "1"}
        return JsonResponse(sendBack)


class MyError(Exception):  # 定义一个异常类，继承Exception

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
