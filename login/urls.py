from django.urls import path
from . import views
urlpatterns = [
    path('loginVerify',views.loginVerify),
    path('register',views.register),
]