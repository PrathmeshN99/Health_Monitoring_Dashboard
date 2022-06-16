from django.contrib import admin
from django.urls import path,include
from DashboardApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register',views.register,name="register"),
    path('',views.login,name="login"),
    path('home',views.home,name="home"),
    path('editProfile',views.editProfile,name="editProfile"),
    path('logout',views.logout_view,name="logout"),
    path('about', views.about,name='about'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)