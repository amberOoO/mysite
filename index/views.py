from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context={}
    return render(request,'index/index.html',context);
