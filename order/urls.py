from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
        path('createOrder', views.createOrder, name="createOrder"),
        path('orderStatusChange', views.orderStatusChange, name="orderStatusChange"),
        path('relatedOrder/<int:affairId>', views.relatedOrder, name="relatedOrder"),
]
