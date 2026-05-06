from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import ContactMessage

class AboutView(View):
    def get(self, request):
        return render(request, 'CoreApp/about.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'CoreApp/contact.html')

    def post(self, request):
        name = request.POST.get('name')
        email_addr = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to Database
        ContactMessage.objects.create(
            name=name,
            email=email_addr,
            subject=subject,
            message=message
        )
        
        # Send Thank You Email
        email_subject = 'Thank you for contacting NotesApp'
        context = {
            'name': name,
            'subject': subject
        }
        html_content = render_to_string('emails/contact_thanks.html', context)
        text_content = strip_tags(html_content)
        
        try:
            email = EmailMultiAlternatives(
                email_subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [email_addr]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
        except Exception as e:
            # We still want to redirect even if email fails, but maybe log it
            print(f"Email error: {e}")

        messages.success(request, f"Thank you {name}, your message has been sent successfully!")
        return redirect('contact')
