from django.contrib import admin
from django.urls import path,include
from UserApp import views

urlpatterns = [
   path('',views.index),
]