from django.shortcuts import render,HttpResponse,redirect

def home(request):
    return redirect('regular-dashboard')
