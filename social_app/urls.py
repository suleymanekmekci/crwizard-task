from django.urls import path
from . import views

app_name = "social_app"
urlpatterns = [
    path('', views.index, name="index"),
    path('logout/', views.logoutUser, name="logoutUser"),

]
