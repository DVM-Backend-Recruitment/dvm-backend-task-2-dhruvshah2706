from django.shortcuts import render,HttpResponse

def home(request):
    return render(request,'ticket/login.html')
