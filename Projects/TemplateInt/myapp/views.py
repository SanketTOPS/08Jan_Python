from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def donation(request):
    return render(request,'donation.html')

def feature(request):
    return render(request,'feature.html')

def team(request):
    return render(request,'team.html')

def testimonial(request):
    return render(request,'testimonial.html')

def errorpage(request):
    return render(request,'404.html')