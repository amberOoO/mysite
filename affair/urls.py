from django.urls import path
from . import views

app_name = 'affair'
urlpatterns = [
    path('createAffair', views.createAffair, name="createAffair"),
    path('processSubmit', views.processSubmit, name="processSubmit"),
    path('editAffair/<int:affairId>', views.editAffair, name="editAffair"),
    path('processEditAffair/<int:affairId>', views.processEditAffair, name="processEditAffair"),
    path('<str:affairType>', views.affairDisplay, name="affairDisplay"),
    path('<str:affairType>/<int:affairId>', views.affairDetail, name="affairDetail"),
]
