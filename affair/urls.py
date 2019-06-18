from django.urls import path
from . import views

app_name = 'affair'
urlpatterns = [
    path('createAffair', views.createAffair, name="createAffair"),
    path('processSubmit', views.processSubmit, name="processSubmit"),
    path('<str:affairType>', views.affairDisplay, name="affairDisplay"),
]
