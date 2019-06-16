from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.files.storage import default_storage
import json
from django.utils import timezone
from affair.models import AffairImg, AffairInfo
from login.models import AccountInfo

def createAffair(request):
    context={}
    return render(request,'affair/createAffair.html',context)

def processSubmit(request):
    if request.method == 'POST':
        print(request)
        accountInfo = AccountInfo.objects.get(phoneNumber=request.COOKIES['phoneNumber'])
        print(request.POST)
        data = request.POST
        print(accountInfo.phoneNumber)
        affairInfo = AffairInfo(affairProviderId=accountInfo,
                            type=data['type'][0],
                            affairDetail=data['affairDetail'],
                            affairCreateTime=timezone.now(),
                            NeedReceiverNum=int(data['receiverNum'][0])
                            )
        print(data.getlist('tag'))
        temp = ''
        # reward待补充
        for tag in data.getlist('tag'): #里边会有多个标签
            temp = temp + tag + ';'
            print(temp)
        affairInfo.tag = temp
        affairInfo.save()
        print(request.FILES.getlist('img_file'))

        count = 0
        for imgFile in request.FILES.getlist('img_file'):
            count = count + 1
            new_img = affairInfo.affairimg_set.create(
                img = imgFile,
                name = imgFile.name
            )


    sendBack = {'statusCode': '1'}
    return JsonResponse(sendBack)
