from django.shortcuts import render,redirect
from .forms import *

# Create your views here.
def index(request):
    if request.method=='POST':
        std=Studform(request.POST)
        if std.is_valid():
            std.save()
            print("Record inserted!")
        else:
            print(std.errors)
    return render(request,'index.html')

def showdata(request):
    stdata=Studinfo.objects.all()
    return render(request,'showdata.html',{'stdata':stdata})

def updatedata(request,id):
    stid=Studinfo.objects.get(id=id)
    if request.method=='POST':
        std=Studform(request.POST,instance=stid)
        if std.is_valid():
            std.save()
            print("Record updated!")
            return redirect('showdata')
        else:
            print(std.errors)
    return render(request,'updatedata.html',{'stid':stid})

def deletedata(request,id):
    stid=Studinfo.objects.get(id=id)
    Studinfo.delete(stid)
    return redirect('showdata')