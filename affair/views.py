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
        accountInfo = AccountInfo.objects.get(phoneNumber=request.COOKIES['phoneNumber'])
        print(request.POST)
        data = request.POST
        print(accountInfo.phoneNumber)
        print("\n\n"+data['type'])
        affairInfo = AffairInfo(affairProviderId=accountInfo,
                            type=data['type'][0],
                            tag=data['type'][0], #里边会有多个标签，后边加
                            affairDetail=data['affairDetail'],
                            affairCreateTime=timezone.now(),
                            reward=data['reward'][0],
                            NeedReceiverNum=int(data['receiverNum'][0])
                            )
        affairInfo.save()
        new_img = affairInfo.affairimg_set.create(
            img = request.FILES['img_file'],
            name = request.FILES['img_file'].name
        )


    sendBack = {'statusCode': '1'}
    return JsonResponse(sendBack)
