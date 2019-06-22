from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
import json
from django.utils import timezone
from affair.models import AffairImg, AffairInfo
from login.models import AccountInfo
from login.views import cookiesVerify
from affair.views import typeDic
import pymysql
# Create your views here.

def totalInfo(request):

    context = {"typeDic": typeDic}
    return render(request, "myinfo/myinfo.html", context)
