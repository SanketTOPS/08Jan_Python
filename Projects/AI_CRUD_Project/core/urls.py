from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('delete-confirm/<int:pk>/', views.student_delete_confirm, name='student_delete_confirm'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('edit-form/<int:pk>/', views.student_edit_form, name='student_edit_form'),
    path('update/<int:pk>/', views.student_update, name='student_update'),
]
