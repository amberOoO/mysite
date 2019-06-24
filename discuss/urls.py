from django.urls import path
from . import views

app_name = 'discuss'
urlpatterns = [
    path('discussProcess', views.discussProcess, name="discussProcess"),
]

