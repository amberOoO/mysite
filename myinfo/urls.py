from django.urls import path
from . import views

app_name = 'myinfo'
urlpatterns = [


    path('', views.totalInfo, name="totalInfo"),
]
