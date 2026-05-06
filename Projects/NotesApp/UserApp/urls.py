from django.urls import path
from .views import SignupView, OTPVerifyView, LoginView, LogoutView, DashboardView, ResendOTPView, ProfileView, ForgotPasswordView, ResetPasswordOTPView, SetNewPasswordView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify_otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password-otp/', ResetPasswordOTPView.as_view(), name='reset_password_otp'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),
]
