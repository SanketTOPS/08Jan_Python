from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Note
from .forms import NoteForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

class AddNoteView(LoginRequiredMixin, View):
    def get(self, request):
        form = NoteForm()
        return render(request, 'NoteApp/add_note.html', {'form': form})

    def post(self, request):
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.status = 'Pending'
            note.save()
            messages.success(request, 'Note submitted successfully! It is currently pending admin approval.')
            return redirect('my_notes')
        return render(request, 'NoteApp/add_note.html', {'form': form})

class MyNotesView(LoginRequiredMixin, View):
    def get(self, request):
        notes = Note.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'NoteApp/my_notes.html', {'notes': notes})

# Admin-side views for managing notes
class AdminManageNotesView(View):
    # This will be integrated into AdminApp later or kept here
    def get(self, request):
        if not request.user.is_staff:
            messages.error(request, "Unauthorized access.")
            return redirect('dashboard')
            
        status_filter = request.GET.get('status', 'Pending')
        notes = Note.objects.filter(status=status_filter).order_by('-created_at')
        return render(request, 'AdminApp/manage_notes.html', {
            'notes': notes,
            'status_filter': status_filter
        })

class AdminNoteActionView(View):
    def post(self, request, note_id, action):
        if not request.user.is_staff:
            return redirect('dashboard')
            
        note = get_object_or_404(Note, id=note_id)
        if action == 'approve':
            note.status = 'Approved'
        elif action == 'reject':
            note.status = 'Rejected'
        note.save()

        # Send confirmation email
        subject = f'Your Note Update: {note.title}'
        context = {
            'full_name': note.user.full_name,
            'note_title': note.title,
            'status': note.status
        }
        html_content = render_to_string('emails/note_status_email.html', context)
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [note.user.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        messages.success(request, f'Note "{note.title}" has been {note.status}. User notified via email.')
        return redirect('admin_manage_notes')
