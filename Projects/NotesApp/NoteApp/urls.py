from django.urls import path
from .views import AddNoteView, MyNotesView, AdminManageNotesView, AdminNoteActionView

urlpatterns = [
    path('add-note/', AddNoteView.as_view(), name='add_note'),
    path('my-notes/', MyNotesView.as_view(), name='my_notes'),
    path('admin-manage-notes/', AdminManageNotesView.as_view(), name='admin_manage_notes'),
    path('admin-note-action/<int:note_id>/<str:action>/', AdminNoteActionView.as_view(), name='admin_note_action'),
]
