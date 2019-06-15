from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core.files.storage import default_storage
import json

from affair.models import IMG

def createAffair(request):
    context={}
    return render(request,'affair/createAffair.html',context)

def processSubmit(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES['img_file'],
            name = request.FILES['img_file'].name
        )
        new_img.save()

        print(request.POST)

    sendBack = {'statusCode': '1'}
    return JsonResponse(sendBack)