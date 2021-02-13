from django.urls import path
from . import views

app_name = "xml_app"
urlpatterns = [
    path('add/', views.addXml, name="addXml"),

]
