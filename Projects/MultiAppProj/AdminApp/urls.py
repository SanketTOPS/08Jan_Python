from django.contrib import admin
from django.urls import path,include
from AdminApp import views

urlpatterns = [
   path('',views.admin_login),
]
