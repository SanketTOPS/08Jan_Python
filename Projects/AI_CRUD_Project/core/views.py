from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import StudentInfo, Subject

def student_list(request):
    students = StudentInfo.objects.all()
    subjects = Subject.objects.all()
    return render(request, 'core/student_list.html', {
        'students': students, 
        'subjects': subjects
    })

def student_create(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')
        subject_id = request.POST.get('subject')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        
        subject = get_object_or_404(Subject, id=subject_id) if subject_id else None
        
        student = StudentInfo.objects.create(
            student_id=student_id,
            name=name,
            subject=subject,
            email=email,
            dob=dob
        )
        return render(request, 'core/student_item.html', {'student': student})
    return HttpResponse(status=400)

def student_delete_confirm(request, pk):
    student = get_object_or_404(StudentInfo, pk=pk)
    return render(request, 'core/student_delete_modal.html', {'student': student})

def student_delete(request, pk):
    student = get_object_or_404(StudentInfo, pk=pk)
    student.delete()
    return HttpResponse('')

def student_edit_form(request, pk):
    student = get_object_or_404(StudentInfo, pk=pk)
    subjects = Subject.objects.all()
    return render(request, 'core/student_edit_form.html', {
        'student': student,
        'subjects': subjects
    })

def student_update(request, pk):
    student = get_object_or_404(StudentInfo, pk=pk)
    if request.method == 'POST':
        student.student_id = request.POST.get('student_id')
        student.name = request.POST.get('name')
        subject_id = request.POST.get('subject')
        student.email = request.POST.get('email')
        student.dob = request.POST.get('dob')
        
        if subject_id:
            student.subject = get_object_or_404(Subject, id=subject_id)
        
        student.save()
        return render(request, 'core/student_item.html', {'student': student})
    return HttpResponse(status=400)
