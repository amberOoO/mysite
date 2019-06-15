from django.urls import path
from . import views

app_name = 'login'
urlpatterns = [
    path('loginVerify', views.loginVerify, name='loginVerify'),
    path('register', views.register, name='register'),
]
