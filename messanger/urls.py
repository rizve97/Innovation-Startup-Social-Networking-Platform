from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'message'

urlpatterns = [
    path("<str:username>", views.message, name="semessage"),
]