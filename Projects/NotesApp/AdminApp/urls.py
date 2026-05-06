from django.urls import path
from .views import AdminDashboardView, ToggleUserStatusView, AddUserView, UpdateUserView, DeleteUserView, AdminMessageListView, AdminMessageDetailView, AdminDeleteMessageView

urlpatterns = [
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('toggle-user/<int:user_id>/', ToggleUserStatusView.as_view(), name='toggle_user'),
    path('add-user/', AddUserView.as_view(), name='add_user'),
    path('update-user/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('admin-messages/', AdminMessageListView.as_view(), name='admin_messages'),
    path('admin-message/<int:msg_id>/', AdminMessageDetailView.as_view(), name='admin_message_detail'),
    path('admin-message-delete/<int:msg_id>/', AdminDeleteMessageView.as_view(), name='admin_delete_message'),
]
