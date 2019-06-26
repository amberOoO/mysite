from django.urls import path
from . import views

app_name = 'affair'
urlpatterns = [
    path('createAffair', views.createAffair, name="createAffair"),
    path('processSubmit', views.processSubmit, name="processSubmit"),
    path('editAffair/<int:affairId>', views.editAffair, name="editAffair"),
    path('deleteAffair/<int:affairId>', views.deleteAffair, name="deleteAffair"),
    path('processEditAffair/<int:affairId>', views.processEditAffair, name="processEditAffair"),
    path('<str:affairType>/<int:affairId>', views.affairDetail, name="affairDetail"),
    path('<str:affairType>', views.affairDisplay, name="affairDisplay"),
]

