from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from affair.views import typeDic

def index(request):
    context = {"typeDic": typeDic}
    return render(request,'index/index.html', context);
