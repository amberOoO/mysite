from django.shortcuts import render

def createAffair(request):
    context={}
    return render(request,'affair/createAffair.html',context);