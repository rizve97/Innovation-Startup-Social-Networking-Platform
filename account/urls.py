from django.contrib import admin
from django.urls import path
from account import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.userLogin, name='login'),
    path('logout', views.userLogout, name='logout'),
    path("change_password", views.Change_Password.as_view(), name='change_password')
]
