from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from UserApp.models import User
from django.contrib import messages
from .forms import UserAdminForm
from CoreApp.models import ContactMessage

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to access this page.")
        return redirect('login')

class AdminDashboardView(AdminRequiredMixin, View):
    def get(self, request):
        status_filter = request.GET.get('status')
        users = User.objects.all().order_by('-date_joined')
        
        if status_filter == 'verified':
            users = users.filter(is_verified=True)
        elif status_filter == 'unverified':
            users = users.filter(is_verified=False)
            
        return render(request, 'AdminApp/dashboard.html', {
            'users': users,
            'status_filter': status_filter
        })

class ToggleUserStatusView(AdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user.is_superuser:
            messages.error(request, "Cannot deactivate a superuser.")
        else:
            user.is_active = not user.is_active
            user.save()
            status = "activated" if user.is_active else "deactivated"
            messages.success(request, f"User {user.email} has been {status}.")
        return redirect('admin_dashboard')

class AddUserView(AdminRequiredMixin, View):
    def get(self, request):
        form = UserAdminForm()
        return render(request, 'AdminApp/user_form.html', {'form': form, 'title': 'Add User'})

    def post(self, request):
        form = UserAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully.")
            return redirect('admin_dashboard')
        return render(request, 'AdminApp/user_form.html', {'form': form, 'title': 'Add User'})

class UpdateUserView(AdminRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserAdminForm(instance=user)
        return render(request, 'AdminApp/user_form.html', {'form': form, 'title': 'Update User'})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = UserAdminForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('admin_dashboard')
        return render(request, 'AdminApp/user_form.html', {'form': form, 'title': 'Update User'})

class DeleteUserView(AdminRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user.is_superuser:
            messages.error(request, "Cannot delete a superuser.")
        else:
            email = user.email
            user.delete()
            messages.success(request, f"User {email} has been deleted.")
        return redirect('admin_dashboard')

class AdminMessageListView(AdminRequiredMixin, View):
    def get(self, request):
        status_filter = request.GET.get('status')
        msgs = ContactMessage.objects.all().order_by('-created_at')
        
        if status_filter == 'read':
            msgs = msgs.filter(is_read=True)
        elif status_filter == 'unread':
            msgs = msgs.filter(is_read=False)
            
        return render(request, 'AdminApp/messages.html', {
            'msgs': msgs,
            'status_filter': status_filter
        })

class AdminMessageDetailView(AdminRequiredMixin, View):
    def get(self, request, msg_id):
        msg = get_object_or_404(ContactMessage, id=msg_id)
        if not msg.is_read:
            msg.is_read = True
            msg.save()
        return render(request, 'AdminApp/message_detail.html', {'msg': msg})

class AdminDeleteMessageView(AdminRequiredMixin, View):
    def post(self, request, msg_id):
        msg = get_object_or_404(ContactMessage, id=msg_id)
        msg.delete()
        messages.success(request, "Message deleted successfully.")
        return redirect('admin_messages')
