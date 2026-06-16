from django.urls import path
from . import views

urlpatterns = [
    path('', views.covid_stats, name='covid_stats'),
]
