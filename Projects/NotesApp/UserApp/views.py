from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .forms import SignupForm, OTPVerifyForm, LoginForm, UserProfileForm
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'UserApp/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True # Active but not verified
            user.save()
            
            # Generate and Send HTML OTP Email
            otp = user.generate_otp()
            subject = 'Your NotesApp Verification Code'
            context = {
                'full_name': user.full_name,
                'otp': otp
            }
            html_content = render_to_string('emails/otp_email.html', context)
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email.attach_alternative(html_content, "text/html")
            
            try:
                email.send()
                messages.success(request, 'Signup successful! Please check your email for OTP.')
                request.session['verify_email'] = user.email
                return redirect('verify_otp')
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}')
                return render(request, 'UserApp/signup.html', {'form': form})
        
        return render(request, 'UserApp/signup.html', {'form': form})

class OTPVerifyView(View):
    def get(self, request):
        email = request.session.get('verify_email')
        if not email:
            return redirect('signup')
        form = OTPVerifyForm()
        return render(request, 'UserApp/verify_otp.html', {'form': form, 'email': email})

    def post(self, request):
        email = request.session.get('verify_email')
        if not email:
            return redirect('signup')
            
        form = OTPVerifyForm(request.POST)
        user = User.objects.filter(email=email).first()
        
        if form.is_valid():
            otp_input = form.cleaned_data['otp']
            if user and user.is_otp_valid(otp_input):
                user.is_verified = True
                user.otp = None
                user.otp_expiry = None
                user.save()
                messages.success(request, 'Email verified successfully! You can now login.')
                del request.session['verify_email']
                return redirect('login')
            else:
                if user:
                    user.otp_attempts += 1
                    user.save()
                    if user.otp_attempts >= 3:
                        messages.error(request, 'Max attempts reached. Please resend OTP.')
                    else:
                        messages.error(request, 'Invalid or expired OTP.')
                else:
                    messages.error(request, 'User not found.')
        
        return render(request, 'UserApp/verify_otp.html', {'form': form, 'email': email})

class ResendOTPView(View):
    def get(self, request):
        email = request.session.get('verify_email')
        if not email:
            return redirect('signup')
            
        user = User.objects.filter(email=email).first()
        if user:
            otp = user.generate_otp()
            subject = 'Your NotesApp Verification Code'
            context = {
                'full_name': user.full_name,
                'otp': otp
            }
            html_content = render_to_string('emails/otp_email.html', context)
            text_content = strip_tags(html_content)
            
            email_msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()
            
            messages.success(request, 'New OTP sent to your email.')
        return redirect('verify_otp')

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = LoginForm()
        return render(request, 'UserApp/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.full_name}!')
                    return redirect('dashboard')
                else:
                    request.session['verify_email'] = user.email
                    messages.warning(request, 'Please verify your email first.')
                    return redirect('verify_otp')
            else:
                messages.error(request, 'Invalid email or password.')
        
        return render(request, 'UserApp/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('login')

from NoteApp.models import Note

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        approved_notes = Note.objects.filter(status='Approved').order_by('-created_at')
        return render(request, 'UserApp/dashboard.html', {'approved_notes': approved_notes})

class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'UserApp/forgot_password.html')

    def post(self, request):
        email_addr = request.POST.get('email')
        user = User.objects.filter(email=email_addr).first()
        
        if user:
            otp = user.generate_otp()
            subject = 'Password Reset OTP - NotesApp'
            context = {
                'full_name': user.full_name,
                'otp': otp,
                'purpose': 'reset your password'
            }
            html_content = render_to_string('emails/otp_email.html', context)
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user.email])
            email.attach_alternative(html_content, "text/html")
            email.send()
            
            request.session['reset_email'] = user.email
            messages.success(request, 'OTP sent to your email for password reset.')
            return redirect('reset_password_otp')
        else:
            messages.error(request, 'No user found with this email address.')
            return render(request, 'UserApp/forgot_password.html')

class ResetPasswordOTPView(View):
    def get(self, request):
        email = request.session.get('reset_email')
        if not email: return redirect('forgot_password')
        form = OTPVerifyForm()
        return render(request, 'UserApp/verify_reset_otp.html', {'form': form, 'email': email})

    def post(self, request):
        email = request.session.get('reset_email')
        if not email: return redirect('forgot_password')
        
        form = OTPVerifyForm(request.POST)
        user = User.objects.filter(email=email).first()
        
        if form.is_valid():
            otp_input = form.cleaned_data['otp']
            if user and user.is_otp_valid(otp_input):
                request.session['otp_verified'] = True
                return redirect('set_new_password')
            else:
                messages.error(request, 'Invalid or expired OTP.')
        return render(request, 'UserApp/verify_reset_otp.html', {'form': form, 'email': email})

class SetNewPasswordView(View):
    def get(self, request):
        if not request.session.get('otp_verified'): return redirect('forgot_password')
        return render(request, 'UserApp/set_new_password.html')

    def post(self, request):
        if not request.session.get('otp_verified'): return redirect('forgot_password')
        
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'UserApp/set_new_password.html')
            
        email = request.session.get('reset_email')
        user = User.objects.filter(email=email).first()
        if user:
            user.set_password(password)
            user.otp = None
            user.otp_expiry = None
            user.save()
            
            # Cleanup session
            del request.session['reset_email']
            del request.session['otp_verified']
            
            messages.success(request, 'Password reset successful! You can now login.')
            return redirect('login')
        return redirect('forgot_password')

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, 'UserApp/profile.html', {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        return render(request, 'UserApp/profile.html', {'form': form})
