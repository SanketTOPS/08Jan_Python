from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import logout

# Create your views here.
def index(request):
    if request.method=='POST':
        em=request.POST["email"]
        pa=request.POST["password"]
        
        user=UserSignup.objects.filter(email=em,password=pa)
        if user:
            print("Login Success!")
            request.session["user"]=em #session generate
            
            return redirect('home')
        else:
            print("Error! Login Faild...")
    return render(request,'index.html')

def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            print("Signup Successfully!")
            return redirect('/')
        else:
            print(form.errors)
    return render(request,'signup.html')

def home(request):
    #Session get
    user=request.session.get('user')
    return render(request,'home.html',{'user':user})

def userlogout(request):
    logout(request)
    return redirect('/')
    
    