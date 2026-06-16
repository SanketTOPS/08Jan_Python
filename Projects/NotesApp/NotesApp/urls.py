from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_redirect, name='home'),
    path('admin/', admin.site.urls),
    path('', include('CoreApp.urls')),
    path('', include('UserApp.urls')),
    path('', include('NoteApp.urls')),
    path('', include('AdminApp.urls')),
    path('payment/', include('PaymentApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
