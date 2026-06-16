from django.urls import path
from . import views

urlpatterns = [
    path('', views.sms_home_view, name='sms_home'),
    path('success/', views.success_view, name='success'),
    path('reset/', views.reset_view, name='reset'),
]
