from django.contrib import admin
from django.urls import path,include
from DashboardApp import views

urlpatterns = [
    path('register',views.register,name="register"),
    path('',views.login,name="login"),
    path('home',views.home,name="home"),
]