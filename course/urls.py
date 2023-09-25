from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.courseHome, name='coursehome'),
    path('post', views.post, name='post'),
    path("delete/<int:courseId>", views.delCourse, name='delcourse'),
    path('enroll', views.enrollCourse, name='enroll'),

    
]