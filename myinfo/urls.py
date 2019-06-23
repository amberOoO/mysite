from django.urls import path
from . import views

app_name = 'myinfo'
urlpatterns = [


    path('personalInfo', views.personalInfo, name="personalInfo"),
    path('changeBasicInfo', views.changeBasicInfo, name="changeBasicInfo"),
    path('changePassword', views.changePassword, name="changePassword"),
    path('processPasswordChange', views.processPasswordChange, name="processPasswordChange"),
    path('changePhoneNumber', views.changePhoneNumber, name="changePhoneNumber"),
    path('phoneNumberProcess', views.phoneNumberProcess, name="phoneNumberProcess"),
    path('myCreatedAffair', views.myCreatedAffair, name="myCreatedAffair"),
    path('', views.totalInfo, name="totalInfo"),
]

